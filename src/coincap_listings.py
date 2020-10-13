import json
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

#currency set and url for calls to currencies listed 
currency = 'USD'
listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#set headers and API key
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(listings_url)
  data = json.loads(response.text)
  #print(json.dumps(data, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

currency_data = data['data']
#format and print out data for each crpyto
for currency in currency_data:
  rank = currency['id']
  name = currency['name']
  symbol = currency['symbol']
  print(str(rank) +': ' + name + ' {' + symbol + '}')
