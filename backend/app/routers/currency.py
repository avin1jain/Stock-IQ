from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/rates")
def get_rates():
    """
    Gets real time USD to INR exchange rate
    """
    try:
        # Using a free exchange rate API
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/USD",
            timeout=10
        )
        data = response.json()
        usd_to_inr = data["rates"]["INR"]
        inr_to_usd = 1 / usd_to_inr

        return {
            "usd_to_inr": round(usd_to_inr, 2),
            "inr_to_usd": round(inr_to_usd, 6),
            "last_updated": data.get("date", ""),
        }
    except Exception as e:
        # Fallback rate if API fails
        return {
            "usd_to_inr": 83.50,
            "inr_to_usd": 0.011976,
            "last_updated": "fallback",
        }
