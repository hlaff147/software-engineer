"""CLI entry point for vulnerability analyzer."""

import sys
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from vuln_analyzer import __version__
from vuln_analyzer.config import Config
from vuln_analyzer.models import AnalysisResult
from vuln_analyzer.parsers.pom_parser import PomParser
from vuln_analyzer.analyzers.owasp_analyzer import OwaspAnalyzer
from vuln_analyzer.analyzers.nvd_analyzer import NvdAnalyzer
from vuln_analyzer.analyzers.offline_analyzer import OfflineAnalyzer
from vuln_analyzer.reporters.console_reporter import ConsoleReporter
from vuln_analyzer.reporters.json_reporter import JsonReporter
from vuln_analyzer.reporters.html_reporter import HtmlReporter
from vuln_analyzer.fixers.pom_fixer import PomFixer

app = typer.Typer(
    name="vuln-analyzer",
    help="Analyze and fix vulnerabilities in Java Spring Maven projects.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"vuln-analyzer version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True,
        help="Show version and exit.",
    ),
):
    """Vulnerability Analyzer Agent for Java Spring Projects."""
    pass


@app.command()
def scan(
    project_path: Path = typer.Argument(
        ...,
        help="Path to Maven project (containing pom.xml)",
        exists=True,
        dir_okay=True,
        file_okay=False,
    ),
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c",
        help="Path to configuration file",
    ),
    use_mend: bool = typer.Option(
        False, "--mend",
        help="Enable Mend.io analysis (requires credentials)",
    ),
    use_owasp: bool = typer.Option(
        True, "--owasp/--no-owasp",
        help="Enable OWASP Dependency-Check analysis",
    ),
    use_nvd: bool = typer.Option(
        True, "--nvd/--no-nvd",  
        help="Enable NVD direct API analysis",
    ),
    output_format: str = typer.Option(
        "console", "--format", "-f",
        help="Output format: console, json, html",
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output file path (for json/html formats)",
    ),
    fail_on_cvss: Optional[float] = typer.Option(
        None, "--fail-on-cvss",
        help="Exit with error if any vulnerability has CVSS >= this value",
    ),
):
    """Scan a Maven project for vulnerabilities."""
    start_time = time.time()
    
    # Load configuration
    config = Config.load(config_file)
    
    if fail_on_cvss is not None:
        config.thresholds.fail_on_cvss = fail_on_cvss
    
    console.print(f"\n🔍 Scanning [bold]{project_path}[/bold]...\n")
    
    # Parse dependencies
    try:
        parser = PomParser(project_path)
        dependencies = parser.parse()
        console.print(f"  Found [cyan]{len(dependencies)}[/cyan] dependencies")
    except Exception as e:
        console.print(f"[red]Error parsing pom.xml: {e}[/red]")
        raise typer.Exit(1)
    
    # Initialize result
    result = AnalysisResult(
        project_path=str(project_path),
        dependencies=dependencies,
        vulnerabilities=[],
        fix_suggestions=[],
    )
    
    errors = []
    
    # Run offline analyzer first (fast, local database)
    console.print("  Checking offline vulnerability database...")
    try:
        offline = OfflineAnalyzer(config)
        vulns = offline.analyze(dependencies)
        result.vulnerabilities.extend(vulns)
        result.sources_used.append("Offline-DB")
        console.print(f"    Found [yellow]{len(vulns)}[/yellow] known vulnerabilities")
    except Exception as e:
        errors.append(f"Offline DB error: {e}")
    
    # Run additional analyzers
    if use_owasp:
        console.print("  Running OWASP Dependency-Check...")
        try:
            owasp = OwaspAnalyzer(config, project_path)
            if owasp.is_available():
                vulns = owasp.analyze(dependencies)
                existing_ids = {v.id for v in result.vulnerabilities}
                new_vulns = [v for v in vulns if v.id not in existing_ids]
                result.vulnerabilities.extend(new_vulns)
                result.sources_used.append("OWASP")
                console.print(f"    Found [yellow]{len(new_vulns)}[/yellow] additional vulnerabilities")
            else:
                console.print("    [dim]OWASP Dependency-Check not available[/dim]")
        except Exception as e:
            errors.append(f"OWASP error: {e}")
    
    if use_nvd:
        console.print("  Querying NVD API...")
        try:
            nvd = NvdAnalyzer(config)
            vulns = nvd.analyze(dependencies)
            # Deduplicate with existing vulns
            existing_ids = {v.id for v in result.vulnerabilities}
            new_vulns = [v for v in vulns if v.id not in existing_ids]
            result.vulnerabilities.extend(new_vulns)
            result.sources_used.append("NVD")
            console.print(f"    Found [yellow]{len(new_vulns)}[/yellow] additional vulnerabilities")
        except Exception as e:
            errors.append(f"NVD error: {e}")
    
    if use_mend:
        console.print("  Querying Mend.io API...")
        try:
            from vuln_analyzer.analyzers.mend_analyzer import MendAnalyzer
            mend = MendAnalyzer(config)
            if mend.is_available():
                vulns = mend.analyze(dependencies)
                existing_ids = {v.id for v in result.vulnerabilities}
                new_vulns = [v for v in vulns if v.id not in existing_ids]
                result.vulnerabilities.extend(new_vulns)
                result.sources_used.append("Mend")
                console.print(f"    Found [yellow]{len(new_vulns)}[/yellow] additional vulnerabilities")
            else:
                console.print("    [dim]Mend not configured or ws-sdk not installed[/dim]")
        except ImportError:
            console.print("    [dim]ws-sdk not installed. Run: pip install ws-sdk[/dim]")
        except Exception as e:
            errors.append(f"Mend error: {e}")
    
    # Generate fix suggestions
    fixer = PomFixer(project_path)
    result.fix_suggestions = fixer.generate_fixes(result)
    
    result.scan_duration_seconds = time.time() - start_time
    result.errors = errors
    
    # Generate report
    if output_format == "json":
        reporter = JsonReporter()
        output = reporter.report(result, output_file)
        if not output_file:
            console.print(output)
        else:
            console.print(f"\n📄 JSON report saved to [bold]{output_file}[/bold]")
    elif output_format == "html":
        reporter = HtmlReporter()
        if not output_file:
            output_file = Path("vulnerability-report.html")
        reporter.report(result, output_file)
        console.print(f"\n📄 HTML report saved to [bold]{output_file}[/bold]")
    else:
        reporter = ConsoleReporter()
        reporter.report(result)
    
    # Check threshold
    if result.has_high_severity(config.thresholds.fail_on_cvss):
        console.print(
            f"\n[bold red]❌ Build failed: Found vulnerabilities with CVSS >= {config.thresholds.fail_on_cvss}[/bold red]"
        )
        raise typer.Exit(1)
    
    console.print("[bold green]✓ Scan complete[/bold green]\n")


