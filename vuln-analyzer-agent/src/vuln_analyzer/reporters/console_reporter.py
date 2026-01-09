"""Console reporter with Rich formatting."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from vuln_analyzer.models import AnalysisResult, Severity


class ConsoleReporter:
    """Report vulnerabilities to console with rich formatting."""
    
    SEVERITY_COLORS = {
        Severity.CRITICAL: "bold red",
        Severity.HIGH: "red",
        Severity.MEDIUM: "yellow",
        Severity.LOW: "blue",
        Severity.UNKNOWN: "dim",
    }
    
    def __init__(self):
        self.console = Console()
    
    def report(self, result: AnalysisResult) -> None:
        """Print analysis results to console."""
        self._print_header(result)
        self._print_summary(result)
        
        if result.vulnerabilities:
            self._print_vulnerability_table(result)
        else:
            self.console.print("\n[green]✓ No vulnerabilities found![/green]\n")
        
        if result.fix_suggestions:
            self._print_fix_suggestions(result)
        
        if result.errors:
            self._print_errors(result)
    
    def _print_header(self, result: AnalysisResult) -> None:
        """Print report header."""
        self.console.print()
        self.console.print(Panel.fit(
            f"[bold]Vulnerability Analysis Report[/bold]\n"
            f"Project: {result.project_path}\n"
            f"Scan Duration: {result.scan_duration_seconds:.2f}s\n"
            f"Sources: {', '.join(result.sources_used) or 'None'}",
            title="🔒 Vuln Analyzer",
        ))
    
    def _print_summary(self, result: AnalysisResult) -> None:
        """Print vulnerability summary."""
        summary = Table(show_header=False, box=None)
        summary.add_column("Label", style="bold")
        summary.add_column("Value")
        
        summary.add_row("Dependencies Scanned:", str(len(result.dependencies)))
        summary.add_row("Total Vulnerabilities:", str(result.total_vulnerabilities))
        summary.add_row(
            "Critical:",
            Text(str(result.critical_count), style=self.SEVERITY_COLORS[Severity.CRITICAL])
        )
        summary.add_row(
            "High:",
            Text(str(result.high_count), style=self.SEVERITY_COLORS[Severity.HIGH])
        )
        summary.add_row(
            "Medium:",
            Text(str(result.medium_count), style=self.SEVERITY_COLORS[Severity.MEDIUM])
        )
        summary.add_row(
            "Low:",
            Text(str(result.low_count), style=self.SEVERITY_COLORS[Severity.LOW])
        )
        
        self.console.print(summary)
        self.console.print()
    
    def _print_vulnerability_table(self, result: AnalysisResult) -> None:
        """Print detailed vulnerability table."""
        table = Table(title="Vulnerabilities")
        
        table.add_column("CVE/ID", style="cyan", no_wrap=True)
        table.add_column("Severity", justify="center")
        table.add_column("CVSS", justify="right")
        table.add_column("Dependency", style="yellow")
        table.add_column("Source")
        table.add_column("Fix Version", style="green")
        
        # Sort by severity (critical first)
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.UNKNOWN: 4,
        }
        
        sorted_vulns = sorted(
            result.vulnerabilities,
            key=lambda v: (severity_order[v.severity], -v.cvss_score)
        )
        
        for vuln in sorted_vulns:
            severity_text = Text(
                vuln.severity.value,
                style=self.SEVERITY_COLORS[vuln.severity]
            )
            
            table.add_row(
                vuln.id,
                severity_text,
                f"{vuln.cvss_score:.1f}",
                vuln.dependency.coordinate,
                vuln.source,
                vuln.fixed_version or "-",
            )
        
        self.console.print(table)
        self.console.print()
    
    def _print_fix_suggestions(self, result: AnalysisResult) -> None:
        """Print fix suggestions."""
        self.console.print("[bold]📦 Suggested Fixes:[/bold]")
        
        table = Table()
        table.add_column("Dependency", style="yellow")
        table.add_column("Current", style="red")
        table.add_column("Recommended", style="green")
        table.add_column("Fixes")
        
        for fix in result.fix_suggestions:
            table.add_row(
                f"{fix.dependency.group_id}:{fix.dependency.artifact_id}",
                fix.current_version,
                fix.recommended_version,
                ", ".join(fix.vulnerabilities_fixed[:3]) + 
                (f" (+{len(fix.vulnerabilities_fixed)-3})" if len(fix.vulnerabilities_fixed) > 3 else ""),
            )
        
        self.console.print(table)
        self.console.print()
    
    def _print_errors(self, result: AnalysisResult) -> None:
        """Print any errors encountered."""
        self.console.print("[bold yellow]⚠ Warnings/Errors:[/bold yellow]")
        for error in result.errors:
            self.console.print(f"  • {error}")
        self.console.print()
