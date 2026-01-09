"""JSON reporter for CI/CD integration."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from vuln_analyzer.models import AnalysisResult


class JsonReporter:
    """Generate JSON vulnerability reports."""
    
    def report(self, result: AnalysisResult, output_path: Optional[Path] = None) -> str:
        """Generate JSON report.
        
        Args:
            result: Analysis results
            output_path: Optional path to write JSON file
            
        Returns:
            JSON string
        """
        report_data = {
            "project": result.project_path,
            "scan_duration_seconds": result.scan_duration_seconds,
            "sources_used": result.sources_used,
            "summary": {
                "total_dependencies": len(result.dependencies),
                "total_vulnerabilities": result.total_vulnerabilities,
                "critical": result.critical_count,
                "high": result.high_count,
                "medium": result.medium_count,
                "low": result.low_count,
            },
            "dependencies": [
                {
                    "group_id": d.group_id,
                    "artifact_id": d.artifact_id,
                    "version": d.version,
                    "scope": d.scope,
                }
                for d in result.dependencies
            ],
            "vulnerabilities": [
                {
                    "id": v.id,
                    "title": v.title,
                    "description": v.description,
                    "severity": v.severity.value,
                    "cvss_score": v.cvss_score,
                    "dependency": {
                        "group_id": v.dependency.group_id,
                        "artifact_id": v.dependency.artifact_id,
                        "version": v.dependency.version,
                    },
                    "source": v.source,
                    "cwe_ids": v.cwe_ids,
                    "references": v.references,
                    "fixed_version": v.fixed_version,
                    "published_date": v.published_date,
                }
                for v in result.vulnerabilities
            ],
            "fix_suggestions": [
                {
                    "dependency": {
                        "group_id": f.dependency.group_id,
                        "artifact_id": f.dependency.artifact_id,
                    },
                    "current_version": f.current_version,
                    "recommended_version": f.recommended_version,
                    "vulnerabilities_fixed": f.vulnerabilities_fixed,
                    "breaking_change": f.breaking_change,
                    "notes": f.notes,
                }
                for f in result.fix_suggestions
            ],
            "errors": result.errors,
        }
        
        json_str = json.dumps(report_data, indent=2, ensure_ascii=False)
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json_str)
        
        return json_str
