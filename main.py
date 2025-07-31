"""
main.py

Entry point to generate a personalized portfolio report for a selected investor persona.
Fetches static stock signals, invokes GPT for explanation, and saves the result to /reports.
Usage: python3 main.py [persona_key]
"""

from personas import get_personas
from data_fetch import get_live_signals
from gpt_utils import build_portfolio_with_gpt
from report_generator import save_markdown_report

# Step 1: Define the tickers you want to test (stock + ETF)
tickers = ["AAPL", "TSLA", "GOOG", "SPY", "VOO"]

# Step 2: Get live/fallback signals from Yahoo Finance
stock_signals = get_live_signals(tickers)

# Step 3: Load beginner-friendly persona
personas = get_personas()
persona = personas["college_student"]

# Step 4: Generate GPT response using gpt-3.5-turbo
report = build_portfolio_with_gpt(persona, stock_signals)

# Step 5: Save output to a Markdown report
save_markdown_report("college_student", report)

# Step 6: Print the Markdown to console for review
print("\n===== GPT Portfolio Report =====\n")
print(report)
