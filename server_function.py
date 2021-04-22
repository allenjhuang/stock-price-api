import json
import requests

BATCH_SIZE = 500


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
            'Access-Control-Allow-Methods': 'GET',  # add POST
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # Request data
    # {
    #     "tickers": ["SPY", "VTSAX"],  // REQUIRED
    #     "range": "1d",  // OPTIONAL
    # }
    requested_tickers = None
    requested_range = None
    request_json = request.get_json()
    # GET
    if request.args:
        if 'tickers' in request.args:
            requested_tickers = request.args.get('tickers')
        if 'range' in request.args:
            requested_range = request.args.get('range')
    # POST
    elif request_json:
        if 'tickers' in request_json:
            requested_tickers = request.json['tickers']
        if 'range' in request_json:
            requested_range = request.json['range']

    # Required parameter
    if requested_tickers is None:
        # Bad request, no tickers found
        return (json.dumps(
            {'error': 'No tickers were in the request.'}), 400, headers)

    # Allow just a string to be passed.
    if not isinstance(requested_tickers, list):
        requested_tickers = [requested_tickers]

    if requested_range is None:
        stock_data = get_daily_stock_data(requested_tickers)
    else:
        stock_data = get_range_stock_data(requested_tickers, requested_range)

    # Return tuple of (body, status, headers)
    return (json.dumps(stock_data), 200, headers)


def get_daily_stock_data(requested_tickers):
    num_batches = ((len(requested_tickers) - 1) // BATCH_SIZE) + 1
    symbol_batches = []
    for batch_index in range(num_batches):
        symbol_batches.append(','.join(requested_tickers[batch_index*BATCH_SIZE:min((batch_index+1)*BATCH_SIZE, len(requested_tickers))]).replace('.', '-'))

    # Response data
    stock_data = []
    for symbols in symbol_batches:
        while True: # infinite loop to keep trying to get ticker_data
            try:
                ticker_data = requests.get(f'https://query2.finance.yahoo.com/v7/finance/quote?symbols={symbols}&fields=symbol,shortName,longName,regularMarketChangePercent,regularMarketPrice').json()['quoteResponse']['result']
                for ticker_datum in ticker_data:
                    #print(f'done with ticker {ticker_datum["symbol"]}')
                    stock_data.append({
                        'ticker': ticker_datum['symbol'] if 'symbol' in ticker_datum else '',
                        'name': ticker_datum['shortName'] if 'shortName' in ticker_datum else (ticker_datum['longName'] if 'longName' in ticker_datum else ''),
                        'price': ticker_datum['regularMarketPrice'] if 'regularMarketPrice' in ticker_datum else 0,
                        'percent_change': ticker_datum['regularMarketChangePercent'] if 'regularMarketChangePercent' in ticker_datum else 0,
                    })
                break
            except TypeError:
                break
            except KeyError: # if ticker doesn't exist
                break
    return stock_data


def get_range_stock_data(requested_tickers, requested_range):
    stock_data = get_daily_stock_data(requested_tickers);
    for stock_datum in stock_data:
        while True: # infinite loop to keep trying to get ticker_data
            try:
                historical_price = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_datum["ticker"]}?interval=1d&range={requested_range}').json()['chart']['result'][0]['indicators']['quote'][0]['close'][0]
                # change = stock_datum['price'] - historical_price
                # percentChange = change / old_price
                print("for " + str(stock_datum["ticker"]) + " at " + str(requested_range) + " ago, price was " + str(historical_price))
                stock_datum['percent_change'] = ((stock_datum['price'] - historical_price) / historical_price) * 100
                break
            except TypeError:
                stock_datum['percent_change'] = None
                break
            except KeyError:
                stock_datum['percent_change'] = None
                break
    return stock_data


def test():
    requested_tickers = ["GME", "TSLA", "GOOG", "VTI", "VTSAX", "ARKK"]
    print("get_daily_stock_data = " + str(get_daily_stock_data(requested_tickers)))
    print("1d  = " + str(get_range_stock_data(requested_tickers, "1d")))
    print("5d  = " + str(get_range_stock_data(requested_tickers, "5d")))
    print("1mo = " + str(get_range_stock_data(requested_tickers, "1mo")))
    print("6mo = " + str(get_range_stock_data(requested_tickers, "6mo")))
    print("ytd = " + str(get_range_stock_data(requested_tickers, "ytd")))
    print("1y  = " + str(get_range_stock_data(requested_tickers, "1y")))
    print("max = " + str(get_range_stock_data(requested_tickers, "max")))
    print(json.dumps(get_daily_stock_data(requested_tickers)))

#test()
