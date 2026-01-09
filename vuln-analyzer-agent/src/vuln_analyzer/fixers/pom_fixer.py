"""POM fixer for automatic vulnerability remediation."""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from lxml import etree

from vuln_analyzer.models import AnalysisResult, Dependency, FixSuggestion


class PomFixer:
    """Automatically fix vulnerabilities by updating pom.xml versions."""
    
    MAVEN_CENTRAL_API = "https://search.maven.org/solrsearch/select"
    
    def __init__(self, project_path: Path):
        """Initialize fixer.
        
        Args:
            project_path: Path to Maven project root
        """
        self.project_path = Path(project_path)
        self.pom_path = self.project_path / "pom.xml"
        self._session = requests.Session()
    
    def generate_fixes(self, result: AnalysisResult) -> list[FixSuggestion]:
        """Generate fix suggestions for vulnerabilities.
        
        Args:
            result: Analysis result with vulnerabilities
            
        Returns:
            List of fix suggestions
        """
        suggestions = []
        
        # Group vulnerabilities by dependency
        vuln_by_dep: dict[str, list] = {}
        for vuln in result.vulnerabilities:
            key = vuln.dependency.gav
            if key not in vuln_by_dep:
                vuln_by_dep[key] = []
            vuln_by_dep[key].append(vuln)
        
        for gav, vulns in vuln_by_dep.items():
            dep = vulns[0].dependency
            
            # Try to find a fix version
            # First check if any vulnerability has a fix version
            fix_version = None
            for vuln in vulns:
                if vuln.fixed_version:
                    if not fix_version or self._is_higher_version(vuln.fixed_version, fix_version):
                        fix_version = vuln.fixed_version
            
            # If no fix version from analyzers, query Maven Central
            if not fix_version:
                fix_version = self._get_latest_version(dep)
            
            if fix_version and fix_version != dep.version:
                suggestions.append(FixSuggestion(
                    dependency=dep,
                    current_version=dep.version,
                    recommended_version=fix_version,
                    vulnerabilities_fixed=[v.id for v in vulns],
                    breaking_change=self._is_major_version_change(dep.version, fix_version),
                    notes=self._generate_notes(dep.version, fix_version),
                ))
        
        return suggestions
    
    def apply_fixes(
        self, 
        fixes: list[FixSuggestion], 
        dry_run: bool = True,
        backup: bool = True,
    ) -> dict[str, str]:
        """Apply fixes to pom.xml.
        
        Args:
            fixes: List of fixes to apply
            dry_run: If True, don't actually modify the file
            backup: If True, create backup before modifying
            
        Returns:
            Dict mapping artifact ID to new version
        """
        if not self.pom_path.exists():
            raise FileNotFoundError(f"pom.xml not found at {self.pom_path}")
        
        # Read current content
        content = self.pom_path.read_text()
        original_content = content
        
        applied = {}
        
        for fix in fixes:
            new_content = self._apply_fix(content, fix)
            if new_content != content:
                content = new_content
                applied[fix.dependency.artifact_id] = fix.recommended_version
        
        if not dry_run and content != original_content:
            # Create backup
            if backup:
                backup_path = self.pom_path.with_suffix(
                    f".xml.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                shutil.copy2(self.pom_path, backup_path)
            
            # Write updated content
            self.pom_path.write_text(content)
        
        return applied
    
    def _apply_fix(self, content: str, fix: FixSuggestion) -> str:
        """Apply a single fix to POM content.
        
        Args:
            content: Current pom.xml content
            fix: Fix to apply
            
        Returns:
            Updated content
        """
        dep = fix.dependency
        
        # Pattern to match the dependency block
        # Handle both with and without namespace
        patterns = [
            # Without namespace
            rf'(<dependency>\s*'
            rf'<groupId>\s*{re.escape(dep.group_id)}\s*</groupId>\s*'
            rf'<artifactId>\s*{re.escape(dep.artifact_id)}\s*</artifactId>\s*'
            rf'<version>)\s*{re.escape(dep.version)}\s*(</version>)',
            
            # With version as property reference
            rf'(<dependency>\s*'
            rf'<groupId>\s*{re.escape(dep.group_id)}\s*</groupId>\s*'
            rf'<artifactId>\s*{re.escape(dep.artifact_id)}\s*</artifactId>\s*'
            rf'<version>)\s*\$\{{[^}}]+\}}\s*(</version>)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                # Replace version
                new_block = f"{match.group(1)}{fix.recommended_version}{match.group(2)}"
                content = content[:match.start()] + new_block + content[match.end():]
                break
        
        # Also check properties section for version properties
        prop_pattern = rf'(<{re.escape(dep.artifact_id)}\.version>)\s*{re.escape(dep.version)}\s*(</{re.escape(dep.artifact_id)}\.version>)'
        content = re.sub(
            prop_pattern,
            f"\\g<1>{fix.recommended_version}\\g<2>",
            content,
            flags=re.IGNORECASE,
        )
        
        return content
    
    def _get_latest_version(self, dep: Dependency) -> Optional[str]:
        """Query Maven Central for latest version.
        
        Args:
            dep: Dependency to query
            
        Returns:
            Latest version or None
        """
        try:
            response = self._session.get(
                self.MAVEN_CENTRAL_API,
                params={
                    "q": f"g:{dep.group_id} AND a:{dep.artifact_id}",
                    "rows": 10,
                    "wt": "json",
                    "core": "gav",
                },
                timeout=10,
            )
            response.raise_for_status()
            
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            
            if docs:
                # Filter to stable versions (no alpha, beta, RC, etc.)
                stable_versions = [
                    d["v"] for d in docs 
                    if not any(x in d["v"].lower() for x in ["alpha", "beta", "rc", "snapshot", "m1", "m2"])
                ]
                
                if stable_versions:
                    return stable_versions[0]
                return docs[0]["v"]
                
        except Exception:
            pass
        
        return None
    
    def _is_higher_version(self, v1: str, v2: str) -> bool:
        """Check if v1 is higher than v2 (simplified)."""
        try:
            parts1 = [int(x) for x in re.findall(r'\d+', v1)]
            parts2 = [int(x) for x in re.findall(r'\d+', v2)]
            return parts1 > parts2
        except Exception:
            return False
    
    def _is_major_version_change(self, old: str, new: str) -> bool:
        """Check if this is a major version change."""
        try:
            old_major = int(re.findall(r'\d+', old)[0])
            new_major = int(re.findall(r'\d+', new)[0])
            return new_major > old_major
        except Exception:
            return False
    
    def _generate_notes(self, old: str, new: str) -> str:
        """Generate notes about the version change."""
        if self._is_major_version_change(old, new):
            return "Major version upgrade - review changelog for breaking changes"
        return ""
