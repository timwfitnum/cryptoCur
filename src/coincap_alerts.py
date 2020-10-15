import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
import time


convert = 'USD'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
quotes_url= 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='
conversion = '&convert=' + convert
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
}

session = Session()
session.headers.update(headers)
"""
try:
  response = session.get(quotes_url)
  data = json.loads(response.text)
#  print(json.dumps(data, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

quotes_url_pairs = {}
data = data['data']
for currency in data:
  symbol = currency['symbol']
  url = currency['id']
  quotes_url_pairs[symbol] = url
"""
print()
print("Alerts Tracking...")
print()

already_hit_symbols = []

while True:
  with open("../alerts.txt") as inp:
    for line in inp:
      ticker, amount = line.split()
      ticker = ticker.upper()
      ticker_url = quotes_url + str(ticker)
      try:
        response = session.get(ticker_url)
        data = json.loads(response.text)
        #print(json.dumps(data, sort_keys=True, indent=4))
      except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
      currency = data['data']
      name = currency[str(ticker)]['name']
      last_updated = currency[str(ticker)]['last_updated']
      symbol = currency[str(ticker)]['symbol']
      quotes = currency[str(ticker)]['quote'][str(convert)]
      price = quotes['price']
      
      if float(price) >= float(amount) and symbol not in already_hit_symbols:
        os.system('say ' + name + ' hit ' + amount)
        print(name + " Hit amount "+ amount +" on " + last_updated)
        already_hit_symbols.append(symbol)

  print("...")
  time.sleep(300)