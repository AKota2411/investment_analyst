"""
gpt_utils.py

Constructs prompts for GPT and processes responses to generate tailored investment
recommendations based on the user persona and stock signals.

Key function:
- build_portfolio_with_gpt(): Sends portfolio-building prompt to GPT-3.5-turbo,
  receives rationale-based stock recommendations and returns them as a string.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_portfolio_with_gpt(persona, stock_signals):
    try:
        persona_name = persona["name"]
        persona_goals = persona["goal"]
        scenario = persona.get("scenario", "balanced long-term growth")
        risk = persona.get("risk_tolerance", "medium")
        holding = persona.get("holding_period", "5+ years")

        stock_descriptions = [
            f"{ticker}: return={float(info['return'])*100:.1f}%, sentiment={float(info['sentiment'])*100:.0f}%"
            for ticker, info in stock_signals.items()
        ]

        prompt = (
            f"You are a financial assistant helping a beginner investor named {persona_name}.\n"
            f"They are seeking: {scenario}\n"
            f"Investment goal: {persona_goals}\n"
            f"Risk tolerance: {risk}\n"
            f"Holding period: {holding}\n\n"
            f"Available stocks and funds with predicted returns and sentiment scores:\n"
            f"{chr(10).join(stock_descriptions)}\n\n"
            f"Suggest a 3–4 asset portfolio tailored to this persona.\n"
            f"For each recommended asset:\n"
            f"- Provide 3–4 sentences explaining the rationale\n"
            f"- Include specific numbers: expected return (%, based on prediction), sentiment score (0–100%), and any notable historical return data\n"
            f"- Add 1–2 pros and 1–2 cons based on risk, performance, or volatility\n"
            f"- Mention past 1-year or 5-year performance if relevant\n\n"
            f"Write in clear, readable paragraphs (no more than 4 sentences per paragraph).\n"
            f"End with a reminder that the final investment decision is up to the user."
        )


        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # low-cost model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ GPT error: {e}")
        return "Fallback: Could not generate portfolio explanation."
