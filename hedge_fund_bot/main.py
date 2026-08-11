"""
Main CLI Entry Point - Enterprise Hedge Fund System
"""

import os
import sys
import logging
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from src.graph import create_graph
from src.state import AgentState
from src.config import settings, AgentPrefix
from src.validation import validate_ticker
from src.telemetry import SessionTelemetry
from src.reporting import generate_html_report


load_dotenv()

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
)
logger = logging.getLogger(__name__)

if not os.getenv("GROQ_API_KEY") and not settings.GROQ_API_KEY:
    print("❌ Error: GROQ_API_KEY is not configured in .env or environment.")
    sys.exit(1)


def run_analysis(ticker: str) -> dict:
    """Execute stock analysis workflow."""
    try:
        ticker = validate_ticker(ticker)
    except ValueError as e:
        print(f"❌ {e}")
        return {"error": str(e)}
    
    print(f"\n🚀 Starting Enterprise Hedge Fund Analysis for {ticker}...")
    
    graph = create_graph()
    
    initial_state: AgentState = {
        "messages": [HumanMessage(content=f"Analyze stock {ticker}")],
        "next": "Supervisor",
        "current_ticker": ticker,
        "research_data": None,
        "technical_data": None,
        "final_report": None,
        "verification_passed": False,
        "verification_result": None,
        "iteration_count": 0,
        "telemetry": [],
    }
    
    try:
        return graph.invoke(initial_state, config={"recursion_limit": settings.RECURSION_LIMIT})
    except Exception as e:
        logger.error(f"Execution failure: {e}", exc_info=True)
        return {"error": str(e)}


def print_report_and_telemetry(state: dict) -> None:
    """Display final structured report and session telemetry."""
    if state.get("error"):
        print(f"\n❌ Analysis halted with error: {state.get('error')}")
        return

    report = state.get("final_report")
    verification = state.get("verification_result")
    technical = state.get("technical_data")
    telemetry_records = state.get("telemetry", [])

    print("\n" + "=" * 70)
    print(f"📊 INSTITUTIONAL INVESTMENT REPORT: {state.get('current_ticker', 'N/A')}")
    print("=" * 70)

    if report:
        print(f"\n🎯 RECOMMENDATION: {report.recommendation}")
        print(f"⚠️ RISK LEVEL:     {report.risk_level}")
        print(f"🔒 CONFIDENCE:     {report.confidence_score}%")
        
        if verification:
            print(f"✅ VERDICT:        {verification.verdict} (Valid: {verification.is_valid})")

        print("\n--- EXECUTIVE SUMMARY ---")
        print(report.executive_summary)

        print("\n--- FUNDAMENTAL ANALYSIS ---")
        print(report.fundamental_analysis)

        print("\n--- TECHNICAL ANALYSIS ---")
        print(report.technical_analysis)

        print("\n--- JUSTIFICATION ---")
        print(report.justification)
    else:
        print("\n⚠️ No final report generated.")

    if technical and technical.indicators:
        ind = technical.indicators
        print("\n" + "-" * 70)
        print("📈 QUANTITATIVE INDICATORS SUMMARY")
        print("-" * 70)
        print(f"Current Price: ${ind.current_price:.2f} ({ind.price_change_pct:+.2f}%)")
        print(f"SMA (20):      ${ind.sma_20:.2f} | Price vs SMA: {technical.price_vs_sma}")
        print(f"RSI (14):      {ind.rsi:.2f} ({technical.rsi_status})")
        print(f"MACD Hist:     {ind.macd_histogram:+.4f} | Outlook: {technical.technical_outlook}")
        print(f"Support/Res:   ${ind.low_support:.2f} / ${ind.high_resistance:.2f}")

    # Telemetry Summary
    session_telemetry = SessionTelemetry(ticker=state.get('current_ticker', 'UNKNOWN'))
    for record in telemetry_records:
        session_telemetry.add_node_telemetry(record)

    print("\n" + "=" * 70)
    print("⚡ SYSTEM TELEMETRY & OBSERVABILITY SUMMARY")
    print("=" * 70)
    print(f"⏱️ Total Execution Latency: {session_telemetry.total_execution_time_seconds:.2f}s")
    print(f"🔤 Total Tokens Consumed:  {session_telemetry.total_tokens:,} (Prompt: {session_telemetry.total_prompt_tokens:,}, Completion: {session_telemetry.total_completion_tokens:,})")
    print(f"💵 Estimated Cost:         ${session_telemetry.total_cost_usd:.6f} USD")
    print("\nBreakdown by Node:")
    for node in session_telemetry.node_telemetries:
        print(f"  • [{node.node_name:<10}] {node.execution_time_seconds:.2f}s | {node.total_tokens:>5} tokens | ${node.estimated_cost_usd:.6f}")
    print("=" * 70)

    # Generate HTML Report
    try:
        html_path = generate_html_report(state)
        print(f"\n🌐 HTML Report generated successfully:")
        print(f"   file://{html_path}\n")
    except Exception as e:
        logger.error(f"Failed to generate HTML report: {e}")



def main():
    print("\n" + "=" * 70)
    print("AUTONOMOUS HEDGE FUND - ENTERPRISE AGENT SYSTEM")
    print("=" * 70)
    print("Stack: LangGraph State Machine + Pydantic v2 + Groq Llama 3.3 70B\n")
    
    while True:
        ticker = input("Enter stock ticker (e.g. AAPL, MSFT, PETR4.SA) or 'exit': ").strip().upper()
        
        if ticker == 'EXIT':
            print("Goodbye!")
            break
        
        if not ticker:
            continue
        
        result = run_analysis(ticker)
        print_report_and_telemetry(result)


if __name__ == "__main__":
    main()
