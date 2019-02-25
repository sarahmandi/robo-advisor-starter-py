from dotenv import load_dotenv
import json
import csv
import os
import requests
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key) # TODO: remove or comment-out this line after you have verified the environment variable is getting read properly

symbols =[]
while True:
    symbol = input("Please specify a stock symbol: ")# TODO: capture user input, like... input("Please specify a stock symbol: ")
    if not symbol.isalpha() or len(symbol) >5:
        print("Please enter a properly formatted stock ticker like 'MSFT'.")
    else: #failing gracefully with help from: https://github.com/hiepnguyen034/robo-stock
        request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey={api_key}"
        response = requests.get(request_url)
        if 'Error' in response.text:
            print("The stock you are looking for cannot be found, please enter another ticker.")
            continue
        else:
            break
# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
#assemble the request url to get daily data for the given stock symbol...
# use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...
#print("RESPONSE STATUS: " + str(response.status_code))
parsed_response = json.loads(response.text)
#print(parsed_response)
#further parse the JSON response...
#traverse the nested response data structure to find the latest closing price and other values of interest...
#the following code on finding latest day was adapted from #opim-243 slack channel
tsd = parsed_response["Time Series (Daily)"] #> 'dict'
day_keys = tsd.keys() #> 'dict_keys' of all the day values
days = list(day_keys) #> 'list' of all the day values
#print(days[0]) # 'str' of the latest day!
latest_day = days[0] #> '2019-02-19'
latest_closing = tsd[latest_day]["4. close"]
#print(latest_closing)

#with help from https://github.com/s2t2/robo-advisor-screencast/blob/master/app/robo_advisor.py
high_prices = []
low_prices = []

for date in days:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


#
# INFO OUTPUTS
#

# write response data to a CSV file
#with help from https://github.com/s2t2/robo-advisor-screencast/blob/master/app/robo_advisor.py

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in days:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })



# further revise the example outputs below to reflect real information
print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: " +str(now))
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_closing))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-----------------")

##algorithm: if the stock is less than 50% between its high and low, buy because there is appreciation potential
###if the stock exceeds 50% threshold between high and low, do not buy -- not much value left
if float(latest_closing) > ((float(recent_high)-float(recent_low))*0.5)+recent_low:
    print("RECOMMENDATION: Do not buy")
    print("RECOMMENDATION REASON: The latest closing price exceeds the 50% threshold between its recent high and low. Currently, it is not a good time to buy " + symbol +".")
if float(latest_closing) < ((float(recent_high)-float(recent_low))*0.5)+recent_low:
    print("RECOMMENDATION: Buy!")
    print("RECOMMENDATION REASON: The latest closing price falls within the 50% threshold between the recent high and low. Thus, it is a good time to buy " + symbol + " - there is likely value remaining for prospective investors.")
print("-----------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-----------------")
print("HAPPY INVESTING!")
print("--------------------------------------------------------------")
