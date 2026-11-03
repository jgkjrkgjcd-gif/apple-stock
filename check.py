import os, requests

PART = os.environ["PART"]
ZIP = os.environ["ZIP"]
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

r = requests.get(
    "https://www.apple.com/jp/shop/fulfillment-messages",
    params={"pl": "true", "mts.0": "regular",
            "parts.0": PART, "location": ZIP},
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)
r.raise_for_status()
stores = r.json()["body"]["content"]["pickupMessage"]["stores"]

found = [s["storeName"] for s in stores
         if s["partsAvailability"][PART]["pickupDisplay"] == "available"]

print("在庫あり:", found or "なし")
if found:
    requests.post(
        WEBHOOK,
        json={"content": "🍎 在庫あり: " + ", ".join(found)},
        timeout=30,
    ).raise_for_status()
