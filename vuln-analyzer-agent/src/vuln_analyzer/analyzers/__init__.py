"""Vulnerability analyzers."""

from vuln_analyzer.analyzers.base import VulnerabilityAnalyzer
from vuln_analyzer.analyzers.owasp_analyzer import OwaspAnalyzer
from vuln_analyzer.analyzers.nvd_analyzer import NvdAnalyzer
from vuln_analyzer.analyzers.offline_analyzer import OfflineAnalyzer

__all__ = ["VulnerabilityAnalyzer", "OwaspAnalyzer", "NvdAnalyzer", "OfflineAnalyzer"]

# Mend analyzer is optional
try:
    from vuln_analyzer.analyzers.mend_analyzer import MendAnalyzer
    __all__.append("MendAnalyzer")
except ImportError:
    pass
