# GenAI-Powered Investment Analyst

## 🔋 Overview

This is a GPT-assisted portfolio builder and explainer tool designed for beginner investors. It combines numerical stock signal data (e.g., returns, sentiment) with natural language generation to provide tailored portfolio recommendations based on user goals, risk tolerance, and holding period.

Reports are generated in plain Markdown, written in simple, readable language, and include rationale, pros/cons, and numerical justification for each asset.

---

## 🔧 Features

* **AI-Powered Recommendations**: Generates 3–4 asset portfolios using GPT-4.
* **Readable Investment Reports**: Explanations written for beginners, max 3–4 sentences per paragraph.
* **Numerical Justification**: Includes predicted returns, sentiment scores, and historical performance.
* **Persona-Based Tailoring**: User goals, risk level, and holding period drive all recommendations.
* **Modular Backend**: Separated logic for data, prompt, personas, and output generation.

---

## 📂 File Structure

```
investment_analyst/
├── main.py                # Core logic: run persona-based recommendation and report
├── gpt_utils.py           # GPT prompt builder and completion handler
├── personas.py            # Investor profile definitions
├── data_fetch.py          # Predicted return and sentiment input (mocked or real)
├── report_generator.py    # Saves final GPT response into Markdown
├── test.py                # Manual testing hooks (optional)
└── reports/               # Generated .md reports saved here
```

---

## 🔢 How It Works

1. **Persona Selected** (`personas.py`)

   * Each persona has a name, risk level, goal, and description

2. **Market Data Pulled** (`data_fetch.py`)

   * Currently mocked or static predicted returns and sentiment values

3. **Prompt Constructed** (`gpt_utils.py`)

   * Uses persona info + optional scenario (e.g., "defensive stocks")
   * Builds prompt with 3-4 sentence per-asset requirements, pros/cons, and numerics

4. **GPT Model Called**

   * Uses `gpt-3.5-turbo` for low-cost, fast completions
   * Returns natural language explanation

5. **Report Saved** (`report_generator.py`)

   * Markdown file saved to `/reports` with user-friendly layout

---

## 👩‍💼 Example Output (College Student Persona)

```
For College Student's balanced long-term growth goal with medium risk tolerance, a diversified portfolio could include AAPL, SPY, and VOO. AAPL offers a predicted return of 6.2% and sentiment score of 72%, providing moderate tech exposure with strong brand reliability.

SPY and VOO provide 3–4% expected returns and sentiment scores above 85%, making them low-risk index funds ideal for compounding. They track the S&P 500 and offer excellent diversification.

AAPL returned ~20% annually over the last 5 years, though tech can be volatile. SPY and VOO returned ~10%, making them suitable for risk-aware beginners.

Final decisions should be made based on individual financial goals and may benefit from professional advice.
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
```

### 3. Run the program

```bash
python3 main.py
```

Markdown output will be saved in `/reports`.

---

## 🛠️ Customization Options

* Add new personas to `personas.py`
* Modify or connect `data_fetch.py` to integrate live financial data
* Adjust prompt behavior or output style in `gpt_utils.py`
* Use `test.py` for running local debug prompts

---

## ⚠️ Disclaimers

This tool is intended for educational use only and is not financial advice. Investment decisions should be based on individual goals and may require consultation with a financial advisor.

---

## 📈 Future Ideas

* FastAPI wrapper for API usage
* Editable scenarios and sector preferences
* Sentiment integration from news + earnings scraping
* Frontend UI for easier persona/scenario selection
