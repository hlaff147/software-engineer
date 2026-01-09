"""NVD (National Vulnerability Database) analyzer."""

import time
from typing import Optional

import requests

from vuln_analyzer.analyzers.base import VulnerabilityAnalyzer
from vuln_analyzer.config import Config
from vuln_analyzer.models import Dependency, Severity, Vulnerability


class NvdAnalyzer(VulnerabilityAnalyzer):
    """Analyzer using NVD REST API."""
    
    NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    def __init__(self, config: Config):
        """Initialize NVD analyzer.
        
        Args:
            config: Application configuration
        """
        super().__init__(config)
        self._session = requests.Session()
        
        # Set API key header if available
        if config.nvd.api_key:
            self._session.headers["apiKey"] = config.nvd.api_key
    
    @property
    def name(self) -> str:
        return "NVD"
    
    def is_available(self) -> bool:
        """NVD API is always available (no auth required, just rate limited)."""
        return True
    
    def analyze(self, dependencies: list[Dependency]) -> list[Vulnerability]:
        """Query NVD for vulnerabilities in dependencies."""
        vulnerabilities = []
        
        for dep in dependencies:
            try:
                vulns = self._query_nvd(dep)
                vulnerabilities.extend(vulns)
                
                # Rate limiting: 6 requests per 30 seconds without API key
                # 50 requests per 30 seconds with API key
                if not self.config.nvd.api_key:
                    time.sleep(5)  # Conservative without API key
                else:
                    time.sleep(0.6)  # With API key
                    
            except Exception:
                continue  # Skip on error, try next dependency
        
        return self.filter_suppressed(vulnerabilities)
    
    def _query_nvd(self, dependency: Dependency) -> list[Vulnerability]:
        """Query NVD API for a specific dependency."""
        # Build CPE match string
        # CPE format: cpe:2.3:a:vendor:product:version
        keyword = f"{dependency.group_id}:{dependency.artifact_id}:{dependency.version}"
        
        params = {
            "keywordSearch": f"{dependency.artifact_id} {dependency.version}",
            "resultsPerPage": 50,
        }
        
        try:
            response = self._session.get(
                self.NVD_API_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_response(data, dependency)
            
        except requests.RequestException:
            return []
    
    def _parse_response(self, data: dict, dependency: Dependency) -> list[Vulnerability]:
        """Parse NVD API response."""
        vulnerabilities = []
        
        for item in data.get("vulnerabilities", []):
            cve = item.get("cve", {})
            cve_id = cve.get("id", "UNKNOWN")
            
            # Get description (prefer English)
            descriptions = cve.get("descriptions", [])
            description = ""
            for desc in descriptions:
                if desc.get("lang") == "en":
                    description = desc.get("value", "")
                    break
            if not description and descriptions:
                description = descriptions[0].get("value", "")
            
            # Get CVSS score
            metrics = cve.get("metrics", {})
            cvss_score = 0.0
            severity = Severity.UNKNOWN
            
            # Try CVSS v3.1 first, then v3.0, then v2.0
            for cvss_key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                if cvss_key in metrics and metrics[cvss_key]:
                    cvss_data = metrics[cvss_key][0].get("cvssData", {})
                    cvss_score = cvss_data.get("baseScore", 0.0)
                    
                    severity_str = cvss_data.get("baseSeverity", "UNKNOWN").upper()
                    try:
                        severity = Severity[severity_str]
                    except KeyError:
                        severity = Severity.from_cvss(cvss_score)
                    break
            
            # Get CWE IDs
            cwe_ids = []
            for weakness in cve.get("weaknesses", []):
                for desc in weakness.get("description", []):
                    if desc.get("value", "").startswith("CWE-"):
                        cwe_ids.append(desc["value"])
            
            # Get references
            references = [
                ref.get("url", "")
                for ref in cve.get("references", [])
                if ref.get("url")
            ][:10]  # Limit to 10 references
            
            # Check if this CVE actually affects our dependency version
            # This is a simplified check - could be improved with proper CPE matching
            if self._affects_dependency(cve, dependency):
                vulnerabilities.append(Vulnerability(
                    id=cve_id,
                    title=cve_id,
                    description=description,
                    severity=severity,
                    cvss_score=cvss_score,
                    dependency=dependency,
                    source=self.name,
                    cwe_ids=cwe_ids,
                    references=references,
                    published_date=cve.get("published"),
                ))
        
        return vulnerabilities
    
    def _affects_dependency(self, cve: dict, dependency: Dependency) -> bool:
        """Check if CVE affects the specific dependency version.
        
        This is a simplified check. A full implementation would
        parse CPE match strings and version ranges properly.
        """
        # Check if dependency name appears in CVE description or configurations
        artifact_lower = dependency.artifact_id.lower()
        
        # Check description
        for desc in cve.get("descriptions", []):
            if artifact_lower in desc.get("value", "").lower():
                return True
        
        # Check configurations (CPE matches)
        for config in cve.get("configurations", []):
            for node in config.get("nodes", []):
                for match in node.get("cpeMatch", []):
                    cpe = match.get("criteria", "").lower()
                    if artifact_lower in cpe:
                        return True
        
        return False
