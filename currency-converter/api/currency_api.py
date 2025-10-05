# filename: currency_api.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import json

app = FastAPI(title="Live Currency Converter API", version="3.0")

# ✅ API key (replace with your real one or set via environment variable in Vercel)
API_KEY = os.getenv("EXCHANGE_API_KEY", "1cf7de841184607a8664ef3e")
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

# ✅ Enable CORS (so frontend can call your API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load supported currencies from JSON file (you’ll create currencies.json)
try:
    with open("currencies.json", "r") as f:
        SUPPORTED_CURRENCIES = json.load(f)
except Exception:
    SUPPORTED_CURRENCIES = {}

@app.get("/")
def root():
    return {
        "message": "Currency Converter API is live!",
        "routes": ["/convert", "/currencies"],
        "credit": "API by JSK"
    }

@app.get("/convert")
def convert(amount: float = Query(...), from_currency: str = Query(...), to_currency: str = Query(...)):
    """
    Example: /convert?amount=100&from_currency=USD&to_currency=INR
    """
    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()
    except Exception as e:
        return {"error": "Failed to connect to ExchangeRate API", "details": str(e), "credit": "API by JSK"}

    if data.get("result") != "success":
        return {"error": "Failed to fetch exchange rates", "credit": "API by JSK"}

    rates = data.get("conversion_rates", {})

    if from_currency not in rates or to_currency not in rates:
        return {"error": "Invalid currency code", "credit": "API by JSK"}

    usd_amount = amount / rates[from_currency]
    converted = usd_amount * rates[to_currency]

    return {
        "query": {
            "amount": amount,
            "from": from_currency,
            "to": to_currency
        },
        "result": {
            "converted_amount": round(converted, 2),
            "rate": round(rates[to_currency] / rates[from_currency], 4)
        },
        "credit": "API by JSK"
    }

@app.get("/currencies")
def list_supported_currencies():
    """List all supported currency codes and names"""
    return {
        "count": len(SUPPORTED_CURRENCIES),
        "supported_currencies": SUPPORTED_CURRENCIES,
        "credit": "API by JSK"
    }
