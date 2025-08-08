# app.py
import streamlit as st
from personas import get_personas
from data_fetch import get_live_signals
from gpt_utils import build_portfolio_with_gpt
from industry_select import fetch_tickers_by_industries

# --------------------------
# Page config and CSS theme
# --------------------------
st.set_page_config(page_title="Investment Assistant", layout="centered")

CARD_CSS = """
<style>
/* Page */
.block-container { max-width: 840px; }



/* Header and helper text */
.card h1 {
  font-size: 1.6rem;
  margin: 0 0 8px 0;
}
.card p.helper {
  color: #6b7280;
  margin: 0 0 20px 0;
}

/* Footer controls */
.card .footer {
  display: flex;
  justify-content: space-between;
  margin-top: 18px;
}

/* Progress bar */
.progress-wrap {
  width: 100%;
  background: #f3f4f6;
  border-radius: 9999px;
  height: 8px;
  margin: 8px 0 20px 0;
}
.progress-fill {
  height: 8px;
  border-radius: 9999px;
  background: #2563eb;
  width: 0%;
  transition: width 250ms ease;
}

/* Pills for choices */
.pill {
  display: inline-block;
  padding: 6px 10px;
  background: #f3f4f6;
  border-radius: 9999px;
  margin-right: 8px;
  margin-bottom: 6px;
  font-size: 0.9rem;
  color: #374151;
}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# --------------------------
# Wizard state
# --------------------------
STEPS = [
    "persona", "scenario", "risk", "holding", "industries", "review", "results"
]
TOTAL_STEPS = len(STEPS)

if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0

if "answers" not in st.session_state:
    st.session_state.answers = {
        "persona_key": None,
        "scenario": "",
        "risk": None,
        "holding": None,
        "industries": []
    }

def go_next():
    if st.session_state.step_idx < TOTAL_STEPS - 1:
        st.session_state.step_idx += 1

def go_back():
    if st.session_state.step_idx > 0:
        st.session_state.step_idx -= 1

def progress_ratio():
    # Count review as “done”, results as 100%
    current = min(st.session_state.step_idx + 1, TOTAL_STEPS)
    return current / TOTAL_STEPS

# --------------------------
# Data sources
# --------------------------
personas = get_personas()
persona_keys = list(personas.keys())
DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOG", "SPY", "VOO"]
INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Energy", "Consumer Goods",
    "Utilities", "Real Estate", "Industrial", "Telecommunications"
]
RISK_OPTIONS = ["very low", "low", "moderate", "high"]
HOLDING_PERIODS = ["1-3 years", "4-7 years", "10+ years"]

# --------------------------
# Header + progress
# --------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h1>Investment Assistant – Personalized Recommendations</h1>", unsafe_allow_html=True)
st.markdown("<p class='helper'>Answer a few quick questions to get your tailored profile.</p>", unsafe_allow_html=True)

prog_pct = int(progress_ratio() * 100)
st.markdown(
    f"<div class='progress-wrap'><div class='progress-fill' style='width:{prog_pct}%;'></div></div>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# Step renderers
# --------------------------
def card_start(title, helper=None):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    if helper:
        st.markdown(f"<p class='helper'>{helper}</p>", unsafe_allow_html=True)

def card_end(show_back=True, show_next=True, next_label="Next", on_next=None):
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    with col1:
        if show_back:
            if st.button("Back", use_container_width=True):
                go_back()
    with col2:
        if show_next:
            if st.button(next_label, use_container_width=True):
                if on_next:
                    ok = on_next()
                    if ok is False:
                        # validation failed; do not advance
                        st.stop()
                go_next()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- persona ---
def step_persona():
    card_start(
        "Who are you as an investor?",
        "Pick a persona that best fits your current situation."
    )
    default_idx = persona_keys.index("college_student") if "college_student" in persona_keys else 0
    choice = st.selectbox(
        "Persona",
        persona_keys,
        index=default_idx,
        format_func=lambda k: personas[k]["name"]
    )
    st.session_state.answers["persona_key"] = choice
    card_end(show_back=False, next_label="Continue")

# --- scenario ---
def step_scenario():
    card_start(
        "What is your investing scenario or goal?",
        "Give a short description so we can tailor recommendations."
    )
    text = st.text_area(
        "Example: Defensive during potential downturn; steady growth while saving for grad school.",
        value=st.session_state.answers.get("scenario", ""),
        height=120
    )
    def on_next():
        st.session_state.answers["scenario"] = text.strip()
        return True
    card_end(next_label="Continue", on_next=on_next)

# --- risk ---
def step_risk():
    card_start(
        "How much risk are you comfortable with?",
        "Pick the level that feels right to you."
    )
    persona_key = st.session_state.answers["persona_key"]
    persona_risk = personas.get(persona_key, {}).get("risk", "moderate")
    idx = RISK_OPTIONS.index(persona_risk) if persona_risk in RISK_OPTIONS else RISK_OPTIONS.index("moderate")
    risk = st.radio("Risk tolerance", RISK_OPTIONS, index=idx, horizontal=True)
    def on_next():
        st.session_state.answers["risk"] = risk
        return True
    card_end(next_label="Continue", on_next=on_next)

# --- holding ---
def step_holding():
    card_start(
        "How long do you plan to hold these investments?",
        "Choose a holding period."
    )
    holding = st.radio("Holding period", HOLDING_PERIODS, index=0, horizontal=True)
    def on_next():
        st.session_state.answers["holding"] = holding
        return True
    card_end(next_label="Continue", on_next=on_next)

# --- industries ---
def step_industries():
    card_start(
        "Any industries you prefer?",
        "Optional, choose one or more industries to personalize your portfolio."
    )
    selected = st.multiselect(
        "Industries",
        INDUSTRIES,
        default=st.session_state.answers.get("industries", [])
    )
    st.write("Selected:")
    if selected:
        st.markdown(" ".join(f"<span class='pill'>{i}</span>" for i in selected), unsafe_allow_html=True)
    else:
        st.caption("No specific industries selected.")
    def on_next():
        st.session_state.answers["industries"] = selected
        return True
    card_end(next_label="Review", on_next=on_next)

# --- review ---
def step_review():
    a = st.session_state.answers
    persona_key = a["persona_key"]
    persona = personas[persona_key]
    card_start(
        "Review your inputs",
        "Confirm your details before generating your portfolio."
    )
    st.write(f"Persona: **{persona['name']}**")
    st.write(f"Goal: **{persona.get('goal','')}**")
    st.write(f"Scenario: **{a['scenario'] or 'balanced long-term growth'}**")
    st.write(f"Risk tolerance: **{a['risk']}**")
    st.write(f"Holding period: **{a['holding']}**")
    inds = a['industries']
    st.write("Industries: " + (", ".join(inds) if inds else "No preference"))

    def on_next():
        # Trigger generation on next step
        return True
    card_end(next_label="Generate Portfolio", on_next=on_next)

# --- results ---
def step_results():
    a = st.session_state.answers
    persona_key = a["persona_key"]
    persona = dict(personas[persona_key])  # copy, so we do not mutate source
    persona["scenario"] = a["scenario"] or "balanced long-term growth"
    persona["risk_tolerance"] = a["risk"]
    persona["holding_period"] = a["holding"]
    if a["industries"]:
        persona["preferred_industries"] = a["industries"]

    card_start(
        "Your tailored portfolio",
        "These recommendations are derived from your inputs and current market signals."
    )

    # >>> NEW: live ticker selection by industries
    with st.spinner("Selecting relevant companies from your chosen industries..."):
        tickers = fetch_tickers_by_industries(a.get("industries", []), per_industry=5, max_total=15)

    # Fetch signals and ask GPT
    with st.spinner("Generating recommendations..."):
        signals = get_live_signals(tickers)
        report = build_portfolio_with_gpt(persona, signals)

    # Render bullets with alignment note
    chunks = [c.strip() for c in report.strip().split("\n\n") if c.strip()]
    if not chunks:
        st.warning("No recommendations returned. Please try again.")
    else:
        for block in chunks:
            lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
            if not lines:
                continue
            lead = lines[0]
            if lead.startswith("-"):
                st.markdown(lead)
                for cont in lines[1:]:
                    st.write(cont)
            else:
                st.markdown(f"- {lead}")
                for cont in lines[1:]:
                    st.write(cont)

            if a["industries"]:
                st.caption(f"This recommendation aligns with your interest in {', '.join(a['industries'])}.")

    st.markdown("---")
    st.write("This is for educational purposes only and is not financial advice.")
    card_end(show_back=True, show_next=False)

# --------------------------
# Router
# --------------------------
current = STEPS[st.session_state.step_idx]
if current == "persona":
    step_persona()
elif current == "scenario":
    step_scenario()
elif current == "risk":
    step_risk()
elif current == "holding":
    step_holding()
elif current == "industries":
    step_industries()
elif current == "review":
    step_review()
elif current == "results":
    step_results()
