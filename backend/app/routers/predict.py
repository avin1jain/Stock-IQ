from fastapi import APIRouter, HTTPException
import yfinance as yf
import numpy as np

router = APIRouter()

@router.get("/{symbol}")
def predict_trend(symbol: str):
    try:
        hist = yf.Ticker(symbol.upper()).history(period="3mo")
        closes = hist["Close"].values
        ma20 = float(np.mean(closes[-20:])) if len(closes) >= 20 else float(closes[-1])
        ma50 = float(np.mean(closes[-50:])) if len(closes) >= 50 else ma20
        last = float(closes[-1])
        if ma20 > ma50:
            trend = "bullish"
            confidence = round(min((ma20 - ma50) / ma50 * 500, 92), 1)
        else:
            trend = "bearish"
            confidence = round(min((ma50 - ma20) / ma50 * 500, 92), 1)
        return {
            "symbol": symbol.upper(),
            "trend": trend,
            "confidence": confidence,
            "last_price": round(last, 2),
            "ma20": round(ma20, 2),
            "ma50": round(ma50, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))