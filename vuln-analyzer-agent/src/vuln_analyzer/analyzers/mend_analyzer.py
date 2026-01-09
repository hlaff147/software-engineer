"""Mend.io (formerly WhiteSource) analyzer."""

from typing import Optional

from vuln_analyzer.analyzers.base import VulnerabilityAnalyzer
from vuln_analyzer.config import Config
from vuln_analyzer.models import Dependency, Severity, Vulnerability


class MendAnalyzer(VulnerabilityAnalyzer):
    """Analyzer using Mend.io API via ws-sdk.
    
    Requires ws-sdk package: pip install ws-sdk
    """
    
    def __init__(self, config: Config):
        """Initialize Mend analyzer.
        
        Args:
            config: Application configuration with Mend credentials
        """
        super().__init__(config)
        self._ws_app = None
    
    @property
    def name(self) -> str:
        return "Mend"
    
    def is_available(self) -> bool:
        """Check if Mend SDK is installed and configured."""
        if not self.config.mend.is_configured:
            return False
        
        try:
            from ws_sdk import WS
            return True
        except ImportError:
            return False
    
    def _get_ws_client(self):
        """Get or create Mend WS client."""
        if self._ws_app is not None:
            return self._ws_app
        
        try:
            from ws_sdk import WS
            
            self._ws_app = WS(
                url=self.config.mend.url,
                user_key=self.config.mend.user_key,
                token=self.config.mend.org_token,
            )
            return self._ws_app
        except Exception:
            return None
    
    def analyze(self, dependencies: list[Dependency]) -> list[Vulnerability]:
        """Query Mend for vulnerabilities in dependencies."""
        if not self.is_available():
            return []
        
        ws = self._get_ws_client()
        if ws is None:
            return []
        
        vulnerabilities = []
        
        for dep in dependencies:
            try:
                vulns = self._query_mend(ws, dep)
                vulnerabilities.extend(vulns)
            except Exception:
                continue
        
        return self.filter_suppressed(vulnerabilities)
    
    def _query_mend(self, ws, dependency: Dependency) -> list[Vulnerability]:
        """Query Mend API for vulnerabilities on a specific dependency."""
        vulnerabilities = []
        
        try:
            # Search for library by GAV coordinates
            search_results = ws.get_libraries(
                search_value=f"{dependency.group_id}:{dependency.artifact_id}:{dependency.version}"
            )
            
            if not search_results:
                return []
            
            for lib in search_results:
                lib_vulns = ws.get_library_vulnerabilities(lib.get("keyUuid", ""))
                
                for vuln in lib_vulns:
                    vuln_id = vuln.get("name", "")
                    cvss_score = vuln.get("score", 0.0)
                    
                    # Mend uses its own severity system
                    severity_str = vuln.get("severity", "UNKNOWN").upper()
                    try:
                        severity = Severity[severity_str]
                    except KeyError:
                        severity = Severity.from_cvss(cvss_score)
                    
                    # Get fix version if available
                    fix_version = None
                    fix_info = vuln.get("topFix", {})
                    if fix_info:
                        fix_version = fix_info.get("fixResolution", "")
                    
                    vulnerabilities.append(Vulnerability(
                        id=vuln_id,
                        title=vuln.get("name", vuln_id),
                        description=vuln.get("description", ""),
                        severity=severity,
                        cvss_score=cvss_score,
                        dependency=dependency,
                        source=self.name,
                        cwe_ids=[],  # Mend doesn't always provide CWE
                        references=[vuln.get("url", "")] if vuln.get("url") else [],
                        fixed_version=fix_version,
                        published_date=vuln.get("publishDate"),
                    ))
        except Exception:
            pass
        
        return vulnerabilities
    
    def get_recommended_version(self, dependency: Dependency) -> Optional[str]:
        """Get recommended safe version for a dependency from Mend.
        
        Args:
            dependency: Dependency to check
            
        Returns:
            Recommended version string or None
        """
        if not self.is_available():
            return None
        
        ws = self._get_ws_client()
        if ws is None:
            return None
        
        try:
            search_results = ws.get_libraries(
                search_value=f"{dependency.group_id}:{dependency.artifact_id}:{dependency.version}"
            )
            
            if not search_results:
                return None
            
            lib = search_results[0]
            vulns = ws.get_library_vulnerabilities(lib.get("keyUuid", ""))
            
            # Find the highest fix version mentioned
            fix_versions = []
            for vuln in vulns:
                fix_info = vuln.get("topFix", {})
                if fix_info and fix_info.get("fixResolution"):
                    fix_versions.append(fix_info["fixResolution"])
            
            if fix_versions:
                # Return the highest version (simplified - assumes semantic versioning)
                return max(fix_versions, key=lambda v: [int(x) for x in v.split(".") if x.isdigit()])
            
        except Exception:
            pass
        
        return None
