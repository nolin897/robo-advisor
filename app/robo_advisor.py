# app/robo_advisor.py

import requests
import json #> Import as dictionary
import datetime

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

latest_close = parsed_response["Time Series (Daily)"]["2020-06-12"]["4. close"]

# breakpoint()

# 
# INFO OUTPUTS
# 

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", now.strftime("%Y-%m-%d %I:%M%p"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")