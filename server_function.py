from datetime import datetime, timedelta, tzinfo
import json
import requests
import time

BATCH_SIZE = 500
MAX_RETRIES = 50
SECONDS_IN_A_DAY = 24 * 60 * 60


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # Set CORS headers for the preflight request.
    if request.method == 'OPTIONS':
        # Allows GET and POST requests from any origin with the Content-Type.
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request.
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # Request data
    # {
    #     "tickers": ["SPY", "VTSAX"],  // REQUIRED
    #     "time_since": "1d"  // OPTIONAL, defaults to "1d"
    # }
    requested_tickers = None
    requested_time_since = None
    request_json = request.get_json(silent=True)  # returns None if failed
    # POST
    if request_json:
        if 'tickers' in request_json:
            requested_tickers = request_json['tickers']
        if 'time_since' in request_json:
            requested_time_since = request_json['time_since']
    # GET
    elif request.args:
        if 'tickers' in request.args:
            requested_tickers = request.args.get('tickers')
        if 'time_since' in request.args:
            requested_time_since = request.args.get('time_since')

    # Required parameter
    if requested_tickers is None or len(requested_tickers) == 0:
        # Bad request, no tickers found
        return (json.dumps({'error': 'No tickers in the request.'}), 400, headers)

    if isinstance(requested_time_since, float):
        requested_time_since = int(requested_time_since)

    # Allow just a string to be passed.
    if not isinstance(requested_tickers, list):
        requested_tickers = [requested_tickers]

    market_time = None
    if is_today(requested_time_since):
        stock_data, market_time = get_daily_stock_data(requested_tickers)
    else:
        stock_data, market_time = get_time_since_stock_data(requested_tickers, requested_time_since)
        if len(stock_data) == 0:
            return (json.dumps({'error': 'Invalid time_since in request.'}), 400, headers)

    # Return tuple of (body, status, headers)
    return (json.dumps({'stock_data': stock_data, 'market_time': market_time}), 200, headers)


def get_daily_stock_data(requested_tickers: list) -> tuple:
    market_time = None

    num_batches = ((len(requested_tickers) - 1) // BATCH_SIZE) + 1
    symbol_batches = []
    for batch_index in range(num_batches):
        symbol_batches.append(','.join(requested_tickers[batch_index*BATCH_SIZE:min((batch_index+1)*BATCH_SIZE, len(requested_tickers))]).replace('.', '-'))

    # Response data
    stock_data = []
    for symbols in symbol_batches:
        while True:  # infinite loop to keep trying to get ticker_data
            try:
                ticker_data = requests.get(f'https://query2.finance.yahoo.com/v7/finance/quote?symbols={symbols}&fields=symbol,shortName,longName,regularMarketChangePercent,regularMarketPrice').json()['quoteResponse']['result']
                for ticker_datum in ticker_data:
                    stock_data.append({
                        'ticker': ticker_datum['symbol'] if 'symbol' in ticker_datum else '',
                        'name': ticker_datum['shortName'] if 'shortName' in ticker_datum else (ticker_datum['longName'] if 'longName' in ticker_datum else ''),
                        'price': ticker_datum['regularMarketPrice'] if 'regularMarketPrice' in ticker_datum else 0,
                        'percent_change': ticker_datum['regularMarketChangePercent'] if 'regularMarketChangePercent' in ticker_datum else 0,
                    })
                    market_time = ticker_datum['regularMarketTime'] if 'regularMarketTime' in ticker_datum else None
                break
            except TypeError:
                break
            except KeyError:  # if ticker doesn't exist
                break
    return (stock_data, market_time)


def get_time_since_stock_data(requested_tickers: list, requested_time_since) -> tuple:
    if (
        not isinstance(requested_time_since, int) and
        not (isinstance(requested_time_since, str) and requested_time_since in {
            '1d',
            '5d',
            '1mo',
            '3mo',
            '6mo',
            '1y',
            '2y',
            '5y',
            '10y',
            'ytd',
            'max',
        })
    ):
        return ([], None)  # unexpected type

    # Get info from other endpoint first.
    stock_data, market_time = get_daily_stock_data(requested_tickers)

    for stock_datum in stock_data:
        while True:  # infinite loop to keep trying to get ticker_data
            try:
                if isinstance(requested_time_since, int):
                    historical_price = get_historical_price_from_period(stock_datum, requested_time_since)
                else:
                    historical_price = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_datum["ticker"]}?interval=1d&range={requested_time_since}').json()['chart']['result'][0]['indicators']['quote'][0]['close'][0]

                # print("for " + str(stock_datum["ticker"]) + " at " + str(requested_time_since) + " ago, price was " + str(historical_price))
                # change = stock_datum['price'] - historical_price
                # percentChange = change / old_price
                if historical_price:
                    stock_datum['percent_change'] = ((stock_datum['price'] - historical_price) / historical_price) * 100
                else:
                    stock_datum['percent_change'] = None
                break
            except TypeError:
                stock_datum['percent_change'] = None
                break
            except KeyError:
                stock_datum['percent_change'] = None
                break
    return (stock_data, market_time)


def get_historical_price_from_period(stock_datum: dict, period: int) -> int:
    # First try
    response_data = []
    historical_price = None
    # Retries
    num_mkt_close_retries = 0
    while 'close' not in response_data:
        # No 'close' data, maybe a holiday.
        if num_mkt_close_retries < MAX_RETRIES:
            # Check the day after.
            period += SECONDS_IN_A_DAY
            response_data = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_datum["ticker"]}?interval=1d&period1={period}&period2={period}').json()['chart']['result'][0]['indicators']['quote'][0]
            num_mkt_close_retries += 1
        else:
            # Maxed out retries, give up.
            historical_price = None
            break
    historical_price = response_data['close'][0]
    return historical_price


def is_today(time_since) -> bool:
    """Returns True if the passed time is today, else False."""
    if time_since is None:
        return True
    if time_since == '1d':
        return True
    if not isinstance(time_since, int):
        return False
    return time_since > int((datetime.now(tz=EST5EDT()) - timedelta(days=1)).timestamp())


class EST5EDT(tzinfo):
    """Eastern Time tzinfo object"""
    def utcoffset(self, dt):
        return timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime(dt.year, 3, 8)        #2nd Sunday in March
        self.dston = d + timedelta(days=6-d.weekday())
        d = datetime(dt.year, 11, 1)       #1st Sunday in Nov
        self.dstoff = d + timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'
