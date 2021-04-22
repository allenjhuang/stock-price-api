from datetime import datetime, timedelta, tzinfo
import json
import requests
import time

BATCH_SIZE = 500
MAX_RETRIES = 50
SECONDS_IN_A_DAY = 86400


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
    #     "range": "1d",  // OPTIONAL str or num (num represents days ago)
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


def get_daily_stock_data(requested_tickers: list) -> list:
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
                break
            except TypeError:
                break
            except KeyError:  # if ticker doesn't exist
                break
    return stock_data


def get_range_stock_data(requested_tickers: list, requested_range) -> list:
    period = None
    if type(requested_range) is int:
        period = get_market_open_time(days_ago=requested_range)
    elif type(requested_range) is str:
        pass
    else:  # unexpected type
        return []

    # Get info from other endpoint first.
    stock_data = get_daily_stock_data(requested_tickers)

    for stock_datum in stock_data:
        while True:  # infinite loop to keep trying to get ticker_data
            try:
                if period:
                    historical_price = get_historical_price_from_period(stock_datum, period)
                else:
                    historical_price = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_datum["ticker"]}?interval=1d&range={requested_range}').json()['chart']['result'][0]['indicators']['quote'][0]['close'][0]

                print("for " + str(stock_datum["ticker"]) + " at " + str(requested_range) + " ago, price was " + str(historical_price))
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
    return stock_data


def get_historical_price_from_period(stock_datum: dict, period: int) -> int:
    # First try
    response_data = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_datum["ticker"]}?interval=1d&period1={period}&period2={period}').json()['chart']['result'][0]['indicators']['quote'][0]
    historical_price = None
    # Retries
    num_mkt_open_retries = 0
    while len(response_data) == 0:
        # No 'close' data, maybe a holiday.
        if num_mkt_open_retries < MAX_RETRIES:
            # Check the day before.
            period -= SECONDS_IN_A_DAY
            response_data = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{stock_datum["ticker"]}?interval=1d&period1={period}&period2={period}').json()['chart']['result'][0]['indicators']['quote'][0]
            num_mkt_open_retries += 1
        else:
            # Maxed out retries, give up.
            historical_price = None
            break
    historical_price = response_data['close'][0]
    return historical_price


def get_market_open_time(days_ago: int = 0, from_day: datetime = None) -> int:
    """Returns the U.S. market open epoch time in whole seconds.

    If days_ago falls on a weekend, the most recent weekday's market open time
    will be returned instead.

    NOTE: Does not account for market holidays.
    """
    # Default from_day to today.
    if from_day is None:
        from_day = datetime.now(tz=EST5EDT())
    market_open_time_days_ago = from_day.replace(
        hour=9, minute=30, second=0, microsecond=0) - timedelta(days=days_ago)
    # Return most recent weekday's market open time.
    # weekday() returns a number from 0 to 6, Monday to Sunday.
    if market_open_time_days_ago.weekday() - 4 > 0:
        market_open_time_days_ago -= timedelta(
            days=market_open_time_days_ago.weekday() - 4)
    return int(market_open_time_days_ago.timestamp())


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
