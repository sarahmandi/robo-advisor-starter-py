from dotenv import load_dotenv
import json
import os
import requests
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

def to_usd(my_price):
    return "${0:,2f}".format(my_price)

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key) # TODO: remove or comment-out this line after you have verified the environment variable is getting read properly

symbols =[]
while True:
    symbol = input("Please specify a stock symbol: ")# TODO: capture user input, like... input("Please specify a stock symbol: ")
    if symbol.isalpha() and len(symbol) <6 and symbol != "DONE":
        symbols.append(symbol)
    if symbol == "DONE":
        break
    if not symbol.isalpha() or len(symbol) >5:
        print("Please enter a properly formatted stock ticker like 'MSFT'")

# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
# TODO: assemble the request url to get daily data for the given stock symbol...
for s in symbols:
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + s + "&apikey={api_key}"
    # use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...
    response = requests.get(request_url)
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
    print(latest_closing)
    #recent_high = max(parsed_response["Time Series (Daily)"], key=lambda ev: ev["high"])
    #print(recent_high)
    #recent_low = 


last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

# TODO: further revise the example outputs below to reflect real information
#for s in symbols:
#    print("-----------------")
#    print(f"STOCK SYMBOL: {s}")
#    print("RUN AT: " +str(now))
#    print("-----------------")
#    print("LATEST DAY OF AVAILABLE DATA:{last_refresed}")
#    print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_closing))}")
#    print("RECENT AVERAGE HIGH CLOSING PRICE: $101,000.00")
#    print("RECENT AVERAGE LOW CLOSING PRICE: $99,000.00")
#    print("-----------------")
#    print("RECOMMENDATION: Buy!")
#    print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
#    print("------------------------------------------------------------------------------------------------")
