"""Base class for vulnerability analyzers."""

from abc import ABC, abstractmethod

from vuln_analyzer.config import Config
from vuln_analyzer.models import Dependency, Vulnerability


class VulnerabilityAnalyzer(ABC):
    """Abstract base class for vulnerability analyzers."""
    
    def __init__(self, config: Config):
        """Initialize analyzer with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return analyzer name (e.g., 'OWASP', 'Mend', 'NVD')."""
        ...
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this analyzer is available and properly configured.
        
        Returns:
            True if analyzer can be used
        """
        ...
    
    @abstractmethod
    def analyze(self, dependencies: list[Dependency]) -> list[Vulnerability]:
        """Analyze dependencies for vulnerabilities.
        
        Args:
            dependencies: List of dependencies to analyze
            
        Returns:
            List of found vulnerabilities
        """
        ...
    
    def filter_suppressed(self, vulnerabilities: list[Vulnerability]) -> list[Vulnerability]:
        """Remove suppressed vulnerabilities from results.
        
        Args:
            vulnerabilities: List of vulnerabilities
            
        Returns:
            Filtered list without suppressed CVEs
        """
        if not self.config.suppressions:
            return vulnerabilities
        
        suppressed_set = set(self.config.suppressions)
        return [v for v in vulnerabilities if v.id not in suppressed_set]
