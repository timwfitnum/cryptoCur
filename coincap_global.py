import json
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# set currency and API url for global metrics
currency = 'USD'
global_metric = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

#set headers and API key
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(global_metric)
  data = json.loads(response.text)
#  print(json.dumps(data, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
#Set variables from query
active_currencies = data['data']['active_cryptocurrencies']
active_markets = data['data']['active_market_pairs']
bitcoin_percentage = data['data']['btc_dominance']
last_updated = data['data']['last_updated']
global_cap = int(data['data']['quote'][currency]['total_market_cap'])
global_volume = int(data['data']['quote'][currency]['total_volume_24h'])

#format data into more readable format
active_currencies_string = '{:,}'.format(active_currencies)
active_markets_string = '{:,}'.format(active_markets)
global_cap_string = '{:,}'.format(global_cap)
global_volume_string = '{:,}'.format(global_volume)
#last_updated_string = datetime.fromtimestamp(last_updated).strftime("%B %d, %Y at %I:%M:%p")

#print out formatted info

#print('There are currently ' + active_currencies_string + ' active cryptocurrencies and ' + active_markets_string + ' active markets.')
#print('The global cap of all cryptos is ' + global_cap_string + ' and the 24hr global volume is ' + global_volume_string + '.')
#print('Bitcoin\'s total percentage of the global cap is ' + str(bitcoin_percentage) + '%.')
#print('\nThis information was last updated on ' + last_updated+ '.')