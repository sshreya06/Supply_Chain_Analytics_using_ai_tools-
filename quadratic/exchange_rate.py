# code for creating table "exchange_rate" in quadratic
import requests
import pandas as pd
from datetime import datetime, timedelta

APP_ID = ""   #replace with own app_id from openexchangerates website

start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 5, 17)

data = []

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")

    url = f"https://openexchangerates.org/api/historical/{date_str}.json"
    response = requests.get(
        url,
        params={
            "app_id": APP_ID,   
            "symbols": "INR"
        }
    )

    json_data = response.json()

    # Safety check
    if "rates" not in json_data:
        print(f"API error on {date_str}: {json_data}")
    else:
        rate = json_data["rates"]["INR"]
        data.append({
            "date": date_str,
            "USD_INR_rate": round(rate,4)
        })

    current_date += timedelta(days=1)

df = pd.DataFrame(data)
df
