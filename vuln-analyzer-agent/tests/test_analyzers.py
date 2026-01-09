"""Tests for analyzers."""

import pytest
from vuln_analyzer.models import Dependency, Severity, Vulnerability
from vuln_analyzer.analyzers.nvd_analyzer import NvdAnalyzer
from vuln_analyzer.config import Config


def test_severity_from_cvss():
    """Test CVSS score to severity conversion."""
    assert Severity.from_cvss(9.5) == Severity.CRITICAL
    assert Severity.from_cvss(9.0) == Severity.CRITICAL
    assert Severity.from_cvss(8.5) == Severity.HIGH
    assert Severity.from_cvss(7.0) == Severity.HIGH
    assert Severity.from_cvss(5.0) == Severity.MEDIUM
    assert Severity.from_cvss(4.0) == Severity.MEDIUM
    assert Severity.from_cvss(2.0) == Severity.LOW
    assert Severity.from_cvss(0.0) == Severity.UNKNOWN


def test_vulnerability_properties():
    """Test Vulnerability model properties."""
    dep = Dependency("org.example", "lib", "1.0.0")
    
    vuln = Vulnerability(
        id="CVE-2024-12345",
        title="Test Vulnerability",
        description="A test vulnerability",
        severity=Severity.CRITICAL,
        cvss_score=9.8,
        dependency=dep,
        source="Test",
    )
    
    assert vuln.is_critical
    assert vuln.is_high_or_critical
    
    vuln.severity = Severity.HIGH
    assert not vuln.is_critical
    assert vuln.is_high_or_critical
    
    vuln.severity = Severity.MEDIUM
    assert not vuln.is_high_or_critical


def test_nvd_analyzer_available():
    """Test NVD analyzer is always available."""
    config = Config()
    analyzer = NvdAnalyzer(config)
    
    assert analyzer.is_available()
    assert analyzer.name == "NVD"


def test_suppression_filter():
    """Test vulnerability suppression filter."""
    config = Config(suppressions=["CVE-2024-12345", "CVE-2024-67890"])
    analyzer = NvdAnalyzer(config)
    
    dep = Dependency("org.example", "lib", "1.0.0")
    vulns = [
        Vulnerability(
            id="CVE-2024-12345",
            title="Suppressed",
            description="",
            severity=Severity.HIGH,
            cvss_score=8.0,
            dependency=dep,
            source="Test",
        ),
        Vulnerability(
            id="CVE-2024-99999",
            title="Not Suppressed",
            description="",
            severity=Severity.MEDIUM,
            cvss_score=5.0,
            dependency=dep,
            source="Test",
        ),
    ]
    
    filtered = analyzer.filter_suppressed(vulns)
    
    assert len(filtered) == 1
    assert filtered[0].id == "CVE-2024-99999"
