import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style

convert = 'USD'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort='
global_metric = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
}

session = Session()
session.headers.update(headers)

convert = str(input("Please select currency for portfolio: "))
conversion = '?convert=' + convert
global_metric = global_metric + conversion

try:
  response = session.get(global_metric)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
    
data = json.loads(response.text)
#print(json.dumps(data, sort_keys=True, indent=4))
data = data['data']

global_cap = int(data['quote'][convert]['total_market_cap'])
global_cap_string = '{:,}'.format(global_cap)

while True:
  print()
  print("CoinmarketCap Explorer Menu")
  print("The global market cap is $" + global_cap_string)
  print()
  print("1 - Top 100 sorted by price")
  print("2 - Top 100 sorted by 24 hour change")
  print("3 - Top 100 sorted by 24 hour volume")
  print("0 - Exit")
  print()
  choice = input("Please choose 1 - 3!")
  
  if choice == '1':
    listings_url += 'price'
  if choice == '2':
    listings_url += 'percent_change_24h'
  if choice == '3':
    listings_url += 'volume_24h'
  if choice == '0':
    break

  try:
    response = session.get(listings_url)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  data = json.loads(response.text)
  data = data['data']

  table = PrettyTable(['CMC Rank','Asset','Price','Market Cap', 'Volume', '1hr Change', 'Daily Change', 'Weekly Change'])

  print()
  for currency in data:
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']
    quotes = currency['quote'][convert]
    market_cap = quotes['market_cap']
    hour_change = quotes['percent_change_1h']
    day_change = quotes['percent_change_24h']
    week_change = quotes['percent_change_7d']
    price = quotes['price']
    volume = quotes['volume_24h']


# could return none type so must check
    if hour_change is not None:
      if hour_change > 0:
        hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
      else:
        hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL
    
    if day_change is not None:
      if day_change > 0:
        day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
      else:
        day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL
    
    if week_change is not None:
      if week_change > 0:
        week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
      else:
        week_change = Back.RED + str(week_change) +'%' + Style.RESET_ALL

    if volume is not None:
      volume_string = '{:,}'.format(volume)

    if market_cap is not None:
      market_cap_string = '{:,}'.format(market_cap)

    table.add_row([rank,
                  name + '{' + symbol + '}',
                  '$' + str(price),
                  '$' + market_cap_string,
                  '$' + volume_string,
                  str(hour_change),
                  str(day_change),
                  str(week_change)])
  print()
  print(table)
  print()

  choice = input("Again? (y/n)")

  if choice == 'n':
    break
      
      
      