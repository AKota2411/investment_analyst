"""
personas.py

Defines preset investor personas that reflect different risk tolerances, goals,
and experience levels. Each persona guides how the portfolio will be tailored.

Example personas include:
- College Student (moderate risk, long-term growth)
- High School Student (very low risk, learning-focused)

Call get_personas() to retrieve all available personas as a dictionary.
"""

def get_personas():
    return {
        "high_school_student": {
            "name": "High School Student",
            "risk": "very low",
            "goal": "learn the market and preserve capital",
            "description": (
                "A first-time investor starting with a small amount of money. "
                "Wants safe exposure to the market and simple explanations. "
                "Prefers well-known index funds and avoids high volatility."
            )
        },

        "college_student": {
            "name": "College Student",
            "risk": "moderate",
            "goal": "long-term balanced growth",
            "description": (
                "A young investor with a long time horizon and willingness to take some risk "
                "for higher returns. Interested in tech, index funds, and learning how to build a portfolio."
            )
        },

        "defensive_investor": {
            "name": "Defensive Investor",
            "risk": "low",
            "goal": "minimize downside during market volatility",
            "description": (
                "Cautious about economic downturns. Invests in large, well-known companies that "
                "are stable and recession-resistant. Avoids complex sectors like energy and real estate. "
                "Prefers S&P 500 stocks and ETFs with strong fundamentals."
            )
        },

        "long_term_holder": {
            "name": "Long-Term Holder",
            "risk": "moderate",
            "goal": "build wealth gradually with stable, proven companies",
            "description": (
                "A disciplined investor focused on holding investments for many years. "
                "Believes in the long-term strength of the market. Values reliable growth "
                "over speculation and short-term gains."
            )
        },

        "research_focused_investor": {
            "name": "Research-Focused Investor",
            "risk": "moderate",
            "goal": "make informed, evidence-based investment choices",
            "description": (
                "Prefers to understand a company's fundamentals before investing. Looks at "
                "analyst reports, peer comparisons, index membership, and valuation data. "
                "Wants both pros and cons clearly explained before taking action."
            )
        },

        "scenario_planner": {
            "name": "Scenario-Based Investor",
            "risk": "customizable",
            "goal": "build a portfolio tailored to specific conditions or themes",
            "description": (
                "Wants the ability to specify scenarios like 'recession-proof' or 'tech-heavy' portfolios. "
                "Seeks tools that allow input on sectors, time horizon, and risk preferences, with "
                "transparent explanations behind each recommendation."
            )
        }
    }
