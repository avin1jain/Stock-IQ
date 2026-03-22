from fastapi import APIRouter, HTTPException
import yfinance as yf
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

@router.get("/{symbol}")
def get_suggestion(symbol: str):
    try:
        sym = symbol.upper()
        info = yf.Ticker(sym).info

        # Gather all data
        name           = info.get("longName", sym)
        price          = info.get("currentPrice") or info.get("regularMarketPrice", 0)
        change_pct     = round(info.get("regularMarketChangePercent", 0), 2)
        pe_ratio       = info.get("trailingPE", None)
        pb_ratio       = info.get("priceToBook", None)
        roe            = info.get("returnOnEquity", None)
        debt_equity    = info.get("debtToEquity", None)
        profit_margins = info.get("profitMargins", None)
        revenue_growth = info.get("revenueGrowth", None)
        market_cap     = info.get("marketCap", 0)
        sector         = info.get("sector", "N/A")
        industry       = info.get("industry", "N/A")
        target_price   = info.get("targetMeanPrice", None)
        recommendation = info.get("recommendationKey", None)
        analyst_count  = info.get("numberOfAnalystOpinions", 0)
        free_cashflow  = info.get("freeCashflow", None)
        earnings_growth= info.get("earningsGrowth", None)
        beta           = info.get("beta", None)

        # Build analysis prompt
        prompt = f"""
You are a professional stock market analyst. Analyze this stock and give a clear investment suggestion.

Company: {name} ({sym})
Sector: {sector}
Industry: {industry}
Current Price: {price}
Today Change: {change_pct}%
P/E Ratio: {pe_ratio}
P/B Ratio: {pb_ratio}
ROE: {roe}
Debt/Equity: {debt_equity}
Profit Margin: {profit_margins}
Revenue Growth: {revenue_growth}
Earnings Growth: {earnings_growth}
Market Cap: {market_cap}
Analyst Target Price: {target_price}
Analyst Recommendation: {recommendation}
Number of Analysts: {analyst_count}
Beta (Volatility): {beta}
Free Cash Flow: {free_cashflow}

Based on all this data give:
1. VERDICT: One of these exactly: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
2. SCORE: A score out of 10 (e.g. 7.5/10)
3. SUMMARY: 2-3 sentences explaining the verdict in simple language
4. POSITIVES: 3 bullet points of good things about this stock
5. RISKS: 3 bullet points of risks or concerns
6. TARGET: Your 12 month price target estimate

Format your response exactly like this:
VERDICT: [verdict]
SCORE: [score]/10
SUMMARY: [summary]
POSITIVES:
- [point 1]
- [point 2]
- [point 3]
RISKS:
- [point 1]
- [point 2]
- [point 3]
TARGET: [price]
"""

        # Try OpenAI first
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "YOUR_KEY_HERE":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    max_tokens=500,
                    messages=[
                        {"role": "system", "content": "You are a professional stock market analyst. Be concise and accurate."},
                        {"role": "user", "content": prompt}
                    ]
                )
                ai_text = response.choices[0].message.content.strip()
                return parse_suggestion(ai_text, sym, name, price)
            except:
                pass

        # Fallback: rule based suggestion
        return rule_based_suggestion(sym, name, price, pe_ratio, roe, debt_equity, profit_margins, revenue_growth, change_pct, target_price, recommendation)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def parse_suggestion(text, sym, name, price):
    lines = text.strip().split("\n")
    result = {
        "symbol": sym,
        "name": name,
        "price": price,
        "verdict": "HOLD",
        "score": "5/10",
        "summary": "",
        "positives": [],
        "risks": [],
        "target": str(price),
        "source": "ai"
    }
    section = None
    for line in lines:
        line = line.strip()
        if line.startswith("VERDICT:"):
            result["verdict"] = line.replace("VERDICT:", "").strip()
        elif line.startswith("SCORE:"):
            result["score"] = line.replace("SCORE:", "").strip()
        elif line.startswith("SUMMARY:"):
            result["summary"] = line.replace("SUMMARY:", "").strip()
        elif line.startswith("POSITIVES:"):
            section = "positives"
        elif line.startswith("RISKS:"):
            section = "risks"
        elif line.startswith("TARGET:"):
            result["target"] = line.replace("TARGET:", "").strip()
        elif line.startswith("- ") and section == "positives":
            result["positives"].append(line[2:])
        elif line.startswith("- ") and section == "risks":
            result["risks"].append(line[2:])
    return result


def rule_based_suggestion(sym, name, price, pe, roe, debt, margins, growth, change, target, recommendation):
    score = 5.0
    positives = []
    risks = []

    if pe and pe < 15:
        score += 1
        positives.append(f"Low P/E ratio of {pe:.1f} suggests the stock may be undervalued")
    elif pe and pe > 40:
        score -= 0.5
        risks.append(f"High P/E ratio of {pe:.1f} means the stock is priced for perfection")

    if roe and roe > 0.15:
        score += 1
        positives.append(f"Strong ROE of {roe*100:.1f}% shows efficient use of capital")
    elif roe and roe < 0:
        score -= 1
        risks.append("Negative return on equity is a concern")

    if debt and debt < 50:
        score += 0.5
        positives.append(f"Low debt-to-equity of {debt:.0f}% indicates financial stability")
    elif debt and debt > 150:
        score -= 1
        risks.append(f"High debt level of {debt:.0f}% could be risky in rising rate environment")

    if margins and margins > 0.20:
        score += 1
        positives.append(f"Excellent profit margin of {margins*100:.1f}% shows pricing power")
    elif margins and margins < 0:
        score -= 1.5
        risks.append("Company is currently unprofitable with negative margins")

    if growth and growth > 0.15:
        score += 1
        positives.append(f"Strong revenue growth of {growth*100:.1f}% shows business momentum")
    elif growth and growth < 0:
        score -= 0.5
        risks.append("Revenue is declining which may impact future earnings")

    if change > 2:
        positives.append(f"Stock is up {change:.1f}% today showing strong market interest")
    elif change < -2:
        risks.append(f"Stock is down {abs(change):.1f}% today showing selling pressure")

    if not positives:
        positives = ["Company is an established player in its industry", "Has a track record of operations", "Listed on major exchange with good liquidity"]
    if not risks:
        risks = ["Market volatility can affect all stocks", "Macroeconomic factors may impact performance", "Competition in the sector remains intense"]

    score = max(1, min(10, score))

    if score >= 8:
        verdict = "STRONG BUY"
    elif score >= 6.5:
        verdict = "BUY"
    elif score >= 5:
        verdict = "HOLD"
    elif score >= 3:
        verdict = "SELL"
    else:
        verdict = "STRONG SELL"

    if recommendation:
        summary = f"Based on financial analysis, this stock gets a {verdict} rating with a score of {score:.1f}/10. Analyst consensus is {recommendation.upper()}."
    else:
        summary = f"Based on financial analysis, this stock gets a {verdict} rating with a score of {score:.1f}/10. Consider your risk tolerance before investing."

    return {
        "symbol": sym,
        "name": name,
        "price": price,
        "verdict": verdict,
        "score": f"{score:.1f}/10",
        "summary": summary,
        "positives": positives[:3],
        "risks": risks[:3],
        "target": str(round(price * 1.1, 2)) if price else "N/A",
        "source": "rules"
    }
