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

    # Response data
    return_value = []
    for requested_ticker in requested_tickers:
        ticker_data = requests.get(f'https://query2.finance.yahoo.com/v11/finance/quoteSummary/{requested_ticker}?modules=price').json()['quoteSummary']['result'][0]['price']
        return_value.append({
            'ticker': requested_ticker,
            'price': ticker_data['regularMarketPrice']['raw'],
            'percent_change': ticker_data['regularMarketChangePercent']['raw'],
        })

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (
        json.dumps(return_value), 200, headers
    )
