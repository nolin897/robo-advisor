# app/robo_advisor.py

import csv
import datetime
import json #> Import as dictionary
import os

import requests

def to_usd(my_price):
    return f"${my_price:,.2f}"

# 
# INFO INPUTS
# 

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)
# print(type(response)) #> <class 'requests.models.Response'>
# print(response.status_code) #>200
# print(response.text)

parsed_response = json.loads(response.text) #>Parse response.text into a dictionary

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

now = datetime.datetime.now()

# breakpoint()

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]


# calculate recent high price
high_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))

recent_high = max(high_prices)

# calculate recent low price
low_prices = []

for date in dates:
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_low = min(low_prices)

# Provide recommendation based on a trading rule of a 100 bps difference from the previous close
previous_day = dates[1]
previous_close = tsd[previous_day]["4. close"]
if float(latest_close) > 1.01*float(previous_close):
    rec = "BUY"
    rec_reason = "Price increased more than 100 bps"
elif float(latest_close) < 0.99*float(previous_close):
    rec = "SELL"
    rec_reason = "Price declined more than 100 bps"
else:
    rec = "HOLD"
    rec_reason = "Price within 100 bps of the previous close"

# 
# INFO OUTPUTS
# 

# csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })
    

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", now.strftime("%Y-%m-%d %I:%M%p"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {rec}!")
print(f"RECOMMENDATION REASON: {rec_reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


