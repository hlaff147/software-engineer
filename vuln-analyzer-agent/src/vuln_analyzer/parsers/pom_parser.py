"""Parser for Maven pom.xml files."""

import re
import subprocess
from pathlib import Path
from typing import Optional

from lxml import etree

from vuln_analyzer.models import Dependency


class PomParser:
    """Parse Maven pom.xml files to extract dependencies."""
    
    MAVEN_NAMESPACE = {"m": "http://maven.apache.org/POM/4.0.0"}
    
    def __init__(self, project_path: Path):
        """Initialize parser with project path.
        
        Args:
            project_path: Path to Maven project root (containing pom.xml)
        """
        self.project_path = Path(project_path)
        self.pom_path = self.project_path / "pom.xml"
        self._properties: dict[str, str] = {}
        self._tree: Optional[etree._ElementTree] = None
    
    def parse(self) -> list[Dependency]:
        """Parse pom.xml and return list of dependencies.
        
        Returns:
            List of Dependency objects
        """
        if not self.pom_path.exists():
            raise FileNotFoundError(f"pom.xml not found at {self.pom_path}")
        
        self._tree = etree.parse(str(self.pom_path))
        self._extract_properties()
        
        dependencies = self._parse_dependencies()
        
        # Try to get transitive dependencies via Maven
        try:
            transitive = self._get_transitive_dependencies()
            dependencies.extend(transitive)
        except Exception:
            pass  # Continue with direct dependencies only
        
        # Remove duplicates
        seen = set()
        unique_deps = []
        for dep in dependencies:
            key = (dep.group_id, dep.artifact_id, dep.version)
            if key not in seen:
                seen.add(key)
                unique_deps.append(dep)
        
        return unique_deps
    
    def _extract_properties(self) -> None:
        """Extract Maven properties from pom.xml."""
        if self._tree is None:
            return
            
        root = self._tree.getroot()
        
        # Handle namespace-aware and non-namespace XML
        ns = self.MAVEN_NAMESPACE if root.tag.startswith("{") else {}
        prefix = "m:" if ns else ""
        
        # Extract from <properties> section
        props_elem = root.find(f"{prefix}properties", ns)
        if props_elem is not None:
            for prop in props_elem:
                # Remove namespace from tag name
                tag = prop.tag.split("}")[-1] if "}" in prop.tag else prop.tag
                if prop.text:
                    self._properties[tag] = prop.text.strip()
        
        # Extract common project properties
        for prop_name in ["version", "groupId", "artifactId"]:
            elem = root.find(f"{prefix}{prop_name}", ns)
            if elem is not None and elem.text:
                self._properties[f"project.{prop_name}"] = elem.text.strip()
        
        # Extract parent properties
        parent = root.find(f"{prefix}parent", ns)
        if parent is not None:
            for prop_name in ["version", "groupId", "artifactId"]:
                elem = parent.find(f"{prefix}{prop_name}", ns)
                if elem is not None and elem.text:
                    self._properties[f"project.parent.{prop_name}"] = elem.text.strip()
    
    def _resolve_property(self, value: Optional[str]) -> str:
        """Resolve Maven property placeholders like ${property.name}."""
        if not value:
            return ""
        
        pattern = r"\$\{([^}]+)\}"
        
        def replace(match: re.Match) -> str:
            prop_name = match.group(1)
            return self._properties.get(prop_name, match.group(0))
        
        # Resolve multiple levels of properties
        resolved = value
        for _ in range(5):  # Max 5 levels of nesting
            new_resolved = re.sub(pattern, replace, resolved)
            if new_resolved == resolved:
                break
            resolved = new_resolved
        
        return resolved
    
    def _parse_dependencies(self) -> list[Dependency]:
        """Parse direct dependencies from pom.xml."""
        if self._tree is None:
            return []
        
        root = self._tree.getroot()
        dependencies = []
        
        # Handle namespace-aware and non-namespace XML
        ns = self.MAVEN_NAMESPACE if root.tag.startswith("{") else {}
        prefix = "m:" if ns else ""
        
        # Find all dependency elements
        for dep_elem in root.findall(f".//{prefix}dependency", ns):
            group_id_elem = dep_elem.find(f"{prefix}groupId", ns)
            artifact_id_elem = dep_elem.find(f"{prefix}artifactId", ns)
            version_elem = dep_elem.find(f"{prefix}version", ns)
            scope_elem = dep_elem.find(f"{prefix}scope", ns)
            
            if group_id_elem is None or artifact_id_elem is None:
                continue
            
            group_id = self._resolve_property(group_id_elem.text)
            artifact_id = self._resolve_property(artifact_id_elem.text)
            version = self._resolve_property(version_elem.text if version_elem is not None else None)
            scope = scope_elem.text.strip() if scope_elem is not None and scope_elem.text else "compile"
            
            # Skip if version couldn't be resolved
            if not version or version.startswith("${"):
                # Try to get from parent or dependency management
                version = self._resolve_managed_version(group_id, artifact_id)
            
            if version:
                dependencies.append(Dependency(
                    group_id=group_id,
                    artifact_id=artifact_id,
                    version=version,
                    scope=scope,
                ))
        
        return dependencies
    
    def _resolve_managed_version(self, group_id: str, artifact_id: str) -> str:
        """Try to resolve version from dependencyManagement or parent."""
        if self._tree is None:
            return ""
            
        root = self._tree.getroot()
        ns = self.MAVEN_NAMESPACE if root.tag.startswith("{") else {}
        prefix = "m:" if ns else ""
        
        # Check dependencyManagement
        for managed in root.findall(f".//{prefix}dependencyManagement//{prefix}dependency", ns):
            gid = managed.find(f"{prefix}groupId", ns)
            aid = managed.find(f"{prefix}artifactId", ns)
            ver = managed.find(f"{prefix}version", ns)
            
            if gid is not None and aid is not None and ver is not None:
                if gid.text == group_id and aid.text == artifact_id:
                    return self._resolve_property(ver.text)
        
        return ""
    
    def _get_transitive_dependencies(self) -> list[Dependency]:
        """Get transitive dependencies using mvn dependency:tree."""
        try:
            result = subprocess.run(
                ["mvn", "dependency:tree", "-DoutputType=text", "-q"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            if result.returncode != 0:
                return []
            
            return self._parse_dependency_tree(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def _parse_dependency_tree(self, output: str) -> list[Dependency]:
        """Parse mvn dependency:tree output."""
        dependencies = []
        
        # Pattern: groupId:artifactId:packaging:version:scope
        pattern = r"([^:\s]+):([^:\s]+):([^:\s]+):([^:\s]+)(?::([^:\s]+))?"
        
        for line in output.split("\n"):
            # Remove tree characters
            cleaned = re.sub(r"^[\s\|\+\-\\]+", "", line).strip()
            
            match = re.match(pattern, cleaned)
            if match:
                groups = match.groups()
                dependencies.append(Dependency(
                    group_id=groups[0],
                    artifact_id=groups[1],
                    packaging=groups[2],
                    version=groups[3],
                    scope=groups[4] if groups[4] else "compile",
                ))
        
        return dependencies


def parse_pom(project_path: Path) -> list[Dependency]:
    """Convenience function to parse pom.xml.
    
    Args:
        project_path: Path to Maven project
        
    Returns:
        List of dependencies
    """
    parser = PomParser(project_path)
    return parser.parse()
