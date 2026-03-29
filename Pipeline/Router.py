from data.Mandi    import get_mandi_price
from data.weather  import get_weather
from data.schemes  import get_scheme_info
from data.advisory import get_advisory


def route(intent):
    """
    Input : intent dict from intent.py
            {
                "crop"          : "onion",
                "location"      : "Nashik",
                "situation"     : "price inquiry",
                "question_type" : "price/weather/scheme/advisory"
            }

    Output: raw data dict from the right data source
            passed directly to answer.py
    """

    question_type = intent.get("question_type", "advisory")
    crop          = intent.get("crop")
    location      = intent.get("location")

    print(f"Router       : question_type = {question_type}")
    print(f"Router       : crop = {crop}, location = {location}")

    if question_type == "price":
        data = get_mandi_price(crop, location)

    elif question_type == "weather":
        data = get_weather(location)

    elif question_type == "scheme":
        data = get_scheme_info(intent.get("situation"))

    elif question_type == "advisory":
        data = get_advisory(crop, intent.get("situation"))

    else:
        # fallback — should never happen if intent.py is working
        data = get_advisory(crop, intent.get("situation"))

    print(f"Router       : data source returned {type(data).__name__}")
    return data


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — price routing
    r1 = route({
        "crop"          : "onion",
        "location"      : "Nashik",
        "situation"     : "price inquiry",
        "question_type" : "price"
    })
    print(f"\n{r1}\n")

    # Test 2 — weather routing
    r2 = route({
        "crop"          : None,
        "location"      : "Pune",
        "situation"     : "rain forecast",
        "question_type" : "weather"
    })
    print(f"\n{r2}\n")

    # Test 3 — scheme routing
    r3 = route({
        "crop"          : None,
        "location"      : None,
        "situation"     : "PM Kisan application",
        "question_type" : "scheme"
    })
    print(f"\n{r3}\n")

    # Test 4 — advisory routing
    r4 = route({
        "crop"          : "cotton",
        "location"      : "Maharashtra",
        "situation"     : "sowing time advice",
        "question_type" : "advisory"
    })
    print(f"\n{r4}\n")