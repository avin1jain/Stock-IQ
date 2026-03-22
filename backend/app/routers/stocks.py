from fastapi import APIRouter, HTTPException
import yfinance as yf
import numpy as np

router = APIRouter()

@router.get("/market/overview")
def market_overview():
    indices = [("S&P 500","^GSPC"),("NASDAQ","^IXIC"),("Dow Jones","^DJI")]
    result = []
    for name, sym in indices:
        try:
            info = yf.Ticker(sym).info
            result.append({
                "name": name,
                "price": info.get("regularMarketPrice", 0),
                "change_pct": round(info.get("regularMarketChangePercent", 0), 2)
            })
        except:
            pass
    return {"indices": result}

@router.get("/{symbol}/history")
def get_history(symbol: str, period: str = "3mo"):
    try:
        hist = yf.Ticker(symbol.upper()).history(period=period)
        if hist.empty:
            raise HTTPException(status_code=404, detail="No data found")
        result = []
        for date, row in hist.iterrows():
            result.append({
                "date":  date.strftime("%Y-%m-%d"),
                "open":  round(float(row["Open"]),  2),
                "close": round(float(row["Close"]), 2),
                "high":  round(float(row["High"]),  2),
                "low":   round(float(row["Low"]),   2),
            })
        return {"symbol": symbol.upper(), "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}")
def get_stock(symbol: str):
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info

        # Check if stock actually exists
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        name  = info.get("longName") or info.get("shortName")

        if not price or not name or price == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Stock '{symbol}' not found. Please check the symbol and try again."
            )

        return {
            "symbol":     symbol.upper(),
            "name":       name,
            "price":      price,
            "change_pct": round(info.get("regularMarketChangePercent", 0), 2),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio":   info.get("trailingPE", None),
            "high_52w":   info.get("fiftyTwoWeekHigh", None),
            "low_52w":    info.get("fiftyTwoWeekLow",  None),
            "sector":     info.get("sector", "N/A"),
            "about":      info.get("longBusinessSummary", "")[:200],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Stock '{symbol}' not found. Please check the symbol and try again."
        )
