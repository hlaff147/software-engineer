"""
HTML Report Generator for Autonomous Hedge Fund System

Generates standalone, responsive HTML reports summarizing research,
technical indicators, investment recommendation, verification audits,
and system observability metrics.
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional
import html

from src.state import AgentState
from src.telemetry import SessionTelemetry


def _escape(text: Optional[str]) -> str:
    """Safely escape HTML characters."""
    if not text:
        return ""
    return html.escape(str(text))


def _get_badge_class(value: str) -> str:
    """Return CSS class for badges based on sentiment or recommendation."""
    val = value.upper()
    if val in ["BUY", "BULLISH", "APPROVED", "LOW"]:
        return "badge-success"
    elif val in ["SELL", "BEARISH", "REJECTED", "HIGH"]:
        return "badge-danger"
    elif val in ["HOLD", "NEUTRAL", "NEEDS_REVISION", "MEDIUM"]:
        return "badge-warning"
    return "badge-secondary"


def generate_html_report(state: Dict[str, Any], output_dir: str = "reports") -> str:
    """
    Generate a standalone HTML report file from an AgentState dictionary.
    
    Args:
        state: LangGraph workflow result state containing research_data, technical_data,
               final_report, verification_result, and telemetry records.
        output_dir: Path to directory where HTML files will be saved.
        
    Returns:
        Absolute filepath to the generated HTML report.
    """
    os.makedirs(output_dir, exist_ok=True)

    ticker = state.get("current_ticker", "UNKNOWN").upper()
    report = state.get("final_report")
    technical = state.get("technical_data")
    research = state.get("research_data")
    verification = state.get("verification_result")
    telemetry_records = state.get("telemetry", [])

    # Calculate Session Telemetry
    session_telemetry = SessionTelemetry(ticker=ticker)
    for rec in telemetry_records:
        session_telemetry.add_node_telemetry(rec)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.abspath(os.path.join(output_dir, f"report_{ticker}_{timestamp_file}.html"))

    # Extract indicators
    ind = technical.indicators if (technical and hasattr(technical, 'indicators')) else None

    # Recommendations & badging
    rec_str = report.recommendation if report else "N/A"
    risk_str = report.risk_level if report else "N/A"
    conf_val = report.confidence_score if report else 0
    verdict_str = verification.verdict if verification else "N/A"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hedge Fund Analysis Report - {ticker}</title>
    <style>
        :root {{
            --bg-main: #0d1117;
            --bg-card: #161b22;
            --bg-card-hover: #1c2128;
            --border-color: #30363d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --green: #2ea043;
            --red: #f85149;
            --yellow: #d29922;
            --purple: #bc8cff;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2rem 1rem;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        
        .header-card {{
            background: linear-gradient(135deg, #1f242d 0%, #161b22 100%);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}
        
        .header-title {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .ticker-badge {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--accent-blue);
            letter-spacing: 1px;
        }}
        
        .meta-date {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .metrics-banner {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
        }}
        
        .kpi-card {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }}
        
        .kpi-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 0.3rem;
            letter-spacing: 0.5px;
        }}
        
        .kpi-value {{
            font-size: 1.4rem;
            font-weight: 700;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
        }}
        
        .badge-success {{ background: rgba(46, 160, 67, 0.2); color: #3fb950; border: 1px solid #2ea043; }}
        .badge-danger {{ background: rgba(248, 81, 73, 0.2); color: #f85149; border: 1px solid #da3633; }}
        .badge-warning {{ background: rgba(210, 153, 34, 0.2); color: #d29922; border: 1px solid #bb8009; }}
        .badge-secondary {{ background: rgba(139, 148, 158, 0.2); color: #8b949e; border: 1px solid #6e7681; }}
        
        .section-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.8rem;
            margin-bottom: 1.5rem;
        }}
        
        .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent-blue);
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.6rem;
        }}
        
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .table-custom {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        
        .table-custom th, .table-custom td {{
            padding: 0.8rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .table-custom th {{
            background: rgba(255,255,255,0.02);
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
        }}
        
        .table-custom tr:hover {{
            background: var(--bg-card-hover);
        }}
        
        ul.tag-list {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}
        
        ul.tag-list li {{
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.9rem;
        }}
        
        ul.tag-list.catalysts li {{ border-left: 3px solid var(--green); }}
        ul.tag-list.red-flags li {{ border-left: 3px solid var(--red); }}
        
        footer {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Card -->
        <div class="header-card">
            <div class="header-title">
                <div>
                    <span class="ticker-badge">📊 {ticker}</span>
                    <h2 style="color: var(--text-secondary); font-size: 1rem; font-weight: 400; margin-top: 0.2rem;">
                        Autonomous Institutional Investment Report
                    </h2>
                </div>
                <div class="meta-date">Generated: {now_str}</div>
            </div>
            
            <div class="metrics-banner">
                <div class="kpi-card">
                    <div class="kpi-label">Recommendation</div>
                    <div class="kpi-value"><span class="badge {_get_badge_class(rec_str)}">{rec_str}</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Risk Level</div>
                    <div class="kpi-value"><span class="badge {_get_badge_class(risk_str)}">{risk_str}</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Confidence Score</div>
                    <div class="kpi-value" style="color: var(--accent-blue);">{conf_val}%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Verifier Audit</div>
                    <div class="kpi-value"><span class="badge {_get_badge_class(verdict_str)}">{verdict_str}</span></div>
                </div>
            </div>
        </div>

        <!-- Executive Summary -->
        {_build_executive_summary_html(report)}

        <!-- Quantitative Technical Analysis -->
        {_build_technical_html(technical, ind)}

        <!-- Fundamental Research & News -->
        {_build_research_html(research)}

        <!-- Verifier Audit (PEV) -->
        {_build_verifier_html(verification)}

        <!-- Telemetry & System Observability -->
        {_build_telemetry_html(session_telemetry)}

        <footer>
            Autonomous Hedge Fund System &bull; LangGraph State Machine &bull; Pydantic v2 Architecture
        </footer>
    </div>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filepath


def _build_executive_summary_html(report: Any) -> str:
    if not report:
        return """
        <div class="section-card">
            <div class="section-title">📌 Executive Summary</div>
            <p style="color: var(--text-secondary);">No analyst report was generated for this session.</p>
        </div>"""
    
    return f"""
    <div class="section-card">
        <div class="section-title">📌 Investment Thesis & Executive Summary</div>
        <p style="font-size: 1.05rem; margin-bottom: 1.2rem;">{_escape(report.executive_summary)}</p>
        
        <h4 style="color: var(--accent-blue); margin-bottom: 0.5rem; font-size: 0.95rem;">CORE JUSTIFICATION</h4>
        <p style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 6px; border-left: 3px solid var(--accent-blue); font-style: italic;">
            "{_escape(report.justification)}"
        </p>
    </div>
    """


def _build_technical_html(technical: Any, ind: Any) -> str:
    if not technical or not ind:
        return """
        <div class="section-card">
            <div class="section-title">📈 Quantitative Technical Analysis</div>
            <p style="color: var(--text-secondary);">No technical data available.</p>
        </div>"""

    change_color = "var(--green)" if ind.price_change_pct >= 0 else "var(--red)"
    change_sign = "+" if ind.price_change_pct >= 0 else ""

    return f"""
    <div class="section-card">
        <div class="section-title">📈 Quantitative Technical Indicators</div>
        
        <div class="grid-2" style="margin-bottom: 1.5rem;">
            <div>
                <table class="table-custom">
                    <tr><th>Current Price</th><td><strong>${ind.current_price:.2f}</strong> (<span style="color:{change_color};">{change_sign}{ind.price_change_pct:.2f}%</span>)</td></tr>
                    <tr><th>SMA (20 Days)</th><td>${ind.sma_20:.2f} (<span class="badge {_get_badge_class('APPROVED' if technical.price_vs_sma == 'ABOVE' else 'REJECTED')}">{technical.price_vs_sma}</span>)</td></tr>
                    <tr><th>RSI (14 Days)</th><td>{ind.rsi:.2f} (<span class="badge {_get_badge_class(technical.rsi_status)}">{technical.rsi_status}</span>)</td></tr>
                </table>
            </div>
            <div>
                <table class="table-custom">
                    <tr><th>MACD Line / Signal</th><td>{ind.macd_line:.4f} / {ind.macd_signal:.4f}</td></tr>
                    <tr><th>MACD Histogram</th><td><strong style="color: {'var(--green)' if ind.macd_histogram > 0 else 'var(--red)'};">{ind.macd_histogram:+.4f}</strong></td></tr>
                    <tr><th>Technical Outlook</th><td><span class="badge {_get_badge_class(technical.technical_outlook)}">{technical.technical_outlook}</span></td></tr>
                    <tr><th>30-Day Support / Res.</th><td>${ind.low_support:.2f} &ndash; ${ind.high_resistance:.2f}</td></tr>
                </table>
            </div>
        </div>
        
        <h4 style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase;">Technical Interpretation</h4>
        <p style="margin-bottom: 1rem;">{_escape(technical.analysis_summary)}</p>
        
        <h4 style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase;">Key Technical Signals</h4>
        <ul class="tag-list">
            {"".join([f"<li>{_escape(s)}</li>" for s in technical.key_signals])}
        </ul>
    </div>
    """


def _build_research_html(research: Any) -> str:
    if not research:
        return """
        <div class="section-card">
            <div class="section-title">📰 Fundamental Research & News</div>
            <p style="color: var(--text-secondary);">No fundamental research data available.</p>
        </div>"""

    catalysts_html = "".join([f"<li>{_escape(c)}</li>" for c in research.catalysts]) or "<li>No growth catalysts specified</li>"
    red_flags_html = "".join([f"<li>{_escape(r)}</li>" for r in research.red_flags]) or "<li>No critical red flags identified</li>"

    return f"""
    <div class="section-card">
        <div class="section-title">
            <span>📰 Fundamental Research & Market Sentiment</span>
            <span class="badge {_get_badge_class(research.market_sentiment)}" style="margin-left: auto;">{research.market_sentiment}</span>
        </div>
        
        <p style="margin-bottom: 1.5rem;">{_escape(research.summary)}</p>
        
        <div class="grid-2">
            <div>
                <h4 style="color: var(--green); font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase;">🚀 Catalysts & Drivers</h4>
                <ul class="tag-list catalysts">
                    {catalysts_html}
                </ul>
            </div>
            <div>
                <h4 style="color: var(--red); font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase;">⚠️ Risks & Red Flags</h4>
                <ul class="tag-list red-flags">
                    {red_flags_html}
                </ul>
            </div>
        </div>
    </div>
    """


def _build_verifier_html(verification: Any) -> str:
    if not verification:
        return ""
        
    status_icon = "✅" if verification.is_valid else "❌"
    issues_html = "".join([f"<li>{_escape(i)}</li>" for i in verification.issues_found]) or "<li>No inconsistencies detected</li>"
    recs_html = "".join([f"<li>{_escape(r)}</li>" for r in verification.recommendations]) or "<li>No revision notes</li>"

    return f"""
    <div class="section-card">
        <div class="section-title">
            <span>🛡️ Verifier Consistency Audit (PEV Pattern)</span>
            <span class="badge {_get_badge_class(verification.verdict)}" style="margin-left: auto;">{status_icon} {verification.verdict}</span>
        </div>
        
        <p style="margin-bottom: 1rem;">{_escape(verification.summary)}</p>
        
        <div class="grid-2">
            <div>
                <h4 style="color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.4rem;">Audit Findings</h4>
                <ul class="tag-list">
                    {issues_html}
                </ul>
            </div>
            <div>
                <h4 style="color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.4rem;">Recommendations</h4>
                <ul class="tag-list">
                    {recs_html}
                </ul>
            </div>
        </div>
    </div>
    """


def _build_telemetry_html(telemetry: SessionTelemetry) -> str:
    rows = ""
    for rec in telemetry.node_telemetries:
        rows += f"""
        <tr>
            <td><strong>{_escape(rec.node_name)}</strong></td>
            <td>{rec.execution_time_seconds:.2f}s</td>
            <td>{rec.total_tokens:,} (Prompt: {rec.prompt_tokens:,}, Comp: {rec.completion_tokens:,})</td>
            <td>${rec.estimated_cost_usd:.6f}</td>
            <td><span class="badge {_get_badge_class('APPROVED' if rec.status == 'SUCCESS' else 'WARNING')}">{_escape(rec.status)}</span></td>
        </tr>
        """

    return f"""
    <div class="section-card">
        <div class="section-title">⚡ System Observability & Telemetry</div>
        
        <div class="grid-2" style="margin-bottom: 1.2rem;">
            <div class="kpi-card">
                <div class="kpi-label">Total Execution Latency</div>
                <div class="kpi-value">{telemetry.total_execution_time_seconds:.2f}s</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Tokens Consumed</div>
                <div class="kpi-value">{telemetry.total_tokens:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Estimated LLM Cost</div>
                <div class="kpi-value" style="color: var(--green);">${telemetry.total_cost_usd:.6f} USD</div>
            </div>
        </div>

        <table class="table-custom">
            <thead>
                <tr>
                    <th>Node</th>
                    <th>Latency</th>
                    <th>Token Breakdown</th>
                    <th>Cost</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else '<tr><td colspan="5" style="text-align:center; color:var(--text-secondary);">No telemetry records collected</td></tr>'}
            </tbody>
        </table>
    </div>
    """
