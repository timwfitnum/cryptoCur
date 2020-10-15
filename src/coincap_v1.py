import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style

convert = 'USD'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
quotes_url= 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='
conversion = '&convert=' + convert
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5ba046a8-ce16-4013-8b5c-7370e96a4e1a',
}

session = Session()
session.headers.update(headers)
"""
try:
  response = session.get(listings_url)
  data = json.loads(response.text)
  #print(json.dumps(data, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

data = data['data']
quotes_url_pairs = {}

for currency in data:
  symbol = currency['symbol']
  url = currency['id']
  quotes_url_pairs[symbol] = url
"""


print("\nMy Portfolio:")

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', convert +' Value', 'Price', '1hr Change', 'Daily Change', 'Weekly Change'])

with open("../portfolio.txt") as inp:
  for line in inp:
    ticker, amount = line.split()
    ticker = ticker.upper()
    ticker_url = quotes_url + str(ticker) +conversion
    try:
      response = session.get(ticker_url)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    data = json.loads(response.text)
    #print(json.dumps(data, sort_keys=True, indent=4))
    currency = data['data'][str(ticker)]
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']
    last_updated = currency['last_updated']

    quotes = currency['quote'][convert]

    price = quotes['price']
    hour_change = quotes["percent_change_1h"]
    day_change = quotes["percent_change_24h"]
    week_change = quotes["percent_change_7d"]

    if hour_change > 0:
      hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
    else:
      hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL
    if day_change > 0:
      day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
    else:
      day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL
    if week_change > 0:
      week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
    else:
      week_change = Back.RED + str(week_change) +'%' + Style.RESET_ALL

    value = float(price) * float(amount)
    portfolio_value += value
    value_string = '{:,}'.format(round(value, 2))

#Asset, Amount Owned,Value, Price, 1hr Change, Daily Change, Weekly Change    

    table.add_row([name + '{' + symbol + '}',
                    str(amount),
                    '$' + value_string,
                    '$' + str(price),
                    str(hour_change),
                    str(day_change),
                    str(week_change)])

print(table)
print()

portfolio_value_string = '{:,}'.format(portfolio_value, 2)
#last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

print("Total Portfolio Value: " + Back.GREEN + portfolio_value_string + convert + Style.RESET_ALL)
#print('\nAPI results last updated on '+ last_updated_string)