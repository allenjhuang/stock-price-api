import json
import requests
# import yfinance as yf


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
    #     "ticker": "SPY"
    # }
    requested_ticker = None
    request_json = request.get_json()
    # GET
    if request.args and 'ticker' in request.args:
        requested_ticker = request.args.get('ticker')
    # POST
    elif request_json or 'ticker' in request_json:
        requested_ticker = request.json['ticker']

    # Response data
    # ticker_data = yf.Ticker(requested_ticker)
    # price = ticker_data.info['regularMarketPrice']
    # percent_change = (price / ticker_data.info['previousClose'] - 1) * 100
    ticker_data = requests.get(f'https://query2.finance.yahoo.com/v11/finance/quoteSummary/{requested_ticker}?modules=price').json()['quoteSummary']['result'][0]['price']
    return_value = json.dumps({
        'price': ticker_data['regularMarketPrice']['raw'],
        'percent_change': ticker_data['regularMarketChangePercent']['raw'],
    })

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (
        return_value, 200, headers
    )
