from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

SYMBOL_TO_NAME = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "WIPRO.NS": "Wipro",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank India",
    "ADANIENT.NS": "Adani Enterprises",
    "BAJFINANCE.NS": "Bajaj Finance",
    "TATASTEEL.NS": "Tata Steel",
    "JSWSTEEL.NS": "JSW Steel",
    "MARUTI.NS": "Maruti Suzuki",
    "TATAMOTORS.NS": "Tata Motors",
    "SUNPHARMA.NS": "Sun Pharma",
    "CIPLA.NS": "Cipla",
    "DRREDDY.NS": "Dr Reddy",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "ITC.NS": "ITC Limited",
    "TITAN.NS": "Titan Company",
    "ZOMATO.NS": "Zomato",
    "PAYTM.NS": "Paytm",
    "NYKAA.NS": "Nykaa",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "AXISBANK.NS": "Axis Bank",
    "ONGC.NS": "ONGC Oil",
    "BHARTIARTL.NS": "Bharti Airtel",
    "ASIANPAINT.NS": "Asian Paints",
    "HCLTECH.NS": "HCL Technologies",
    "TECHM.NS": "Tech Mahindra",
    "LTIM.NS": "LTIMindtree",
    "NTPC.NS": "NTPC Power",
    "POWERGRID.NS": "Power Grid India",
    "NESTLEIND.NS": "Nestle India",
    "DMART.NS": "DMart Avenue Supermarts",
    "SAIL.NS": "SAIL Steel",
    "HINDAL CO.NS": "Hindalco Industries",
    "INDUSINDBK.NS": "IndusInd Bank",
    "YESBANK.NS": "Yes Bank",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "BAJAJ-AUTO.NS": "Bajaj Auto",
    "EICHERMOT.NS": "Eicher Motors Royal Enfield",
    "HEROMOTOCO.NS": "Hero MotoCorp",
    "DIVISLAB.NS": "Divi's Laboratories",
    "AUROPHARMA.NS": "Aurobindo Pharma",
}

@router.get("/{symbol}")
def get_news(symbol: str):
    try:
        key = os.getenv("NEWS_API_KEY")
        if not key or key == "YOUR_KEY_HERE":
            return {"symbol": symbol.upper(), "articles": [], "error": "Add your NEWS_API_KEY to the .env file"}

        # Use company name for Indian stocks instead of symbol
        search_query = SYMBOL_TO_NAME.get(symbol.upper(), symbol.upper())
        # Remove .NS or .BO suffix for better search
        if search_query == symbol.upper():
            search_query = symbol.upper().replace(".NS", "").replace(".BO", "")

        r = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q":        search_query,
                "language": "en",
                "sortBy":   "publishedAt",
                "pageSize": 8,
                "apiKey":   key,
            },
            timeout=10
        )
        data = r.json()

        if data.get("status") != "ok":
            return {"symbol": symbol.upper(), "articles": []}

        articles = []
        for a in data.get("articles", []):
            articles.append({
                "title":     a.get("title", ""),
                "source":    a.get("source", {}).get("name", ""),
                "url":       a.get("url", ""),
                "date":      a.get("publishedAt", "")[:10],
                "summary":   a.get("description", ""),
                "sentiment": "neutral"
            })

        return {"symbol": symbol.upper(), "articles": articles}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
