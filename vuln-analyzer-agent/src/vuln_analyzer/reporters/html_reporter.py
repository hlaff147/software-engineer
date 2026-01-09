"""HTML reporter with interactive visualization."""

from pathlib import Path
from typing import Optional

from jinja2 import Template

from vuln_analyzer.models import AnalysisResult, Severity


class HtmlReporter:
    """Generate standalone HTML vulnerability reports."""
    
    HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerability Report - {{ project_name }}</title>
    <style>
        :root {
            --critical: #dc2626;
            --high: #ea580c;
            --medium: #ca8a04;
            --low: #2563eb;
            --bg: #0f172a;
            --card: #1e293b;
            --text: #e2e8f0;
            --border: #334155;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }
        
        .container { max-width: 1400px; margin: 0 auto; }
        
        header {
            background: var(--card);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
        }
        
        h1 { font-size: 1.75rem; margin-bottom: 1rem; }
        
        .meta { color: #94a3b8; font-size: 0.875rem; }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--card);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid var(--border);
        }
        
        .stat-card.critical { border-left: 4px solid var(--critical); }
        .stat-card.high { border-left: 4px solid var(--high); }
        .stat-card.medium { border-left: 4px solid var(--medium); }
        .stat-card.low { border-left: 4px solid var(--low); }
        
        .stat-value { font-size: 2.5rem; font-weight: bold; }
        .stat-label { color: #94a3b8; font-size: 0.875rem; }
        
        .critical .stat-value { color: var(--critical); }
        .high .stat-value { color: var(--high); }
        .medium .stat-value { color: var(--medium); }
        .low .stat-value { color: var(--low); }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--card);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        
        th, td { padding: 1rem; text-align: left; }
        th { background: rgba(0,0,0,0.3); font-weight: 600; }
        tr:hover { background: rgba(255,255,255,0.05); }
        
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-critical { background: rgba(220, 38, 38, 0.2); color: var(--critical); }
        .badge-high { background: rgba(234, 88, 12, 0.2); color: var(--high); }
        .badge-medium { background: rgba(202, 138, 4, 0.2); color: var(--medium); }
        .badge-low { background: rgba(37, 99, 235, 0.2); color: var(--low); }
        
        .cve-link { color: #60a5fa; text-decoration: none; }
        .cve-link:hover { text-decoration: underline; }
        
        .fix { color: #22c55e; font-weight: 500; }
        
        .section-title { 
            font-size: 1.25rem; 
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border);
        }
        
        .no-vulns {
            text-align: center;
            padding: 3rem;
            background: var(--card);
            border-radius: 12px;
            border: 1px solid var(--border);
        }
        
        .no-vulns-icon { font-size: 3rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 Vulnerability Analysis Report</h1>
            <div class="meta">
                <strong>Project:</strong> {{ project_path }}<br>
                <strong>Scan Duration:</strong> {{ "%.2f"|format(scan_duration) }}s<br>
                <strong>Sources:</strong> {{ sources | join(', ') or 'None' }}<br>
                <strong>Generated:</strong> {{ timestamp }}
            </div>
        </header>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">{{ total_deps }}</div>
                <div class="stat-label">Dependencies</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value">{{ critical }}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card high">
                <div class="stat-value">{{ high }}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-value">{{ medium }}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card low">
                <div class="stat-value">{{ low }}</div>
                <div class="stat-label">Low</div>
            </div>
        </div>
        
        {% if vulnerabilities %}
        <h2 class="section-title">Vulnerabilities ({{ vulnerabilities | length }})</h2>
        <table>
            <thead>
                <tr>
                    <th>CVE/ID</th>
                    <th>Severity</th>
                    <th>CVSS</th>
                    <th>Dependency</th>
                    <th>Source</th>
                    <th>Fix Version</th>
                </tr>
            </thead>
            <tbody>
                {% for v in vulnerabilities %}
                <tr>
                    <td>
                        <a href="https://nvd.nist.gov/vuln/detail/{{ v.id }}" 
                           target="_blank" class="cve-link">{{ v.id }}</a>
                    </td>
                    <td><span class="badge badge-{{ v.severity | lower }}">{{ v.severity }}</span></td>
                    <td>{{ "%.1f"|format(v.cvss_score) }}</td>
                    <td>{{ v.dependency }}</td>
                    <td>{{ v.source }}</td>
                    <td>{% if v.fixed_version %}<span class="fix">{{ v.fixed_version }}</span>{% else %}-{% endif %}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="no-vulns">
            <div class="no-vulns-icon">✅</div>
            <h2>No Vulnerabilities Found!</h2>
            <p>All {{ total_deps }} dependencies passed security checks.</p>
        </div>
        {% endif %}
        
        {% if fix_suggestions %}
        <h2 class="section-title">Recommended Fixes</h2>
        <table>
            <thead>
                <tr>
                    <th>Dependency</th>
                    <th>Current Version</th>
                    <th>Recommended Version</th>
                    <th>CVEs Fixed</th>
                </tr>
            </thead>
            <tbody>
                {% for fix in fix_suggestions %}
                <tr>
                    <td>{{ fix.dependency }}</td>
                    <td style="color: var(--critical);">{{ fix.current }}</td>
                    <td class="fix">{{ fix.recommended }}</td>
                    <td>{{ fix.cves }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}
    </div>
</body>
</html>
"""
    
    def report(self, result: AnalysisResult, output_path: Optional[Path] = None) -> str:
        """Generate HTML report.
        
        Args:
            result: Analysis results
            output_path: Optional path to write HTML file
            
        Returns:
            HTML string
        """
        from datetime import datetime
        
        template = Template(self.HTML_TEMPLATE)
        
        # Prepare vulnerability data
        vulnerabilities = [
            {
                "id": v.id,
                "severity": v.severity.value,
                "cvss_score": v.cvss_score,
                "dependency": v.dependency.coordinate,
                "source": v.source,
                "fixed_version": v.fixed_version,
            }
            for v in sorted(
                result.vulnerabilities,
                key=lambda x: (-x.cvss_score, x.id)
            )
        ]
        
        # Prepare fix suggestions
        fix_suggestions = [
            {
                "dependency": f"{f.dependency.group_id}:{f.dependency.artifact_id}",
                "current": f.current_version,
                "recommended": f.recommended_version,
                "cves": ", ".join(f.vulnerabilities_fixed[:5]) + 
                       (f" (+{len(f.vulnerabilities_fixed)-5})" if len(f.vulnerabilities_fixed) > 5 else ""),
            }
            for f in result.fix_suggestions
        ]
        
        html = template.render(
            project_name=Path(result.project_path).name,
            project_path=result.project_path,
            scan_duration=result.scan_duration_seconds,
            sources=result.sources_used,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_deps=len(result.dependencies),
            critical=result.critical_count,
            high=result.high_count,
            medium=result.medium_count,
            low=result.low_count,
            vulnerabilities=vulnerabilities,
            fix_suggestions=fix_suggestions,
        )
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)
        
        return html
