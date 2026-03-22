from fastapi import APIRouter, HTTPException
import yfinance as yf

router = APIRouter()

@router.get("/{symbol}")
def get_financials(symbol: str):
    try:
        info = yf.Ticker(symbol.upper()).info
        return {
            "symbol": symbol.upper(),
            "pe_ratio":        info.get("trailingPE", None),
            "pb_ratio":        info.get("priceToBook", None),
            "roe":             info.get("returnOnEquity", None),
            "profit_margins":  info.get("profitMargins", None),
            "debt_to_equity":  info.get("debtToEquity", None),
            "revenue_growth":  info.get("revenueGrowth", None),
            "market_cap":      info.get("marketCap", None),
            "earnings_growth": info.get("earningsGrowth", None),
            "current_ratio":   info.get("currentRatio", None),
            "revenue":         info.get("totalRevenue", None),
            "gross_profits":   info.get("grossProfits", None),
            "ebitda":          info.get("ebitda", None),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
