from fastapi import APIRouter, HTTPException
import yfinance as yf

router = APIRouter()

@router.get("/{symbol}")
def get_insights(symbol: str):
    try:
        info = yf.Ticker(symbol.upper()).info
        change = info.get("regularMarketChangePercent", 0)
        pe = info.get("trailingPE", None)
        debt = info.get("debtToEquity", None)
        margins = info.get("profitMargins", None)
        growth = info.get("revenueGrowth", None)
        insights = []

        if change > 3:
            insights.append({"type": "positive", "text": f"Up {change:.1f}% today - strong buying momentum."})
        elif change > 0:
            insights.append({"type": "neutral", "text": f"Up {change:.1f}% today - mild positive movement."})
        elif change < -3:
            insights.append({"type": "warning", "text": f"Down {abs(change):.1f}% today - watch support levels."})
        else:
            insights.append({"type": "neutral", "text": f"Down {abs(change):.1f}% today - mild selling pressure."})

        if pe:
            if pe < 15:
                insights.append({"type": "positive", "text": f"P/E of {pe:.1f} is low - stock may be undervalued."})
            elif pe > 40:
                insights.append({"type": "warning", "text": f"P/E of {pe:.1f} is high - market expects big growth."})
            else:
                insights.append({"type": "neutral", "text": f"P/E of {pe:.1f} is in a normal range."})

        if debt:
            if debt > 150:
                insights.append({"type": "risk", "text": f"High debt ratio of {debt:.0f}% - monitor carefully."})
            elif debt < 50:
                insights.append({"type": "positive", "text": f"Low debt of {debt:.0f}% - healthy balance sheet."})

        if margins:
            if margins > 0.20:
                insights.append({"type": "positive", "text": f"Profit margin {margins*100:.1f}% - very profitable."})
            elif margins < 0:
                insights.append({"type": "risk", "text": "Company currently not profitable - negative margins."})

        if growth and growth > 0.15:
            insights.append({"type": "positive", "text": f"Revenue growing {growth*100:.1f}% - strong expansion."})

        if not insights:
            insights.append({"type": "neutral", "text": "No significant signals at this time."})

        return {"symbol": symbol.upper(), "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))