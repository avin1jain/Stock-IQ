from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StockIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://stockiq-beta.vercel.app",
        "https://stockiq.vercel.app",
        "https://stockiq-avin1jain.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import stocks, news, predict, insights, search, financials, competitors, currency, suggestion

app.include_router(stocks.router,      prefix="/api/stocks",      tags=["Stocks"])
app.include_router(news.router,        prefix="/api/news",        tags=["News"])
app.include_router(predict.router,     prefix="/api/predict",     tags=["Predict"])
app.include_router(insights.router,    prefix="/api/insights",    tags=["Insights"])
app.include_router(search.router,      prefix="/api/search",      tags=["Search"])
app.include_router(financials.router,  prefix="/api/financials",  tags=["Financials"])
app.include_router(competitors.router, prefix="/api/competitors", tags=["Competitors"])
app.include_router(currency.router,    prefix="/api/currency",    tags=["Currency"])
app.include_router(suggestion.router,  prefix="/api/suggestion",  tags=["Suggestion"])

@app.get("/")
def home():
    return {"message": "StockIQ is running!"}
