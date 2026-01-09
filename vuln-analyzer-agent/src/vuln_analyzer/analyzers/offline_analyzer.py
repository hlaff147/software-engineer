"""Offline vulnerability database for known Java CVEs."""

from vuln_analyzer.analyzers.base import VulnerabilityAnalyzer
from vuln_analyzer.config import Config
from vuln_analyzer.models import Dependency, Severity, Vulnerability


# Known vulnerabilities database - curated list of well-known Java CVEs
KNOWN_VULNERABILITIES = {
    # Log4j - Log4Shell
    ("org.apache.logging.log4j", "log4j-core"): [
        {
            "id": "CVE-2021-44228",
            "title": "Log4Shell - Apache Log4j2 Remote Code Execution",
            "description": "Apache Log4j2 <=2.14.1 JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers.",
            "severity": Severity.CRITICAL,
            "cvss_score": 10.0,
            "affected_versions": ["2.0", "2.14.1"],  # min, max
            "fixed_version": "2.17.1",
            "cwe_ids": ["CWE-502", "CWE-400", "CWE-20"],
        },
        {
            "id": "CVE-2021-45046",
            "title": "Log4j2 Thread Context Lookup Pattern RCE",
            "description": "It was found that the fix to address CVE-2021-44228 in Apache Log4j 2.15.0 was incomplete in certain non-default configurations.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.0,
            "affected_versions": ["2.0", "2.16.0"],
            "fixed_version": "2.17.0",
            "cwe_ids": ["CWE-502"],
        },
        {
            "id": "CVE-2021-45105",
            "title": "Log4j2 Infinite Recursion DoS",
            "description": "Apache Log4j2 versions 2.0-alpha1 through 2.16.0 did not protect from uncontrolled recursion from self-referential lookups.",
            "severity": Severity.HIGH,
            "cvss_score": 7.5,
            "affected_versions": ["2.0", "2.16.0"],
            "fixed_version": "2.17.0",
            "cwe_ids": ["CWE-674"],
        },
    ],
    # Spring Framework - Spring4Shell
    ("org.springframework", "spring-beans"): [
        {
            "id": "CVE-2022-22965",
            "title": "Spring4Shell - Spring Framework RCE via Data Binding",
            "description": "A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution (RCE) via data binding.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.8,
            "affected_versions": ["5.0.0", "5.3.17"],
            "fixed_version": "5.3.18",
            "cwe_ids": ["CWE-94"],
        },
    ],
    ("org.springframework", "spring-webmvc"): [
        {
            "id": "CVE-2022-22965",
            "title": "Spring4Shell - Spring Framework RCE via Data Binding",
            "description": "A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution (RCE) via data binding.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.8,
            "affected_versions": ["5.0.0", "5.3.17"],
            "fixed_version": "5.3.18",
            "cwe_ids": ["CWE-94"],
        },
    ],
    # Jackson databind
    ("com.fasterxml.jackson.core", "jackson-databind"): [
        {
            "id": "CVE-2019-12384",
            "title": "Jackson Databind Polymorphic Typing Deserialization RCE",
            "description": "FasterXML jackson-databind allows remote attackers to execute arbitrary code via ehcache 'net.sf.ehcache.transaction.manager.selector.GenericJndiSelector'.",
            "severity": Severity.HIGH,
            "cvss_score": 7.5,
            "affected_versions": ["2.0.0", "2.9.9"],
            "fixed_version": "2.9.10",
            "cwe_ids": ["CWE-502"],
        },
        {
            "id": "CVE-2019-14540",
            "title": "Jackson Databind SSRF via HikariConfig",
            "description": "FasterXML jackson-databind through 2.9.9.3 allows server-side request forgery.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.8,
            "affected_versions": ["2.0.0", "2.9.9.3"],
            "fixed_version": "2.9.10",
            "cwe_ids": ["CWE-918"],
        },
    ],
    # Commons Collections
    ("commons-collections", "commons-collections"): [
        {
            "id": "CVE-2015-6420",
            "title": "Apache Commons Collections Deserialization RCE",
            "description": "The InvokerTransformer class in Apache Commons Collections allows remote attackers to execute arbitrary Java functions via a serialized object.",
            "severity": Severity.HIGH,
            "cvss_score": 7.5,
            "affected_versions": ["3.0", "3.2.1"],
            "fixed_version": "3.2.2",
            "cwe_ids": ["CWE-502"],
        },
    ],
    # Snakeyaml
    ("org.yaml", "snakeyaml"): [
        {
            "id": "CVE-2022-1471",
            "title": "SnakeYAML Constructor Deserialization RCE",
            "description": "SnakeYAML's Constructor() class does not restrict types which can be instantiated during deserialization, allowing remote code execution.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.8,
            "affected_versions": ["1.0", "1.33"],
            "fixed_version": "2.0",
            "cwe_ids": ["CWE-502"],
        },
    ],
    # Gson
    ("com.google.code.gson", "gson"): [
        {
            "id": "CVE-2022-25647",
            "title": "Gson Denial of Service via Deep Nesting",
            "description": "The package com.google.code.gson before 2.8.9 is vulnerable to Deserialization of Untrusted Data via the writeReplace() method in internal classes.",
            "severity": Severity.MEDIUM,
            "cvss_score": 6.5,
            "affected_versions": ["2.0", "2.8.8"],
            "fixed_version": "2.8.9",
            "cwe_ids": ["CWE-502"],
        },
    ],
    # Hibernate
    ("org.hibernate", "hibernate-core"): [
        {
            "id": "CVE-2020-25638",
            "title": "Hibernate SQL Injection",
            "description": "A flaw was found in hibernate-core allowing SQL injection with update or delete statements, enabling modification of records.",
            "severity": Severity.HIGH,
            "cvss_score": 7.4,
            "affected_versions": ["5.0.0", "5.4.23"],
            "fixed_version": "5.4.24.Final",
            "cwe_ids": ["CWE-89"],
        },
    ],
    # Apache HttpClient
    ("org.apache.httpcomponents", "httpclient"): [
        {
            "id": "CVE-2020-13956",
            "title": "Apache HttpClient Incorrect Input Validation",
            "description": "Apache HttpClient 4.5.x before 4.5.13 and 5.x before 5.0.3 can misinterpret malformed authority component in request URIs.",
            "severity": Severity.MEDIUM,
            "cvss_score": 5.3,
            "affected_versions": ["4.5.0", "4.5.12"],
            "fixed_version": "4.5.13",
            "cwe_ids": ["CWE-20"],
        },
    ],
    # Netty
    ("io.netty", "netty-all"): [
        {
            "id": "CVE-2021-21290",
            "title": "Netty Insecure Temp File Creation",
            "description": "Netty creates temporary files with insecure permissions, allowing local system info disclosure.",
            "severity": Severity.MEDIUM,
            "cvss_score": 5.5,
            "affected_versions": ["4.0.0", "4.1.58"],
            "fixed_version": "4.1.59.Final",
            "cwe_ids": ["CWE-378"],
        },
        {
            "id": "CVE-2021-21295",
            "title": "Netty HTTP Request Smuggling",
            "description": "Netty is vulnerable to HTTP request smuggling via Content-Length and Transfer-Encoding headers.",
            "severity": Severity.MEDIUM,
            "cvss_score": 5.3,
            "affected_versions": ["4.0.0", "4.1.59"],
            "fixed_version": "4.1.60.Final",
            "cwe_ids": ["CWE-444"],
        },
    ],
    # Guava
    ("com.google.guava", "guava"): [
        {
            "id": "CVE-2020-8908",
            "title": "Guava Temporary Directory Info Disclosure",
            "description": "A temp directory creation vulnerability exists in Guava that allows local users to access temporary data.",
            "severity": Severity.LOW,
            "cvss_score": 3.3,
            "affected_versions": ["1.0", "29.0"],
            "fixed_version": "30.0-jre",
            "cwe_ids": ["CWE-732"],
        },
    ],
    # Commons IO
    ("commons-io", "commons-io"): [
        {
            "id": "CVE-2021-29425",
            "title": "Apache Commons IO Path Traversal",
            "description": "In Apache Commons IO before 2.7, when invoking the method FileNameUtils.normalize with an improper input string, the result would be the same input.",
            "severity": Severity.HIGH,
            "cvss_score": 7.5,
            "affected_versions": ["1.0", "2.6"],
            "fixed_version": "2.7",
            "cwe_ids": ["CWE-22"],
        },
    ],
    # Bouncy Castle
    ("org.bouncycastle", "bcprov-jdk15on"): [
        {
            "id": "CVE-2020-28052",
            "title": "Bouncy Castle LDAP Injection",
            "description": "An issue was discovered in Legion of the Bouncy Castle BC Java 1.65 and 1.66 affecting OpenBSDBcrypt password checking.",
            "severity": Severity.HIGH,
            "cvss_score": 8.1,
            "affected_versions": ["1.60", "1.66"],
            "fixed_version": "1.67",
            "cwe_ids": ["CWE-287"],
        },
    ],
    # PostgreSQL JDBC
    ("org.postgresql", "postgresql"): [
        {
            "id": "CVE-2022-26520",
            "title": "PostgreSQL JDBC Driver Path Traversal",
            "description": "The JDBC driver allows code execution through the loggerFile and loggerLevel connection properties.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.8,
            "affected_versions": ["42.1.0", "42.3.2"],
            "fixed_version": "42.3.3",
            "cwe_ids": ["CWE-22"],
        },
        {
            "id": "CVE-2022-21724",
            "title": "PostgreSQL JDBC Driver Arbitrary Code Execution",
            "description": "pgjdbc is the offical PostgreSQL JDBC Driver. A security hole was found in the pgjdbc driver before 42.3.3.",
            "severity": Severity.CRITICAL,
            "cvss_score": 9.8,
            "affected_versions": ["42.0.0", "42.3.2"],
            "fixed_version": "42.3.3",
            "cwe_ids": ["CWE-665"],
        },
    ],
}