@app.command()
def fix(
    project_path: Path = typer.Argument(
        ...,
        help="Path to Maven project",
        exists=True,
        dir_okay=True,
        file_okay=False,
    ),
    dry_run: bool = typer.Option(
        True, "--dry-run/--apply",
        help="Preview changes without applying them",
    ),
    no_backup: bool = typer.Option(
        False, "--no-backup",
        help="Don't create backup before modifying pom.xml",
    ),
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c",
        help="Path to configuration file",
    ),
):
    """Fix vulnerabilities by updating dependency versions."""
    config = Config.load(config_file)
    
    console.print(f"\n🔧 Analyzing [bold]{project_path}[/bold] for fixes...\n")
    
    # First, scan for vulnerabilities
    parser = PomParser(project_path)
    dependencies = parser.parse()
    
    # Run OWASP to get vulnerabilities
    result = AnalysisResult(
        project_path=str(project_path),
        dependencies=dependencies,
        vulnerabilities=[],
        fix_suggestions=[],
    )
    
    # Use offline analyzer for fix command
    offline = OfflineAnalyzer(config)
    result.vulnerabilities = offline.analyze(dependencies)
    
    # Generate and apply fixes
    fixer = PomFixer(project_path)
    fixes = fixer.generate_fixes(result)
    
    if not fixes:
        console.print("[green]No fixes needed - no vulnerable dependencies found![/green]\n")
        raise typer.Exit(0)
    
    console.print(f"Found [yellow]{len(fixes)}[/yellow] dependencies to update:\n")
    
    for fix in fixes:
        console.print(
            f"  • [cyan]{fix.dependency.group_id}:{fix.dependency.artifact_id}[/cyan]"
        )
        console.print(
            f"    [red]{fix.current_version}[/red] → [green]{fix.recommended_version}[/green]"
        )
        if fix.breaking_change:
            console.print("    [yellow]⚠ Major version change - review for breaking changes[/yellow]")
        console.print(f"    Fixes: {', '.join(fix.vulnerabilities_fixed[:3])}"
                     + (f" (+{len(fix.vulnerabilities_fixed)-3} more)" if len(fix.vulnerabilities_fixed) > 3 else ""))
        console.print()
    
    if dry_run:
        console.print("[dim]This is a dry run. Use --apply to make changes.[/dim]\n")
    else:
        applied = fixer.apply_fixes(fixes, dry_run=False, backup=not no_backup)
        console.print(f"\n[bold green]✓ Applied {len(applied)} fixes to pom.xml[/bold green]")
        if not no_backup:
            console.print("[dim]A backup was created with .bak extension[/dim]")
        console.print("\n[yellow]Run 'mvn compile' to verify the changes work correctly[/yellow]\n")


if __name__ == "__main__":
    app()
