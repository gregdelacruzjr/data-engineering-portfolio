import requests
import json

BASE_URL = "https://api.worldbank.org/v2"
COUNTRY_CODE = "PH"

def get_gdp_data():
    url = f"{BASE_URL}/country/{COUNTRY_CODE}/indicator/NY.GDP.MKTP.KD.ZG"
    params = {
        "format": "json",
        "mrv": 10
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data[1]

def calculate_average_gdp(records):
    total = 0
    rec=0
    for record in records:
        if record["value"] is not None:
            total = total + record["value"]
            rec=rec+1
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