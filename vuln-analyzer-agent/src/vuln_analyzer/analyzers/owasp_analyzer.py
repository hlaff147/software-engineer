"""OWASP Dependency-Check analyzer."""

import json
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

from vuln_analyzer.analyzers.base import VulnerabilityAnalyzer
from vuln_analyzer.config import Config
from vuln_analyzer.models import Dependency, Severity, Vulnerability


class OwaspAnalyzer(VulnerabilityAnalyzer):
    """Analyzer using OWASP Dependency-Check."""
    
    DOWNLOAD_URL = "https://github.com/jeremylong/DependencyCheck/releases/download/v10.0.4/dependency-check-10.0.4-release.zip"
    
    def __init__(self, config: Config, project_path: Path):
        """Initialize OWASP analyzer.
        
        Args:
            config: Application configuration
            project_path: Path to the project to analyze
        """
        super().__init__(config)
        self.project_path = project_path
        self._dc_path: Optional[Path] = None
    
    @property
    def name(self) -> str:
        return "OWASP"
    
    def is_available(self) -> bool:
        """Check if dependency-check is available."""
        return self._get_dependency_check_path() is not None
    
    def _get_dependency_check_path(self) -> Optional[Path]:
        """Get path to dependency-check script."""
        if self._dc_path:
            return self._dc_path
        
        # Check config
        if self.config.owasp.path:
            path = Path(self.config.owasp.path)
            if path.exists():
                self._dc_path = path
                return path
        
        # Check in PATH
        try:
            result = subprocess.run(
                ["which", "dependency-check.sh"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                self._dc_path = Path(result.stdout.strip())
                return self._dc_path
        except Exception:
            pass
        
        # Check common locations
        common_paths = [
            Path.home() / ".local" / "share" / "dependency-check" / "bin" / "dependency-check.sh",
            Path("/opt/dependency-check/bin/dependency-check.sh"),
            Path("/usr/local/bin/dependency-check.sh"),
        ]
        
        for path in common_paths:
            if path.exists():
                self._dc_path = path
                return path
        
        # Try to download
        downloaded = self._download_dependency_check()
        if downloaded:
            self._dc_path = downloaded
            return downloaded
        
        return None
    
    def _download_dependency_check(self) -> Optional[Path]:
        """Download OWASP Dependency-Check if not available."""
        install_dir = Path.home() / ".local" / "share" / "dependency-check"
        
        if (install_dir / "bin" / "dependency-check.sh").exists():
            return install_dir / "bin" / "dependency-check.sh"
        
        try:
            install_dir.mkdir(parents=True, exist_ok=True)
            
            with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
                urllib.request.urlretrieve(self.DOWNLOAD_URL, tmp.name)
                
                with zipfile.ZipFile(tmp.name, "r") as zf:
                    zf.extractall(install_dir.parent)
                
                Path(tmp.name).unlink()
            
            script = install_dir / "bin" / "dependency-check.sh"
            if script.exists():
                script.chmod(0o755)
                return script
                
        except Exception:
            pass
        
        return None
    
    def analyze(self, dependencies: list[Dependency]) -> list[Vulnerability]:
        """Run OWASP Dependency-Check and parse results."""
        dc_path = self._get_dependency_check_path()
        if not dc_path:
            return []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "dependency-check-report.json"
            
            cmd = [
                str(dc_path),
                "--scan", str(self.project_path),
                "--format", "JSON",
                "--out", str(output_file),
                "--project", self.project_path.name,
            ]
            
            # Add NVD API key if available
            nvd_key = self.config.owasp.nvd_api_key or self.config.nvd.api_key
            if nvd_key:
                cmd.extend(["--nvdApiKey", nvd_key])
            
            try:
                subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=600,  # 10 minutes
                    check=False,  # Don't raise on non-zero exit
                )
                
                if output_file.exists():
                    return self._parse_report(output_file, dependencies)
            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass
        
        return []
    
    def _parse_report(self, report_path: Path, dependencies: list[Dependency]) -> list[Vulnerability]:
        """Parse OWASP Dependency-Check JSON report."""
        vulnerabilities = []
        
        with open(report_path) as f:
            report = json.load(f)
        
        # Create lookup map for dependencies
        dep_map = {
            f"{d.group_id}:{d.artifact_id}": d
            for d in dependencies
        }
        
        for dep in report.get("dependencies", []):
            vulns = dep.get("vulnerabilities", [])
            
            # Try to match with our dependencies
            file_path = dep.get("filePath", "")
            file_name = dep.get("fileName", "")
            
            matched_dep = None
            for key, d in dep_map.items():
                if d.artifact_id in file_name or d.artifact_id in file_path:
                    matched_dep = d
                    break
            
            if not matched_dep:
                # Create a placeholder dependency
                matched_dep = Dependency(
                    group_id="unknown",
                    artifact_id=file_name.split("-")[0] if file_name else "unknown",
                    version="unknown",
                )
            
            for vuln in vulns:
                cvss_v3 = vuln.get("cvssv3", {})
                cvss_v2 = vuln.get("cvssv2", {})
                
                score = cvss_v3.get("baseScore", 0) or cvss_v2.get("score", 0)
                
                severity_str = vuln.get("severity", "UNKNOWN").upper()
                try:
                    severity = Severity[severity_str]
                except KeyError:
                    severity = Severity.from_cvss(score)
                
                vulnerabilities.append(Vulnerability(
                    id=vuln.get("name", "UNKNOWN"),
                    title=vuln.get("name", "Unknown Vulnerability"),
                    description=vuln.get("description", ""),
                    severity=severity,
                    cvss_score=score,
                    dependency=matched_dep,
                    source=self.name,
                    cwe_ids=[cwe.get("cweId", "") for cwe in vuln.get("cwes", [])],
                    references=[ref.get("url", "") for ref in vuln.get("references", [])],
                ))
        
        return self.filter_suppressed(vulnerabilities)
