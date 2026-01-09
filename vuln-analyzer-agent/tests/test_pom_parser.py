"""Tests for POM parser."""

import pytest
from pathlib import Path
from vuln_analyzer.parsers.pom_parser import PomParser


def test_parse_simple_pom(tmp_path):
    """Test parsing a simple pom.xml."""
    pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <groupId>com.example</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <spring.version>3.3.6</spring.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>${spring.version}</version>
        </dependency>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>some-lib</artifactId>
            <version>2.0.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
"""
    pom_path = tmp_path / "pom.xml"
    pom_path.write_text(pom_content)
    
    parser = PomParser(tmp_path)
    deps = parser.parse()
    
    assert len(deps) == 2
    
    # Check first dependency (with property resolution)
    web_dep = next(d for d in deps if d.artifact_id == "spring-boot-starter-web")
    assert web_dep.group_id == "org.springframework.boot"
    assert web_dep.version == "3.3.6"  # Property resolved
    
    # Check second dependency
    lib_dep = next(d for d in deps if d.artifact_id == "some-lib")
    assert lib_dep.group_id == "com.example"
    assert lib_dep.version == "2.0.0"
    assert lib_dep.scope == "test"


def test_parse_pom_not_found(tmp_path):
    """Test error when pom.xml doesn't exist."""
    parser = PomParser(tmp_path)
    
    with pytest.raises(FileNotFoundError):
        parser.parse()


def test_dependency_coordinate():
    """Test Dependency coordinate property."""
    from vuln_analyzer.models import Dependency
    
    dep = Dependency(
        group_id="org.example",
        artifact_id="my-lib",
        version="1.2.3",
    )
    
    assert dep.coordinate == "org.example:my-lib:1.2.3"
    assert dep.gav == dep.coordinate