class OfflineAnalyzer(VulnerabilityAnalyzer):
    """Analyzer using offline curated vulnerability database.
    
    Uses a local database of well-known Java vulnerabilities for fast,
    reliable detection without network calls.
    """
    
    def __init__(self, config: Config):
        super().__init__(config)
    
    @property
    def name(self) -> str:
        return "Offline-DB"
    
    def is_available(self) -> bool:
        return True
    
    def analyze(self, dependencies: list[Dependency]) -> list[Vulnerability]:
        """Check dependencies against known vulnerability database."""
        vulnerabilities = []
        
        for dep in dependencies:
            key = (dep.group_id, dep.artifact_id)
            
            if key in KNOWN_VULNERABILITIES:
                for vuln_info in KNOWN_VULNERABILITIES[key]:
                    if self._version_in_range(dep.version, vuln_info["affected_versions"]):
                        vulnerabilities.append(Vulnerability(
                            id=vuln_info["id"],
                            title=vuln_info["title"],
                            description=vuln_info["description"],
                            severity=vuln_info["severity"],
                            cvss_score=vuln_info["cvss_score"],
                            dependency=dep,
                            source=self.name,
                            cwe_ids=vuln_info.get("cwe_ids", []),
                            fixed_version=vuln_info.get("fixed_version"),
                        ))
        
        return self.filter_suppressed(vulnerabilities)
    
    def _version_in_range(self, version: str, range_tuple: list[str]) -> bool:
        """Check if version is within affected range."""
        if len(range_tuple) != 2:
            return False
        
        min_ver, max_ver = range_tuple
        
        try:
            ver_parts = self._parse_version(version)
            min_parts = self._parse_version(min_ver)
            max_parts = self._parse_version(max_ver)
            
            return min_parts <= ver_parts <= max_parts
        except Exception:
            # If version parsing fails, be conservative and report
            return True
    
    def _parse_version(self, version: str) -> tuple:
        """Parse version string into comparable tuple."""
        import re
        # Remove suffixes like -Final, -jre, etc.
        clean = re.sub(r'[-.]?(Final|jre|android|RELEASE)$', '', version, flags=re.IGNORECASE)
        # Extract numeric parts
        parts = re.findall(r'\d+', clean)
        return tuple(int(p) for p in parts)
