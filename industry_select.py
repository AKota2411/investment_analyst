# industry_select.py
import random
from typing import List, Dict
from yahooquery import Screener

# Fallback curated tickers per industry (used only if live fetch fails)
FALLBACK_TICKERS: Dict[str, List[str]] = {
    "Technology": ["AAPL", "MSFT", "NVDA", "ADBE", "GOOG", "AMZN", "AVGO", "CRM", "AMD", "INTC"],
    "Healthcare": ["JNJ", "PFE", "UNH", "MRK", "LLY", "ABBV", "TMO", "DHR", "BMY", "AMGN"],
    "Finance": ["JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "AXP", "USB"],
    "Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "PSX", "MPC", "PXD", "VLO", "BKR"],
    "Consumer Goods": ["PG", "KO", "PEP", "COST", "WMT", "PM", "MDLZ", "CL", "KMB", "MO"],
    "Utilities": ["NEE", "DUK", "SO", "AEP", "D", "EXC", "SRE", "XEL", "PEG", "ED"],
    "Real Estate": ["PLD", "AMT", "EQIX", "SPG", "PSA", "CCI", "O", "WELL", "VICI", "DLR"],
    "Industrial": ["CAT", "GE", "HON", "UPS", "DE", "RTX", "LMT", "BA", "EMR", "ETN"],
    "Telecommunications": ["VZ", "T", "TMUS", "CHTR", "VOD", "TEF", "NTTYY", "CMCSA", "ORAN", "BTI"],
}

# Yahoo screener collection keys mapped to our industry names.
# These keys are public “collections” Yahoo exposes via its screener.
# They can change; we handle errors and fallback if they do.
SCREENER_KEYS = {
    "Technology": "all_technology",
    "Healthcare": "all_healthcare",
    "Finance": "all_financial",
    "Energy": "all_energy",
    "Consumer Goods": "all_consumer_goods",
    "Utilities": "all_utilities",
    "Real Estate": "all_real_estate",
    "Industrial": "all_industrials",
    "Telecommunications": "all_telecom",
}

def fetch_live_tickers_for_industry(industry: str, count: int = 8) -> List[str]:
    """
    Fetch tickers for an industry using Yahoo's public screener via yahooquery.
    Applies basic quality filters and samples diverse names.
    Falls back to curated list if needed.
    """
    screener_key = SCREENER_KEYS.get(industry)
    if not screener_key:
        # Unknown industry mapping; fallback
        return random.sample(FALLBACK_TICKERS.get(industry, []), min(count, len(FALLBACK_TICKERS.get(industry, []))))

    try:
        s = Screener()
        # Ask for up to ~200 symbols; we'll filter/sort locally
        data = s.get_screeners([screener_key], count=200)
        quotes = (data or {}).get(screener_key, {}).get("quotes", [])
        if not quotes:
            raise ValueError("No quotes returned")

        # Filter to US and reasonable liquidity/size
        filtered = []
        for q in quotes:
            symbol = q.get("symbol")
            market = q.get("market", "")
            cap = q.get("marketCap") or q.get("market_cap") or 0
            vol = q.get("averageDailyVolume3Month") or q.get("average_daily_volume_3month") or 0

            # Basic filters: US market, market cap >= $3B, avg vol >= 300k
            if not symbol:
                continue
            if not market or "us" not in market.lower():
                continue
            if cap and cap < 3_000_000_000:
                continue
            if vol and vol < 300_000:
                continue

            filtered.append(symbol)

        # Dedup + randomize for diversity
        filtered = list(dict.fromkeys(filtered))  # order-preserve dedup
        random.shuffle(filtered)

        # Sample requested count (or fewer if not enough)
        if not filtered:
            raise ValueError("Filtered list empty")

        return filtered[:count]

    except Exception as e:
        print(f"[industry_select] Live fetch failed for {industry}: {e}. Using fallback.")
        # Fallback curated sampling
        fallback = FALLBACK_TICKERS.get(industry, [])
        random.shuffle(fallback)
        return fallback[:count]

def fetch_tickers_by_industries(industries: List[str], per_industry: int = 5, max_total: int = 15) -> List[str]:
    """
    Aggregate tickers across selected industries with live fetch + filtering.
    Ensures diversity and caps total length.
    """
    all_syms: List[str] = []
    for ind in industries or []:
        syms = fetch_live_tickers_for_industry(ind, count=per_industry)
        all_syms.extend(syms)

    # If user chose no industry, diversify with a few across all categories
    if not industries:
        for ind in list(SCREENER_KEYS.keys())[:3]:  # grab a few categories to keep it short
            all_syms.extend(fetch_live_tickers_for_industry(ind, count=per_industry))

    # Dedup while preserving order, cap total
    seen = set()
    unique = []
    for s in all_syms:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    # Shuffle to avoid same ordering each run
    random.shuffle(unique)
    return unique[:max_total]
