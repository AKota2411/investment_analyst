from personas import get_personas
from gpt_utils import build_portfolio_with_gpt
from report_generator import save_markdown_report

# Load predefined investor personas
personas = get_personas()

# Select one persona for demonstratio
persona = personas['college_student']  # Could be replaced with user input

# Static stock and index fund signal data
# Values represent predicted return and sentiment score (between -1 and 1)
stock_signals = {
    "AAPL": {"return": 0.03, "sentiment": 0.6},     # Apple: Moderate growth, positive sentiment
    "TSLA": {"return": 0.05, "sentiment": 0.8},     # Tesla: High risk, strong news coverage
    "GOOG": {"return": 0.02, "sentiment": 0.5},     # Google: Stable growth, neutral sentiment
    "SPY":  {"return": 0.01, "sentiment": 0.9},     # S&P 500 ETF: Very low risk, steady market sentiment
    "VOO":  {"return": 0.015, "sentiment": 0.85}    # Vanguard S&P 500 ETF: Conservative, highly diversified
}

# Ask GPT to build a rationale-based portfolio
report = build_portfolio_with_gpt(persona, stock_signals)

# Save the response as a Markdown report
save_markdown_report("college_student", report)

print("Portfolio report saved to reports/college_student_report.md")
