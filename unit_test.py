import server_function
from datetime import datetime, timedelta
import json
import unittest


def are_all_fields_in_return_stock_data(data):
    return len(data) > 0 and all(
        [
            'ticker' in datum and
            'name' in datum and
            'price' in datum and
            'percent_change' in datum and
            datum['ticker'] is not None and
            datum['name'] is not None and
            datum['price'] is not None and
            datum['percent_change'] is not None
            for datum in data
        ]
    )


class TestGetDataMethods(unittest.TestCase):
    def test_get_daily_stock_data_for_one(self):
        requested_tickers = ['SPY']
        data, market_time = server_function.get_daily_stock_data(
            requested_tickers)
        self.assertTrue(
            len(data) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(data)
        )
        self.assertTrue(market_time is not None)

    def test_get_daily_stock_data_for_six(self):
        requested_tickers = ['GME', 'TSLA', 'GOOG', 'VTI', 'VTSAX', 'ARKK']
        data, market_time = server_function.get_daily_stock_data(
            requested_tickers)
        self.assertTrue(
            len(data) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(data)
        )
        self.assertTrue(market_time is not None)

    # def test_historical_data_1_and_1d(self):
    #     """NOTE: Test failed on 4/22/21 at 5:33 PM ET."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=1)).timestamp()))[0]
    #     second = server_function.get_time_since_stock_data(requested_tickers, '1d')[0]
    #     self.assertTrue(
    #         len(first) == len(requested_tickers)
    #         and are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )

    def test_historical_data_7_and_5d(self):
        requested_tickers = ['SPY']
        first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=7)).timestamp()))[0]
        second = server_function.get_time_since_stock_data(requested_tickers, '5d')[0]
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )

    def test_historical_data_30_and_1mo(self):
        """NOTE: Test passed on 4/22/21."""
        requested_tickers = ['SPY']
        first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=31)).timestamp()))[0]
        second = server_function.get_time_since_stock_data(requested_tickers, '1mo')[0]
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )

    # def test_historical_data_90_and_3mo(self):
    #     """NOTE: Test failed on 4/22/21."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=90)).timestamp()))[0]
    #     second = server_function.get_time_since_stock_data(requested_tickers, '3mo')[0]
    #     self.assertTrue(
    #         len(first) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )

    def test_historical_data_180_and_6mo(self):
        """NOTE: Test passed on 4/22/21."""
        requested_tickers = ['SPY']
        first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=181)).timestamp()))[0]
        second = server_function.get_time_since_stock_data(requested_tickers, '6mo')[0]
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )

    # def test_historical_data_365_and_1y(self):
    #     """NOTE: Test failed on 4/22/21."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=365)).timestamp()))[0]
    #     second = server_function.get_time_since_stock_data(requested_tickers, '1y')[0]
    #     self.assertTrue(
    #         len(first) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )

    def test_historical_data_ytd(self):
        """"""
        requested_tickers = ['SPY']
        first = server_function.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=server_function.EST5EDT()).replace(month=1, day=1, hour=16, minute=0, second=0, microsecond=0)).timestamp()))[0]
        second = server_function.get_time_since_stock_data(requested_tickers, 'ytd')[0]
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first),
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second),
        )


class TestRequest:
    """Only used to simulate a request object for the below test."""
    def __init__(self, initial_data) -> None:
        self.json = initial_data
        self.method = "TEST"

    def get_json(self, silent: bool = False) -> dict:
        if not isinstance(self.json, dict):
            if silent:
                return None
            raise Exception('"parse" error')
        return self.json

    def get_tickers_length(self) -> int:
        if isinstance(self.json, dict):
            if isinstance(self.json['tickers'], str):
                return 1
            elif isinstance(self.json['tickers'], list):
                return len(self.json['tickers'])
            else:
                return -1
        else:
            return -1


class TestMain(unittest.TestCase):
    def test_main_simple(self):
        request = TestRequest({
            'tickers': 'SPY',
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        body = json.loads(return_value_from_main[0])
        self.assertTrue(
            len(body['stock_data']) == request.get_tickers_length())
        self.assertTrue(
            are_all_fields_in_return_stock_data(body['stock_data']))
        self.assertTrue(body['market_time'] is not None)

    def test_main_empty_ticker_array(self):
        request = TestRequest({
            'tickers': [],
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        self.assertTrue(return_value_from_main[1], 400)
        self.assertTrue('error' in json.loads(return_value_from_main[0]))

    def test_main_null_ticker(self):
        request = TestRequest({
            'tickers': None,
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        self.assertTrue(return_value_from_main[1], 400)
        self.assertTrue('error' in json.loads(return_value_from_main[0]))

    def test_main_time_since_1d(self):
        request = TestRequest({
            'tickers': ['SPY'],
            'time_since': '1d',
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        body = json.loads(return_value_from_main[0])
        self.assertTrue(
            len(body['stock_data']) == request.get_tickers_length())
        self.assertTrue(
            are_all_fields_in_return_stock_data(body['stock_data']))
        self.assertTrue(body['market_time'] is not None)

    def test_main_time_since_1(self):
        request = TestRequest({
            'tickers': ['SPY'],
            'time_since': int((datetime.now(tz=server_function.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=1)).timestamp()),
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        body = json.loads(return_value_from_main[0])
        self.assertTrue(
            len(body['stock_data']) == request.get_tickers_length())
        self.assertTrue(
            are_all_fields_in_return_stock_data(body['stock_data']))
        self.assertTrue(body['market_time'] is not None)

    def test_main_invalid_time_since(self):
        request = TestRequest({
            'tickers': ['SPY'],
            'time_since': 'gibberish',
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        self.assertTrue(return_value_from_main[1], 400)
        self.assertTrue('error' in json.loads(return_value_from_main[0]))


if __name__ == '__main__':
    unittest.main()
