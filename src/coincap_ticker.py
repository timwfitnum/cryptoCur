import json
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# set currency and API url for global metrics
while True:
  limit = input("How many cryptos would you like to return?");
  currency = 'USD'
  quotes_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit='+str(limit)

  #set headers and API key
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(quotes_url)
    data = json.loads(response.text)
  # print(json.dumps(data, sort_keys=True, indent=4))
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

  data = data['data']
  for currency in data:
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']
    
    circ_supply = int(currency['circulating_supply'])
    total_supply = int(currency['total_supply'])

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
    print('Percentage of coins in circulation: ' + str(int(circ_supply/total_supply)) + '%')
    print('\n')


  choice = input('Again? (y/n)')

  if choice == 'n':
    break
