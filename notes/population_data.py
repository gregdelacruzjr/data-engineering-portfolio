import requests
import json
import pandas as pd

# World Bank API base URL (v2)
# Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/898590
BASE_URL = "https://api.worldbank.org/v2"

# ISO 3166-1 alpha-2 country code for the Philippines
# Reference: https://www.iso.org/iso-3166-country-codes.html
COUNTRY_CODE = "PH"

# World Bank indicator code for total population
# Source: https://data.worldbank.org/indicator/SP.POP.TOTL
INDICATOR_POPULATION = "SP.POP.TOTL"

def get_population_data():
    """Fetch total population data for the Philippines from the World Bank API."""
    try:
        url = f"{BASE_URL}/country/{COUNTRY_CODE}/indicator/{INDICATOR_POPULATION}"
        params = {
            "format": "json",
            "mrv": 10
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # raises error if status code is 4xx or 5xx
        data = response.json()
        return data[1]

    except requests.exceptions.Timeout:
        print("✗ Error: API request timed out. Check your internet connection.")
        return None

    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the World Bank API.")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"✗ Error: API returned an error — {e}")
        return None

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None

def save_raw_json(records):
    """Save raw API response to a JSON file for raw data preservation."""
    with open("notes/population_raw.json", "w") as f:
        json.dump(records, f, indent=2)
    print("✓ Raw data saved to notes/population_raw.json")

def load_and_clean(filepath):
    """Load JSON file into a pandas DataFrame and clean it."""
    df = pd.read_json(filepath)
    df = df[["date", "value"]]
    df.columns = ["Year", "Population"]
    df = df.dropna()
    df["Population"] = df["Population"].astype(int)
    return df

def save_to_csv(df, filepath):
    """Export clean DataFrame to CSV file."""
    df.to_csv(filepath, index=False)
    print(f"✓ Clean data saved to {filepath}")

def calculate_average_population(records):
    """Calculate average population excluding None values."""
    total = 0
    count = 0
    for record in records:
        if record["value"] is not None:
            total = total + record["value"]
            count = count + 1
    average = total / count
    return average

def get_population_growth(records):
    """Calculate population growth between the oldest and newest record."""
    valid = [r for r in records if r["value"] is not None]
    newest = valid[0]["value"]
    oldest = valid[-1]["value"]
    growth = newest - oldest
    return growth

def main():
    print("Philippine Population Analysis")
    print("=" * 40)

    records = get_population_data()

    if records is None:
        print("✗ Could not retrieve data. Exiting.")
        return

    save_raw_json(records)
    df = load_and_clean("notes/population_raw.json")
    print("\nClean DataFrame:")
    print(df.to_string(index=False))

    average = calculate_average_population(records)
    growth = get_population_growth(records)
    print(f"\nAverage Population (last 10 years): {average:,.0f}")
    print(f"Population Growth (newest - oldest): {growth:,.0f}")

if __name__ == "__main__":
    main()