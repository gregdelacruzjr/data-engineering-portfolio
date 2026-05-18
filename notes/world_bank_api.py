import requests
import json

# World Bank API - Philippine economic indicators
COUNTRY_CODE = "PH"
BASE_URL = "https://api.worldbank.org/v2"

def get_indicator(indicator_code, indicator_name):
    """Fetch a single indicator from the World Bank API."""
    url = f"{BASE_URL}/country/{COUNTRY_CODE}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "per_page": 10,
        "mrv": 10  # most recent 10 values
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        records = data[1]  # index 0 is metadata, index 1 is the data
        print(f"\n{indicator_name}")
        print("-" * 40)
        for record in records:
            if record["value"] is not None:
                print(f"  {record['date']}: {record['value']:.2f}")
    else:
        print(f"Error fetching {indicator_name}: {response.status_code}")

def main():
    print("Philippine Economic Indicators — World Bank API")
    print("=" * 50)

    indicators = {
    "NY.GDP.MKTP.KD.ZG": "GDP growth rate (%)",
    "FP.CPI.TOTL.ZG": "Inflation rate (%)",
    "SL.UEM.TOTL.ZS": "Unemployment rate (%)",
}

    for code, name in indicators.items():
        get_indicator(code, name)

if __name__ == "__main__":
    main()