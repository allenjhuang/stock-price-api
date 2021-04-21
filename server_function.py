import json
import requests


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)


    # Request data
    # {
    #     "tickers": ["SPY", "VTSAX"]
    # }
    requested_tickers = None
    request_json = request.get_json()
    # GET
    if request.args and 'tickers' in request.args:
        requested_tickers = request.args.get('tickers')
    # POST
    elif request_json or 'tickers' in request_json:
        requested_tickers = request.json['tickers']

    # Allow just a string to be passed.
    if not isinstance(requested_tickers, list):
        requested_tickers = [requested_tickers]

    
    symbols = ",".join(requested_tickers)
    # Response data
    return_value = []
    while True:
        try:
            ticker_data = requests.get(f'https://query2.finance.yahoo.com/v7/finance/quote?symbols={symbols}&fields=symbol,shortName,longName,regularMarketChangePercent,regularMarketPrice').json()['quoteResponse']['result']
            for ticker_datum in ticker_data:
                try:
                    return_value.append({
                        'ticker': ticker_datum['symbol'],
                        'name': ticker_datum['shortName'] if 'shortName' in ticker_datum else (ticker_datum['longName'] if 'longName' in ticker_datum else ''),
                        'price': ticker_datum['regularMarketPrice'],
                        'percent_change': ticker_datum['regularMarketChangePercent'],
                        # 'percent_change': ticker_data['regularMarketPrice']['raw'] / ticker_data['regularMarketPreviousClose']['raw'] - 1
                        # 'error': False,
                    })
            break
        except TypeError:
            pass
        except KeyError:
            return_value.append({
                'ticker': 'NULL',
                'name': 'NULL',
                'price': 0,
                'percent_change': 0,
                # 'error': True,
            })
            break

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (
        json.dumps(return_value), 200, headers
    )
