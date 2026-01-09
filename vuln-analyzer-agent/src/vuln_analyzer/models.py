"""Data models for vulnerability analysis."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Vulnerability severity levels."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"
    
    @classmethod
    def from_cvss(cls, score: float) -> "Severity":
        """Convert CVSS score to severity level."""
        if score >= 9.0:
            return cls.CRITICAL
        elif score >= 7.0:
            return cls.HIGH
        elif score >= 4.0:
            return cls.MEDIUM
        elif score > 0:
            return cls.LOW
        return cls.UNKNOWN


@dataclass
class Dependency:
    """Represents a Maven dependency."""
    group_id: str
    artifact_id: str
    version: str
    scope: str = "compile"
    packaging: str = "jar"
    
    @property
    def coordinate(self) -> str:
        """Return Maven coordinate string."""
        return f"{self.group_id}:{self.artifact_id}:{self.version}"
    
    @property
    def gav(self) -> str:
        """Return GAV (Group:Artifact:Version) format."""
        return self.coordinate
    
    def __hash__(self) -> int:
        return hash((self.group_id, self.artifact_id, self.version))


@dataclass
class Vulnerability:
    """Represents a security vulnerability."""
    id: str  # CVE-XXXX-XXXXX or WS-XXXX
    title: str
    description: str
    severity: Severity
    cvss_score: float
    dependency: Dependency
    source: str  # "OWASP", "Mend", "NVD"
    cwe_ids: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    fixed_version: Optional[str] = None
    published_date: Optional[str] = None
    
    @property
    def is_critical(self) -> bool:
        return self.severity == Severity.CRITICAL
    
    @property
    def is_high_or_critical(self) -> bool:
        return self.severity in (Severity.CRITICAL, Severity.HIGH)


@dataclass
class FixSuggestion:
    """Represents a suggested fix for a vulnerability."""
    dependency: Dependency
    current_version: str
    recommended_version: str
    vulnerabilities_fixed: list[str]  # List of CVE IDs
    breaking_change: bool = False
    notes: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result for a project."""
    project_path: str
    dependencies: list[Dependency]
    vulnerabilities: list[Vulnerability]
    fix_suggestions: list[FixSuggestion]
    scan_duration_seconds: float = 0.0
    sources_used: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    
    @property
    def total_vulnerabilities(self) -> int:
        return len(self.vulnerabilities)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.CRITICAL)
    
    @property
    def high_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.HIGH)
    
    @property
    def medium_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.MEDIUM)
    
    @property
    def low_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.LOW)
    
    def get_by_severity(self, severity: Severity) -> list[Vulnerability]:
        return [v for v in self.vulnerabilities if v.severity == severity]
    
    def has_high_severity(self, threshold: float = 7.0) -> bool:
        """Check if any vulnerability exceeds CVSS threshold."""
        return any(v.cvss_score >= threshold for v in self.vulnerabilities)
