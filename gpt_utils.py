"""
gpt_utils.py

Constructs prompts for GPT and processes responses to generate tailored investment
recommendations based on the user persona and stock signals.

Key function:
- build_portfolio_with_gpt(): Sends portfolio-building prompt to GPT-3.5-turbo,
  receives rationale-based stock recommendations and returns them as a string.
"""

# gpt_utils.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# optional: resolve company names for nicer bullets
import yfinance as yf

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _resolve_company_names(tickers):
    """
    Best-effort mapping from ticker -> company long name using yfinance.
    Falls back to the ticker if not available or on error.
    """
    names = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).info  # may be slow; we only call for the small set we pass in
            long_name = info.get("longName") or info.get("shortName") or t
            names[t] = long_name
        except Exception:
            names[t] = t
    return names

def build_portfolio_with_gpt(persona, stock_signals):
    """
    Build tightly structured, industry-aware recommendations.
    Each asset includes one concise 'Industry relevance' line (<= 20 words)
    referencing a product/service/market role that ties to the selected industries.
    """
    try:
        persona_name = persona.get("name", "Investor")
        persona_goals = persona.get("goal", "grow wealth")
        scenario = persona.get("scenario", "balanced long-term growth")
        risk = persona.get("risk_tolerance", persona.get("risk", "moderate"))
        holding = persona.get("holding_period", "5+ years")
        industries = persona.get("preferred_industries", [])
        industries_str = ", ".join(industries) if industries else "no specific industries selected"

        # Prepare ticker -> company name mapping for nicer bullets
        tickers = list(stock_signals.keys())
        company_names = _resolve_company_names(tickers)

        # Build compact stock descriptions with numbers for the model
        # Example: "AAPL (Apple Inc.): expected_return=3.2%, sentiment=78%"
        stock_rows = []
        for t, info in stock_signals.items():
            try:
                exp_ret = float(info["return"]) * 100.0
            except Exception:
                exp_ret = 0.0
            try:
                sent = float(info["sentiment"]) * 100.0
            except Exception:
                sent = 50.0
            stock_rows.append(f"{t} ({company_names.get(t, t)}): expected_return={exp_ret:.1f}%, sentiment={sent:.0f}%")

        stock_block = "\n".join(stock_rows)

        # Prompt: short, numeric, and industry-tied relevance
        prompt = (
            "You are a financial assistant helping a beginner investor.\n\n"
            f"Investor: {persona_name}\n"
            f"Scenario: {scenario}\n"
            f"Goal: {persona_goals}\n"
            f"Risk tolerance: {risk}\n"
            f"Holding period: {holding}\n"
            f"Preferred industries: {industries_str}\n\n"
            f"Available stocks and funds (all have positive recent returns) with predicted returns and sentiment scores:\n"
            f"{stock_block}\n\n"
            "Task: Recommend a 3–4 asset portfolio tailored to this investor and industries. "
            "Be concise, numerically grounded, and beginner-friendly.\n\n"
            "For EACH recommended asset, output exactly this Markdown shape:\n"
            "- TICKER – Company Name\n"
            "  Industry relevance: <max 20 words tying the company to the selected industry via a product/service/market role>\n"
            "  Rationale: 2–3 sentences; include expected_return (%) and sentiment (%) from above; keep it plain-English.\n"
            "  Pros: <1–2 short pros>\n"
            "  Cons: <1–2 short cons>\n"
            "  Recent performance: brief 1-year or 5-year context if useful (concise)\n\n"
            "Constraints:\n"
            "- Use the candidate list above; prioritize those aligned with the selected industries.\n"
            "- Keep each 'Industry relevance' to 20 words or fewer—specific and concrete (e.g., flagship product, dominant segment, ETF coverage of sector).\n"
            "- Keep paragraphs short and readable; avoid long blocks of text.\n"
            "- End with one sentence reminding the user that final decisions are theirs."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",   # low-cost model per your constraint
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,         # slightly lower for tighter, more factual outputs
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"GPT error: {e}")
        return "Fallback: Could not generate portfolio explanation."
