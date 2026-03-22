from fastapi import APIRouter
router = APIRouter()

SYMBOLS = {
    # US Stocks
    "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL",
    "alphabet": "GOOGL", "tesla": "TSLA", "amazon": "AMZN",
    "nvidia": "NVDA", "meta": "META", "facebook": "META",
    "netflix": "NFLX", "uber": "UBER", "airbnb": "ABNB",
    "spotify": "SPOT", "disney": "DIS", "nike": "NKE",
    "coca cola": "KO", "pepsi": "PEP", "intel": "INTC",
    "amd": "AMD", "paypal": "PYPL", "visa": "V",
    "mastercard": "MA", "jpmorgan": "JPM", "goldman sachs": "GS",
    "bank of america": "BAC", "walmart": "WMT", "target": "TGT",
    "costco": "COST", "johnson": "JNJ", "pfizer": "PFE",
    "moderna": "MRNA", "exxon": "XOM", "chevron": "CVX",

    # Indian IT
    "tcs": "TCS.NS", "tata consultancy": "TCS.NS",
    "infosys": "INFY.NS", "infy": "INFY.NS",
    "wipro": "WIPRO.NS", "hcl": "HCLTECH.NS",
    "hcl tech": "HCLTECH.NS", "hcltech": "HCLTECH.NS",
    "tech mahindra": "TECHM.NS", "techm": "TECHM.NS",
    "ltimindtree": "LTIM.NS", "lti": "LTIM.NS",
    "mphasis": "MPHASIS.NS", "persistent": "PERSISTENT.NS",
    "coforge": "COFORGE.NS", "hexaware": "HEXAWARE.NS",

    # Indian Banks
    "hdfc": "HDFCBANK.NS", "hdfc bank": "HDFCBANK.NS",
    "icici": "ICICIBANK.NS", "icici bank": "ICICIBANK.NS",
    "sbi": "SBIN.NS", "state bank": "SBIN.NS",
    "kotak": "KOTAKBANK.NS", "kotak bank": "KOTAKBANK.NS",
    "axis bank": "AXISBANK.NS", "axis": "AXISBANK.NS",
    "indusind": "INDUSINDBK.NS", "indusind bank": "INDUSINDBK.NS",
    "yes bank": "YESBANK.NS", "bandhan": "BANDHANBNK.NS",
    "pnb": "PNB.NS", "punjab national": "PNB.NS",
    "bank of baroda": "BANKBARODA.NS", "canara": "CANBK.NS",

    # Indian Energy & Conglomerates
    "reliance": "RELIANCE.NS", "reliance industries": "RELIANCE.NS",
    "ongc": "ONGC.NS", "oil india": "OIL.NS",
    "bpcl": "BPCL.NS", "ioc": "IOC.NS", "indian oil": "IOC.NS",
    "gail": "GAIL.NS", "petronet": "PETRONET.NS",
    "adani": "ADANIENT.NS", "adani enterprises": "ADANIENT.NS",
    "adani ports": "ADANIPORTS.NS", "adani green": "ADANIGREEN.NS",
    "adani power": "ADANIPOWER.NS", "adani total": "ADANITOTAL.NS",
    "adani wilmar": "AWL.NS",

    # Indian Metals & Mining
    "tata steel": "TATASTEEL.NS", "tatasteel": "TATASTEEL.NS",
    "jsw steel": "JSWSTEEL.NS", "jsw": "JSWSTEEL.NS",
    "sail": "SAIL.NS", "steel authority": "SAIL.NS",
    "hindalco": "HINDALCO.NS", "vedanta": "VEDL.NS",
    "vedl": "VEDL.NS", "sterlite": "VEDL.NS",
    "nmdc": "NMDC.NS", "coal india": "COALINDIA.NS",
    "jindal steel": "JINDALSTEL.NS", "jspl": "JINDALSTEL.NS",

    # Indian Auto
    "maruti": "MARUTI.NS", "maruti suzuki": "MARUTI.NS",
    "tata motors": "TATAMOTORS.NS", "tatamotors": "TATAMOTORS.NS",
    "mahindra": "M&M.NS", "m&m": "M&M.NS",
    "bajaj auto": "BAJAJ-AUTO.NS", "bajaj": "BAJFINANCE.NS",
    "hero motocorp": "HEROMOTOCO.NS", "hero": "HEROMOTOCO.NS",
    "eicher": "EICHERMOT.NS", "royal enfield": "EICHERMOT.NS",
    "tvs motor": "TVSMOTOR.NS", "tvs": "TVSMOTOR.NS",
    "ashok leyland": "ASHOKLEY.NS",

    # Indian Aviation
    "indigo": "INDIGO.NS", "interglobe": "INDIGO.NS",
    "spicejet": "SPICEJET.NS", "spice jet": "SPICEJET.NS",
    "air india": "AIRINDIA.NS",

    # Indian Pharma
    "sun pharma": "SUNPHARMA.NS", "sunpharma": "SUNPHARMA.NS",
    "cipla": "CIPLA.NS", "dr reddy": "DRREDDY.NS",
    "drreddy": "DRREDDY.NS", "divi": "DIVISLAB.NS",
    "aurobindo": "AUROPHARMA.NS", "lupin": "LUPIN.NS",
    "torrent pharma": "TORNTPHARM.NS", "abbott india": "ABBOTINDIA.NS",
    "biocon": "BIOCON.NS", "glenmark": "GLENMARK.NS",
    "ipca": "IPCALAB.NS", "alkem": "ALKEM.NS",

    # Indian FMCG
    "hindustan unilever": "HINDUNILVR.NS", "hul": "HINDUNILVR.NS",
    "itc": "ITC.NS", "nestle": "NESTLEIND.NS", "nestle india": "NESTLEIND.NS",
    "dabur": "DABUR.NS", "marico": "MARICO.NS",
    "godrej consumer": "GODREJCP.NS", "godrej": "GODREJCP.NS",
    "colgate": "COLPAL.NS", "colgate palmolive": "COLPAL.NS",
    "emami": "EMAMILTD.NS", "britannia": "BRITANNIA.NS",
    "varun beverages": "VBL.NS",

    # Indian Telecom
    "airtel": "BHARTIARTL.NS", "bharti airtel": "BHARTIARTL.NS",
    "jio": "RELIANCE.NS", "vodafone idea": "IDEA.NS",
    "vi": "IDEA.NS", "idea": "IDEA.NS",

    # Indian Retail & Consumer
    "dmart": "DMART.NS", "avenue supermarts": "DMART.NS",
    "titan": "TITAN.NS", "asian paints": "ASIANPAINT.NS",
    "berger paints": "BERGEPAINT.NS", "pidilite": "PIDILITIND.NS",
    "havells": "HAVELLS.NS", "voltas": "VOLTAS.NS",
    "blue star": "BLUESTARCO.NS", "whirlpool": "WHIRLPOOL.NS",
    "dixon": "DIXON.NS",

    # Indian Fintech & New Age
    "zomato": "ZOMATO.NS", "paytm": "PAYTM.NS",
    "nykaa": "NYKAA.NS", "policybazaar": "POLICYBZR.NS",
    "ola": "OLAELEC.NS", "ola electric": "OLAELEC.NS",
    "swiggy": "SWIGGY.NS",

    # Indian Infrastructure
    "larsen": "LT.NS", "l&t": "LT.NS", "larsen toubro": "LT.NS",
    "ultratech": "ULTRACEMCO.NS", "ultratech cement": "ULTRACEMCO.NS",
    "ambuja cement": "AMBUJACEM.NS", "acc": "ACC.NS",
    "shree cement": "SHREECEM.NS", "ntpc": "NTPC.NS",
    "power grid": "POWERGRID.NS", "bhel": "BHEL.NS",

    # Indian Healthcare
    "apollo hospitals": "APOLLOHOSP.NS", "apollo": "APOLLOHOSP.NS",
    "max healthcare": "MAXHEALTH.NS", "fortis": "FORTIS.NS",
    "narayana": "NH.NS", "aster dm": "ASTERDM.NS",

    # Indian Insurance
    "lic": "LICI.NS", "sbi life": "SBILIFE.NS",
    "hdfc life": "HDFCLIFE.NS", "icici prudential": "ICICIPRULI.NS",
    "bajaj allianz": "BAJAJALLIANZ.NS",

    # Indian Exchanges & Finance
    "nse": "NSEI", "bse": "BSE.NS",
    "hdfc amc": "HDFCAMC.NS", "nippon": "NAM-INDIA.NS",
    "muthoot": "MUTHOOTFIN.NS", "muthoot finance": "MUTHOOTFIN.NS",
    "bajaj finance": "BAJFINANCE.NS", "bajaj finserv": "BAJAJFINSV.NS",
    "shriram finance": "SHRIRAMFIN.NS",
}

@router.get("/{query}")
def search_symbol(query: str):
    lower = query.lower().strip()

    # Exact match first
    if lower in SYMBOLS:
        return {"query": query, "symbol": SYMBOLS[lower]}

    # Partial match
    for name, symbol in SYMBOLS.items():
        if lower in name or name in lower:
            return {"query": query, "symbol": symbol}

    # If nothing found just return the query as uppercase
    # It might be a valid symbol like VEDL, INDIGO etc
    return {"query": query, "symbol": query.upper().strip()}
