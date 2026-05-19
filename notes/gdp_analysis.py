import requests

# Base URL for the World Bank API (v2)
# Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/898590
BASE_URL = "https://api.worldbank.org/v2"

# ISO 3166-1 alpha-2 country code for the Philippines
# Reference: https://www.iso.org/iso-3166-country-codes.html
COUNTRY_CODE = "PH"

# World Bank indicator codes with source references
# Source: https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
INDICATOR_GDP_GROWTH = "NY.GDP.MKTP.KD.ZG"  # GDP growth rate (%)


def get_gdp_data():
    """Fetch GDP growth rate data for the Philippines from the World Bank API."""
    url = f"{BASE_URL}/country/{COUNTRY_CODE}/indicator/{INDICATOR_GDP_GROWTH}"
    params = {
        "format": "json",
        "mrv": 10  # most recent 10 values
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data[1]  # index 0 is metadata, index 1 is the actual data


def calculate_average_gdp(records):
    """Calculate average GDP growth rate excluding None values."""
    total = 0
    rec = 0
    for record in records:
        if record["value"] is not None:
            total = total + record["value"]
            rec = rec + 1
    average = total / rec
    return average


def main():
    print("Philippine GDP Growth Analysis")
    print("=" * 40)
    records = get_gdp_data()
    average = calculate_average_gdp(records)
    print(f"Average GDP Growth (last 10 years): {average:.2f}%")
    for record in records:
        if record["value"] is not None:
            print(f"  {record['date']}: {record['value']:.2f}%")


if __name__ == "__main__":
    main()