# ── weather.py ────────────────────────────────────────────────────────────────
# Fetch live weather forecast for any Indian city
# Uses Open-Meteo geocoding API to resolve city → coordinates dynamically
# No hardcoded location map — works for any city in the world
# ─────────────────────────────────────────────────────────────────────────────

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry  import Retry

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL  = "https://api.open-meteo.com/v1/forecast"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _session():
    """HTTP session with automatic retry on server errors."""
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=Retry(
        total            = 3,
        backoff_factor   = 2,
        status_forcelist = [500, 502, 503, 504]
    )))
    return s


def _geocode(location):
    """
    Convert any city / district / village name → (lat, lon, resolved_name).

    Uses Open-Meteo's free geocoding API — no API key needed.
    Biases results toward India by checking country_code == "IN" first,
    but falls back to any country if not found in India.

    Returns (lat, lon, name) or (None, None, None) if not found.
    """
    params = {
        "name"     : location,
        "count"    : 10,          # fetch top 10 — filter for India below
        "language" : "en",
        "format"   : "json"
    }

    try:
        resp    = _session().get(GEOCODING_URL, params=params, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results", [])

        if not results:
            return None, None, None

        # prefer Indian results
        india = [r for r in results if r.get("country_code") == "IN"]
        best  = india[0] if india else results[0]

        lat  = best.get("latitude")
        lon  = best.get("longitude")
        name = best.get("name", location)

        # build a readable name: "Nashik, Maharashtra, India"
        parts = [best.get("name"), best.get("admin1"), best.get("country")]
        full_name = ", ".join(p for p in parts if p)

        print(f"Weather      : geocoded {location!r} → {full_name} ({lat}, {lon})")
        return lat, lon, full_name

    except requests.RequestException as e:
        print(f"Weather      : geocoding error — {e}")
        return None, None, None


def _empty_result(location):
    return {
        "location"    : location,
        "temperature" : None,
        "rainfall_mm" : None,
        "humidity"    : None,
        "condition"   : None,
        "forecast"    : None,
        "source"      : "open-meteo.com"
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def get_weather(location):
    """
    Fetch current weather + 3-day forecast for any city.

    Input
    -----
    location : str | None — any city, district, or village name
               e.g. "Pune", "Nashik", "Wayanad", "Bathinda",
                    "Vidisha", "Osmanabad", "Tokyo" (works globally too)

    Output
    ------
    {
        "location"      : "Pune, Maharashtra, India",
        "temperature"   : "28°C",
        "rainfall_mm"   : "2.4",        ← current hour precipitation
        "humidity"      : "74%",
        "condition"     : "Currently 28°C, humidity 74%",
        "forecast"      : "Light rain expected — 18.2mm over 3 days",
        "daily_rain_mm" : [4.2, 8.1, 5.9],   ← per-day breakdown
        "temp_max"      : ["31°C", "30°C", "29°C"],
        "temp_min"      : ["22°C", "21°C", "21°C"],
        "source"        : "open-meteo.com"
    }

    Returns fields as None if API call fails.
    """

    if not location:
        print("Weather      : ⚠️  no location provided")
        return _empty_result(location)

    # ── Step 1: resolve city name → coordinates ───────────────────────────────
    lat, lon, resolved_name = _geocode(location)

    if lat is None or lon is None:
        print(f"Weather      : ⚠️  could not geocode {location!r}")
        return _empty_result(location)

    # ── Step 2: fetch weather forecast ───────────────────────────────────────
    params = {
        "latitude"      : lat,
        "longitude"     : lon,
        "current"       : "temperature_2m,relative_humidity_2m,precipitation",
        "daily"         : "precipitation_sum,temperature_2m_max,temperature_2m_min",
        "timezone"      : "Asia/Kolkata",
        "forecast_days" : 3,
    }

    try:
        resp = _session().get(FORECAST_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        daily   = data.get("daily",   {})

        temp      = current.get("temperature_2m",       "N/A")
        humidity  = current.get("relative_humidity_2m", "N/A")
        rainfall  = current.get("precipitation",        0)

        daily_rain = daily.get("precipitation_sum",    [0, 0, 0])
        temp_max   = daily.get("temperature_2m_max",   [])
        temp_min   = daily.get("temperature_2m_min",   [])
        total_rain = sum(r for r in daily_rain if r is not None)

        if total_rain > 20:
            forecast = f"Heavy rain expected — {total_rain:.1f}mm over 3 days"
        elif total_rain > 5:
            forecast = f"Light rain expected — {total_rain:.1f}mm over 3 days"
        else:
            forecast = "Mostly dry for next 3 days"

        result = {
            "location"      : resolved_name,
            "temperature"   : f"{temp}°C",
            "rainfall_mm"   : str(rainfall),
            "humidity"      : f"{humidity}%",
            "condition"     : f"Currently {temp}°C, humidity {humidity}%",
            "forecast"      : forecast,
            "daily_rain_mm" : daily_rain,
            "temp_max"      : [f"{t}°C" for t in temp_max],
            "temp_min"      : [f"{t}°C" for t in temp_min],
            "source"        : "open-meteo.com"
        }

        print(f"Weather      : ✅ {result['condition']}")
        print(f"Weather      : ✅ {result['forecast']}")
        return result

    except requests.RequestException as e:
        print(f"Weather      : ❌ forecast error — {e}")
        return _empty_result(resolved_name)


# ── Test ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    test_cases = [
        # location              note
        ("Pune",                "major city"),
        ("Amritsar",            "punjab"),
        ("Nashik",              "maharashtra district"),
        ("Wayanad",             "kerala district — was hardcoded before"),
        ("Vidisha",             "small MP district — not in any hardcoded list"),
        ("Bathinda",            "punjab farming district"),
        ("Osmanabad",           "marathwada — small city"),
        ("Somewhere Unknown",   "invalid city — expect None"),
        (None,                  "no location — expect None"),
    ]

    passed, failed, errors = 0, 0, []

    print("=" * 75)
    print(f"{'#':<3}  {'Location':<22} {'Temp':<8} {'Forecast':<40}  Status")
    print("-" * 75)

    for i, (loc, note) in enumerate(test_cases, 1):
        r    = get_weather(loc)
        temp = r.get("temperature")
        ok   = (temp is not None) if loc and "Unknown" not in str(loc) else (temp is None)

        status = "✅ PASS" if ok else "❌ FAIL"
        t_str  = str(temp)           if temp else "None"
        f_str  = str(r.get("forecast", ""))[:38] if r.get("forecast") else "None"

        print(f"{i:<3}  {str(loc):<22} {t_str:<8} {f_str:<40}  {status}  ({note})")

        if ok:
            passed += 1
        else:
            failed += 1
            errors.append({"test": i, "location": loc, "note": note, "result": r})

    print("=" * 75)
    print(f"\nResults : ✅ {passed} passed   ❌ {failed} failed   out of {len(test_cases)}")

    if errors:
        print("\nFailed cases:")
        for e in errors:
            print(f"\n  Test {e['test']} — {e['note']}")
            print(f"    location={e['location']!r}")
            print(f"    result={e['result']}")
    else:
        print("\n🎉 All tests passed!")