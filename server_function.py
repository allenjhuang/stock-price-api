import json
import yfinance as yf


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
    yf_ticker = yf.Ticker(requested_ticker)
    percent_change = (yf_ticker.info['regularMarketPrice'] / yf_ticker.info['previousClose'] - 1) * 100
    return_value = json.dumps({
        'message': percent_change,
    })

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (
        return_value, 200, headers
    )
