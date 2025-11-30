import random
import os
USE_SERPAPI = bool(os.getenv("SERPAPI_KEY"))
if USE_SERPAPI:
    import requests

def mock_price(item):
    return {"item": item, "price": round(random.uniform(1,5),2), "store":"MockMart"}

def serpapi_price(item):
    try:
        resp = requests.get("https://serpapi.com/search", params={"engine":"google_shopping","q":item,"api_key":os.getenv("SERPAPI_KEY")}, timeout=10)
        data = resp.json()
        entry = data["shopping_results"][0]
        price_str = entry.get("price","")
        price = float(''.join(c for c in price_str if c.isdigit() or c=='.') or 1.0)
        return {"item": item, "price": price, "store": entry.get("source","Store")}
    except:
        return mock_price(item)

def price_lookup(item):
    if USE_SERPAPI:
        return serpapi_price(item)
    return mock_price(item)
