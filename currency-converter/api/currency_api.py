from fastapi import FastAPI, Query
import requests

app = FastAPI()

API_URL = "https://v6.exchangerate-api.com/v6/1cf7de841184607a8664ef3e/latest/USD"

@app.get("/")
def root():
    return {"message": "Currency Converter API is live!"}

@app.get("/convert")
def convert(amount: float = Query(...), from_currency: str = Query(...), to_currency: str = Query(...)):
    """
    Example: /convert?amount=100&from_currency=USD&to_currency=INR
    """
    response = requests.get(API_URL)
    data = response.json()

    if data["result"] != "success":
        return {"error": "Failed to fetch exchange rates"}

    rates = data["conversion_rates"]

    if from_currency not in rates or to_currency not in rates:
        return {"error": "Invalid currency code"}

    usd_amount = amount / rates[from_currency]
    converted = usd_amount * rates[to_currency]

    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted_amount": round(converted, 2),
        "rate": round(rates[to_currency] / rates[from_currency], 4)
    }
