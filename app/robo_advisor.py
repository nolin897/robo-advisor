# app/robo_advisor.py

# Import Modules
import csv
import datetime
import json #> Import as dictionary
import math
import os
import statistics

# Import Packages
from dotenv import load_dotenv
import plotly
import plotly.graph_objs as go
import requests

load_dotenv()

def to_usd(my_price):
    return f"${my_price:,.2f}"

# 
# INFO INPUTS
# 
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

selected_symbols = []

while True:
    symbol = input("Please enter a stock symbol, or DONE if finished: ")
    if symbol == "DONE" or symbol == "done":
        break
    else:
        if symbol.isalpha() == True:
            if len(symbol) < 6:  #I got the idea to use len() on the symbol variable from https://stackoverflow.com/questions/12717435/how-can-i-get-the-total-number-of-characters-in-the-given-string-that-are-digits; I got the maximum correct number of letters in each symbol from https://www.investopedia.com/terms/s/stocksymbol.asp#:~:text=A%20stock%20symbol%20is%20a,have%20four%20or%20five%20characters.     
                selected_symbols.append(symbol)
            else:
                print("Sorry, please enter a correct stock symbol to get your investment recommendation...")        
        else:
            print("Sorry, please enter a correct stock symbol to get your investment recommendation...")    

for symbol in selected_symbols:    
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    
    # ATTEMPT TO VALIDATE URL
    # if response.status_code > int(399) or response.status_code < int(500):
    #     print("Please run the script again with correct stock symbols!")
    #     break
    # else:
    #     continue

    parsed_response = json.loads(response.text) #>Parse response.text into a dictionary

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    now = datetime.datetime.now()

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

    # GENERATE CSV FILES

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{symbol}.csv")

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

    # GENERATE TIME SERIES VIA PLOTLY

    closing_prices = []

    for date in dates:
        closing_price = tsd[date]["4. close"]
        closing_prices.append(float(closing_price))
    
    plotly.offline.plot({
    "data": [go.Scatter(x=dates, y=closing_prices)],
    "layout": go.Layout(title=f"{symbol.upper()} Time Series")
    }, auto_open=True)
    
    # FINANCIAL CALCULATIONS BASED ON PRIOR COURSEWORK

    # ANNUALIZED EXPECTED RETURN, ANNUALIZED VOLATILITY, & SHARPE RATIO
    
    stock_returns = []
    for date in dates:
        if dates.index(date)+1 < len(dates): # I googled how to look at the index of a list and found the following link https://www.programiz.com/python-programming/methods/list/index ; I corroborated this information using the course repo https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/lists.md
            latest_day_dynamic = dates[dates.index(date)]
            latest_close_dynamic = tsd[latest_day_dynamic]["4. close"]
            previous_day_dynamic = dates[dates.index(date)+1]
            previous_close_dynamic = tsd[previous_day_dynamic]["4. close"]
            stock_return = (float(latest_close_dynamic)-float(previous_close_dynamic))/float(previous_close_dynamic)
            stock_returns.append(stock_return)
        else:
            break    

    daily_expected_return = statistics.mean(stock_returns)
    annualized_expected_return = 252*daily_expected_return
    daily_volatility = statistics.stdev(stock_returns)
    annualized_volatility = math.sqrt(252)*daily_volatility

    risk_free_rate = 0.18 #from https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=billrates        
    sharpe_ratio = (annualized_expected_return - risk_free_rate)/annualized_volatility

    print("------------------------------------------------------------------------")
    print("$+$+$+$+$+$+$+$+YOUR$+$+$+INVESTMENT$+$+$+RECOMMENDATION$+$+$+$+$+$+$+$+")
    print("------------------------------------------------------------------------")
    print(f"SELECTED SYMBOL: {symbol.upper()}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: ", now.strftime("%Y-%m-%d %I:%M%p"))
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print(f"EXPECTED RETURN: {annualized_expected_return*100:,.2f}%")
    print(f"VOLATILITY: {annualized_volatility*100:,.2f}%")
    print(f"SHARPE RATIO: {sharpe_ratio:,.2f}")
    print("-------------------------")
    print(f"RECOMMENDATION: {rec}!")
    print(f"RECOMMENDATION REASON: {rec_reason}")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}...")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")


