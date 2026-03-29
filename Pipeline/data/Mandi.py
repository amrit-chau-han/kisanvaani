import requests

try:
    API_KEY = dbutils.secrets.get(scope="kisanvaani", key="data_gov_api_key")
except:
    API_KEY = "579b464db66ec23bdd000001aee7d6da7d4b4ca97a9f21e6b212319d"

RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"   # agmarknet mandi dataset — fixed
BASE_URL    = f"https://api.data.gov.in/resource/{RESOURCE_ID}"


def get_mandi_price(crop, location):
    """
    Input : crop     = "onion"
            location = "Nashik"

    Output: {
                "crop"     : "onion",
                "location" : "Nashik",
                "price"    : "1200",
                "unit"     : "per quintal",
                "market"   : "Nashik APMC",
                "date"     : "2025-01-15",
                "source"   : "data.gov.in"
            }

    Note  : data has 1-2 day lag — prices are from yesterday or day before
    """

    params = {
        "api-key"            : API_KEY,
        "format"             : "json",
        "limit"              : "5",
        "filters[commodity]" : crop.title() if crop else "",
        "filters[market]"    : location if location else "",
    }

    print(f"Mandi        : fetching price for {crop} in {location}")

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data    = response.json()
        records = data.get("records", [])

        if not records:
            print(f"Mandi        : no records found for {crop} / {location}")
            return {
                "crop"     : crop,
                "location" : location,
                "price"    : None,
                "unit"     : "per quintal",
                "market"   : None,
                "date"     : None,
                "source"   : "data.gov.in"
            }

        # take the most recent record
        rec = records[0]

        result = {
            "crop"     : rec.get("commodity",    crop),
            "location" : rec.get("market",       location),
            "price"    : rec.get("modal_price"),
            "unit"     : "per quintal",
            "market"   : rec.get("market"),
            "date"     : rec.get("arrival_date"),
            "source"   : "data.gov.in"
        }

        print(f"Mandi        : price = ₹{result['price']} {result['unit']} on {result['date']}")
        return result

    except requests.RequestException as e:
        print(f"Mandi        : API error — {e}")
        return {
            "crop"     : crop,
            "location" : location,
            "price"    : None,
            "unit"     : "per quintal",
            "market"   : None,
            "date"     : None,
            "source"   : "data.gov.in"
        }


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — onion in Nashik
    r1 = get_mandi_price("onion", "Nashik")
    print(f"\n{r1}\n")

    # Test 2 — wheat in Amritsar
    r2 = get_mandi_price("wheat", "Amritsar")
    print(f"\n{r2}\n")

    # Test 3 — no location
    r3 = get_mandi_price("tomato", None)
    print(f"\n{r3}\n")