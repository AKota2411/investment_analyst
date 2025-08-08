import streamlit as st
from personas import get_personas
from data_fetch import get_live_signals
from gpt_utils import build_portfolio_with_gpt

# Define available tickers for demo
DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOG", "SPY", "VOO"]

# Industries to filter by
INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Energy", "Consumer Goods",
    "Utilities", "Real Estate", "Industrial", "Telecommunications"
]

# Holding period choices
HOLDING_PERIODS = ["1-3 years", "4-7 years", "10+ years"]

# Streamlit app
st.set_page_config(page_title="Investment Assistant", layout="centered")

st.title("💼 Investment Assistant – Personalized Recommendations")
st.write("Get tailored investment ideas based on your goals, risk tolerance, and preferred industries.")

# Step 1: Persona selection
personas = get_personas()
persona_choice = st.selectbox("Choose an Investor Persona", list(personas.keys()))
persona = personas[persona_choice]

# Step 2: Holding period
holding_period = st.selectbox("Select your holding period", HOLDING_PERIODS)

# Step 3: Industries
selected_industries = st.multiselect(
    "Select preferred industries",
    INDUSTRIES,
    default=["Technology", "Finance"]
)

# Step 4: Risk tolerance (override persona if needed)
risk_override = st.selectbox(
    "Select your risk tolerance (optional)",
    ["Use persona default", "very low", "low", "moderate", "high"]
)

# Generate button
if st.button("Generate Recommendations"):
    with st.spinner("Fetching data and generating portfolio..."):
        # Update persona fields
        if risk_override != "Use persona default":
            persona["risk_tolerance"] = risk_override
        persona["holding_period"] = holding_period
        persona["preferred_industries"] = selected_industries

        # Fetch live/fallback stock signals
        stock_signals = get_live_signals(DEFAULT_TICKERS)

        # Get GPT recommendations
        report = build_portfolio_with_gpt(persona, stock_signals)

    # Display result
    st.subheader("📊 Recommended Portfolio")
    for line in report.split("\n"):
        if line.strip().startswith("-"):
            st.markdown(f"{line}")
        else:
            st.write(line)

    st.success("✅ Recommendations generated successfully!")
