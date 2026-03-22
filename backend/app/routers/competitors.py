from fastapi import APIRouter, HTTPException
import yfinance as yf
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

def get_competitors_ai(symbol: str, name: str, sector: str, industry: str):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial expert. Return only stock ticker symbols separated by commas. No explanations. For Indian stocks use NSE format with .NS suffix."
                },
                {
                    "role": "user",
                    "content": f"Give me exactly 4 main competitor stock symbols for {name} ({symbol}) in the {industry} industry. Return only ticker symbols separated by commas like: SYM1,SYM2,SYM3,SYM4"
                }
            ]
        )
        result = response.choices[0].message.content.strip()
        symbols = [s.strip().upper() for s in result.split(",")]
        return symbols[:4]
    except:
        return []

FALLBACK_COMPETITORS = {
    "AAPL": ["MSFT", "GOOGL", "META", "AMZN"],
    "MSFT": ["AAPL", "GOOGL", "AMZN", "META"],
    "GOOGL": ["META", "MSFT", "AAPL", "AMZN"],
    "TSLA": ["F", "GM", "RIVN", "NIO"],
    "NVDA": ["AMD", "INTC", "QCOM", "TSM"],
    "AMZN": ["WMT", "SHOP", "BABA", "TGT"],
    "META": ["SNAP", "GOOGL", "PINS", "TWTR"],
    "NFLX": ["DIS", "WBD", "PARA", "SPOT"],
    "TCS.NS": ["INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
    "INFY.NS": ["TCS.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
    "WIPRO.NS": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "TECHM.NS"],
    "HCLTECH.NS": ["TCS.NS", "INFY.NS", "WIPRO.NS", "TECHM.NS"],
    "TECHM.NS": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS"],
    "LTIM.NS": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS"],
    "RELIANCE.NS": ["ONGC.NS", "BPCL.NS", "IOC.NS", "GAIL.NS"],
    "TATASTEEL.NS": ["JSWSTEEL.NS", "SAIL.NS", "HINDALCO.NS", "JINDALSTEL.NS"],
"NFLX": ["DIS", "WBD", "PARA", "SPOT"],
"TSM": ["NVDA", "INTC", "AMAT", "ASML"],
    "ASML": ["TSM", "AMAT", "LRCX", "KLAC"],
    "INTC": ["AMD", "NVDA", "QCOM", "TSM"],
    "AMD": ["NVDA", "INTC", "QCOM", "TSM"],
    "QCOM": ["INTC", "AMD", "NVDA", "AVGO"],
    "AVGO": ["QCOM", "INTC", "AMD", "NVDA"],
    "CRM": ["SAP", "ORCL", "MSFT", "NOW"],
    "ORCL": ["CRM", "SAP", "MSFT", "IBM"],
    "IBM": ["ORCL", "MSFT", "GOOGL", "HPE"],
    "SHOP": ["AMZN", "ETSY", "WMT", "TGT"],
    "PYPL": ["V", "MA", "SQ", "AFRM"],
    "SQ": ["PYPL", "V", "MA", "AFRM"],
    "SNAP": ["META", "PINS", "TWTR", "GOOGL"],
    "PINS": ["META", "SNAP", "GOOGL", "TWTR"],
    "UBER": ["LYFT", "GRAB", "DIDI", "ABNB"],
    "LYFT": ["UBER", "GRAB", "DIDI", "ABNB"],
    "ABNB": ["BKNG", "EXPE", "TRIP", "UBER"],
    "BKNG": ["ABNB", "EXPE", "TRIP", "PCLN"],
    "SPOT": ["AAPL", "AMZN", "GOOGL", "NFLX"],
    "COIN": ["MSTR", "RIOT", "MARA", "HUT"],
    "JPM": ["GS", "BAC", "MS", "C"],
    "GS": ["JPM", "MS", "BAC", "C"],
    "BAC": ["JPM", "GS", "MS", "WFC"],
    "V": ["MA", "PYPL", "SQ", "AXP"],
    "MA": ["V", "PYPL", "SQ", "AXP"],
    "JNJ": ["PFE", "MRK", "ABBV", "BMY"],
    "PFE": ["JNJ", "MRK", "ABBV", "MRNA"],
    "MRNA": ["PFE", "JNJ", "BNTX", "NVAX"],
    "XOM": ["CVX", "SHEL", "BP", "COP"],
    "CVX": ["XOM", "SHEL", "BP", "COP"],
    "WMT": ["TGT", "COST", "AMZN", "SHOP"],
    "TGT": ["WMT", "COST", "AMZN", "SHOP"],
    "DIS": ["NFLX", "WBD", "PARA", "CMCSA"],
    "NKE": ["ADDYY", "PUMA", "UAA", "SKX"],
    "F": ["GM", "TSLA", "RIVN", "STLA"],
    "GM": ["F", "TSLA", "RIVN", "STLA"],
    "JSWSTEEL.NS": ["TATASTEEL.NS", "SAIL.NS", "HINDALCO.NS", "JINDALSTEL.NS"],
    "SAIL.NS": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "JINDALSTEL.NS"],
    "JINDALSTEL.NS": ["TATASTEEL.NS", "JSWSTEEL.NS", "SAIL.NS", "HINDALCO.NS"],
    "VEDL.NS": ["HINDALCO.NS", "NMDC.NS", "COALINDIA.NS", "JINDALSTEL.NS"],
    "HINDALCO.NS": ["VEDL.NS", "NMDC.NS", "TATASTEEL.NS", "JINDALSTEL.NS"],
    "HDFCBANK.NS": ["ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    "ICICIBANK.NS": ["HDFCBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    "SBIN.NS": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    "KOTAKBANK.NS": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS"],
    "AXISBANK.NS": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS"],
    "INDUSINDBK.NS": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "YESBANK.NS"],
    "YESBANK.NS": ["INDUSINDBK.NS", "AXISBANK.NS", "BANDHANBNK.NS", "PNB.NS"],
    "INDIGO.NS": ["SPICEJET.NS", "AIRINDIA.NS", "BLUEDART.NS", "AKASAAIR.NS"],
    "SPICEJET.NS": ["INDIGO.NS", "AIRINDIA.NS", "BLUEDART.NS", "AKASAAIR.NS"],
    "MARUTI.NS": ["TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS"],
    "TATAMOTORS.NS": ["MARUTI.NS", "M&M.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS"],
    "BAJAJ-AUTO.NS": ["HEROMOTOCO.NS", "TVSMOTOR.NS", "EICHERMOT.NS", "MARUTI.NS"],
    "HEROMOTOCO.NS": ["BAJAJ-AUTO.NS", "TVSMOTOR.NS", "EICHERMOT.NS", "M&M.NS"],
    "TVSMOTOR.NS": ["HEROMOTOCO.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "MARUTI.NS"],
    "EICHERMOT.NS": ["HEROMOTOCO.NS", "BAJAJ-AUTO.NS", "TVSMOTOR.NS", "MARUTI.NS"],
    "SUNPHARMA.NS": ["CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS", "AUROPHARMA.NS"],
    "CIPLA.NS": ["SUNPHARMA.NS", "DRREDDY.NS", "DIVISLAB.NS", "LUPIN.NS"],
    "DRREDDY.NS": ["SUNPHARMA.NS", "CIPLA.NS", "DIVISLAB.NS", "LUPIN.NS"],
    "LUPIN.NS": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "AUROPHARMA.NS"],
    "DIVISLAB.NS": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "LUPIN.NS"],
    "BIOCON.NS": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS"],
    "HINDUNILVR.NS": ["ITC.NS", "NESTLEIND.NS", "DABUR.NS", "MARICO.NS"],
    "ITC.NS": ["HINDUNILVR.NS", "NESTLEIND.NS", "DABUR.NS", "MARICO.NS"],
    "NESTLEIND.NS": ["HINDUNILVR.NS", "ITC.NS", "DABUR.NS", "BRITANNIA.NS"],
    "DABUR.NS": ["HINDUNILVR.NS", "MARICO.NS", "GODREJCP.NS", "EMAMILTD.NS"],
    "MARICO.NS": ["HINDUNILVR.NS", "DABUR.NS", "GODREJCP.NS", "COLPAL.NS"],
    "BRITANNIA.NS": ["NESTLEIND.NS", "ITC.NS", "HINDUNILVR.NS", "DABUR.NS"],
    "ADANIENT.NS": ["RELIANCE.NS", "ADANIPORTS.NS", "ADANIGREEN.NS", "ADANIPOWER.NS"],
    "ADANIPORTS.NS": ["ADANIENT.NS", "ADANIGREEN.NS", "GMRINFRA.NS", "IRB.NS"],
    "BAJFINANCE.NS": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "MUTHOOTFIN.NS"],
    "BAJAJFINSV.NS": ["BAJFINANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBILIFE.NS"],
    "MUTHOOTFIN.NS": ["BAJFINANCE.NS", "SHRIRAMFIN.NS", "MANAPPURAM.NS", "IIFL.NS"],
    "TITAN.NS": ["ASIANPAINT.NS", "HINDUNILVR.NS", "MARICO.NS", "DABUR.NS"],
    "ASIANPAINT.NS": ["BERGEPAINT.NS", "KANSAINER.NS", "PIDILITIND.NS", "AKZOINDIA.NS"],
    "ZOMATO.NS": ["SWIGGY.NS", "PAYTM.NS", "NYKAA.NS", "POLICYBZR.NS"],
    "PAYTM.NS": ["ZOMATO.NS", "POLICYBZR.NS", "NYKAA.NS", "BAJFINANCE.NS"],
    "NYKAA.NS": ["ZOMATO.NS", "PAYTM.NS", "POLICYBZR.NS", "DMART.NS"],
    "DMART.NS": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
    "LT.NS": ["ULTRACEMCO.NS", "BHEL.NS", "SIEMENS.NS", "ABB.NS"],
    "NTPC.NS": ["POWERGRID.NS", "ADANIGREEN.NS", "TATAPOWER.NS", "CESC.NS"],
    "POWERGRID.NS": ["NTPC.NS", "ADANIGREEN.NS", "TATAPOWER.NS", "CESC.NS"],
    "APOLLOHOSP.NS": ["MAXHEALTH.NS", "FORTIS.NS", "NH.NS", "ASTERDM.NS"],
    "MAXHEALTH.NS": ["APOLLOHOSP.NS", "FORTIS.NS", "NH.NS", "ASTERDM.NS"],
    "LICI.NS": ["SBILIFE.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "MAXFINSERV.NS"],
    "SBILIFE.NS": ["LICI.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "BAJAJFINSV.NS"],
    "HDFCLIFE.NS": ["LICI.NS", "SBILIFE.NS", "ICICIPRULI.NS", "BAJAJFINSV.NS"],
    "BHARTIARTL.NS": ["IDEA.NS", "RELIANCE.NS", "TATACOMM.NS", "HFCL.NS"],
    "IDEA.NS": ["BHARTIARTL.NS", "RELIANCE.NS", "TATACOMM.NS", "HFCL.NS"],
    "ONGC.NS": ["RELIANCE.NS", "BPCL.NS", "IOC.NS", "GAIL.NS"],
    "BPCL.NS": ["IOC.NS", "ONGC.NS", "GAIL.NS", "RELIANCE.NS"],
    "IOC.NS": ["BPCL.NS", "ONGC.NS", "GAIL.NS", "RELIANCE.NS"],
    "COALINDIA.NS": ["NMDC.NS", "VEDL.NS", "HINDCOPPER.NS", "MOIL.NS"],
    "NMDC.NS": ["COALINDIA.NS", "VEDL.NS", "SAIL.NS", "TATASTEEL.NS"],
    "HAVELLS.NS": ["VOLTAS.NS", "BLUESTARCO.NS", "DIXON.NS", "WHIRLPOOL.NS"],
    "PIDILITIND.NS": ["ASIANPAINT.NS", "BERGEPAINT.NS", "KANSAINER.NS", "AKZOINDIA.NS"],
}

@router.get("/{symbol}")
def get_competitors(symbol: str):
    sym = symbol.upper()

    try:
        info = yf.Ticker(sym).info
        name     = info.get("longName", sym)
        sector   = info.get("sector", "")
        industry = info.get("industry", "")
    except:
        name = sym
        sector = ""
        industry = ""

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "YOUR_KEY_HERE":
        try:
            competitor_symbols = get_competitors_ai(sym, name, sector, industry)
            if competitor_symbols:
                results = []
                for comp in competitor_symbols:
                    try:
                        cinfo = yf.Ticker(comp).info
                        cprice = cinfo.get("currentPrice") or cinfo.get("regularMarketPrice", 0)
                        if cprice and cprice > 0:
                            results.append({
                                "symbol":         comp,
                                "name":           cinfo.get("longName", comp),
                                "price":          cprice,
                                "change_pct":     round(cinfo.get("regularMarketChangePercent", 0), 2),
                                "market_cap":     cinfo.get("marketCap", 0),
                                "pe_ratio":       cinfo.get("trailingPE", None),
                                "profit_margins": cinfo.get("profitMargins", None),
                            })
                    except:
                        pass
                if results:
                    return {"symbol": sym, "competitors": results, "source": "ai"}
        except:
            pass

    competitors = FALLBACK_COMPETITORS.get(sym, [])
    if not competitors:
        return {"symbol": sym, "competitors": [], "message": "No competitor data found"}

    results = []
    for comp in competitors:
        try:
            cinfo = yf.Ticker(comp).info
            cprice = cinfo.get("currentPrice") or cinfo.get("regularMarketPrice", 0)
            if cprice and cprice > 0:
                results.append({
                    "symbol":         comp,
                    "name":           cinfo.get("longName", comp),
                    "price":          cprice,
                    "change_pct":     round(cinfo.get("regularMarketChangePercent", 0), 2),
                    "market_cap":     cinfo.get("marketCap", 0),
                    "pe_ratio":       cinfo.get("trailingPE", None),
                    "profit_margins": cinfo.get("profitMargins", None),
                })
        except:
            pass

    return {"symbol": sym, "competitors": results, "source": "fallback"}
