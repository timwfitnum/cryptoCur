import json
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


quotes_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  #set headers and API key
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY'
}

session = Session()
session.headers.update(headers)

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

#print(quotes_url_pairs)

while True:
  print()
  choice = input("Enter Ticker of cryptocurrency: ")
  choice = choice.upper()

  coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=' + str(quotes_url_pairs[choice])
  response = session.get(coin_url)
  data = json.loads(response.text)
#  print(coin_url)
#  print(json.dumps(data, sort_keys=True, indent=4))

  currency = data['data'][str(quotes_url_pairs[choice])]
  rank = currency['cmc_rank']
  name = currency['name']
  symbol = currency['symbol']
    
  circ_supply = float(currency['circulating_supply'])
  total_supply = float(currency['total_supply'])

  quotes = currency['quote']['USD']
  market_cap = quotes['market_cap']
  hour_change = quotes["percent_change_1h"]
  day_change = quotes["percent_change_24h"]
  week_change = quotes["percent_change_7d"]
  price = quotes['price']
  volume = quotes['volume_24h']

  volume_string = '{:,}'.format(volume)
  market_cap_string = '{:,}'.format(market_cap)
  circ_supply_string = '{:,}'.format(circ_supply)
  total_supply_string = '{:,}'.format(total_supply)

  print(str(rank) + ': ' + name + '(' + symbol + ')')
  print('Market cap: \t\t$' + market_cap_string)
  print('Price: \t\t\t$' + str(price))
  print('24Hr Volume: \t\t$' + volume_string)
  print('Hour change: \t\t' + str(hour_change) + '%')
  print('Day change: \t\t' + str(day_change) + '%')
  print('Week change: \t\t' + str(week_change) + '%')
  print("Total supply: \t\t$" + total_supply_string)
  print('Circulating supply: \t$' + circ_supply_string)
  print('Percentage of coins in circulation: ' + str(float(circ_supply/total_supply)) + '%')
  print('\n')