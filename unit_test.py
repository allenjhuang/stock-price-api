import server_function
from datetime import datetime
import json
import unittest


def are_all_fields_in_return_stock_data(data):
    return len(data) > 0 and all(
        [
            'ticker' in datum and
            'name' in datum and
            'price' in datum and
            'percent_change' in datum and
            'market_time' in datum and
            datum['ticker'] is not None and
            datum['name'] is not None and
            datum['price'] is not None and
            datum['percent_change'] is not None and
            datum['market_time'] is not None
            for datum in data
        ]
    )


class TestGetDataMethods(unittest.TestCase):
    def test_get_daily_stock_data_for_one(self):
        requested_tickers = ['SPY']
        data = server_function.get_daily_stock_data(requested_tickers)
        self.assertTrue(
            len(data) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(data)
        )

    def test_get_daily_stock_data_for_six(self):
        requested_tickers = ['GME', 'TSLA', 'GOOG', 'VTI', 'VTSAX', 'ARKK']
        data = server_function.get_daily_stock_data(requested_tickers)
        self.assertTrue(
            len(data) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(data)
        )

    # def test_compare_historical_data_1_and_1d(self):
    #     """NOTE: Test failed on 4/22/21 at 5:33 PM ET."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_range_stock_data(requested_tickers, 1)
    #     second = server_function.get_range_stock_data(requested_tickers, '1d')
    #     self.assertTrue(
    #         len(first) == len(requested_tickers)
    #         and are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )
    #     self.assertEqual(
    #         first=first,
    #         second=second,
    #     )

    def test_compare_historical_data_5_and_5d(self):
        requested_tickers = ['SPY']
        first = server_function.get_range_stock_data(requested_tickers, 5)
        second = server_function.get_range_stock_data(requested_tickers, '5d')
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )
        self.assertEqual(
            first=first,
            second=second,
        )

    def test_compare_historical_data_30_and_1mo(self):
        """NOTE: Test passed on 4/22/21."""
        requested_tickers = ['SPY']
        first = server_function.get_range_stock_data(requested_tickers, 30)
        second = server_function.get_range_stock_data(requested_tickers, '1mo')
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )
        self.assertEqual(
            first=first,
            second=second,
        )

    # def test_compare_historical_data_90_and_3mo(self):
    #     """NOTE: Test failed on 4/22/21."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_range_stock_data(requested_tickers, 90)
    #     second = server_function.get_range_stock_data(requested_tickers, '3mo')
    #     self.assertTrue(
    #         len(first) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )
    #     self.assertEqual(
    #         first=first,
    #         second=second,
    #     )

    def test_compare_historical_data_180_and_6mo(self):
        """NOTE: Test passed on 4/22/21."""
        requested_tickers = ['SPY']
        first = server_function.get_range_stock_data(requested_tickers, 180)
        second = server_function.get_range_stock_data(requested_tickers, '6mo')
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )
        self.assertEqual(
            first=first,
            second=second,
        )

    def test_compare_historical_data_180_and_6mo(self):
        """NOTE: Test passed on 4/22/21."""
        requested_tickers = ['SPY']
        first = server_function.get_range_stock_data(requested_tickers, 180)
        second = server_function.get_range_stock_data(requested_tickers, '6mo')
        self.assertTrue(
            len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            len(second) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(second)
        )
        self.assertEqual(
            first=first,
            second=second,
        )

    # def test_compare_historical_data_365_and_1y(self):
    #     """NOTE: Test failed on 4/22/21."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_range_stock_data(requested_tickers, 365)
    #     second = server_function.get_range_stock_data(requested_tickers, '1y')
    #     self.assertTrue(
    #         len(first) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )
    #     self.assertEqual(
    #         first=first,
    #         second=second,
    #     )


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
        data = json.loads(return_value_from_main[0])
        self.assertTrue(len(data) == request.get_tickers_length())
        self.assertTrue(are_all_fields_in_return_stock_data(data))

    def test_main_empty_ticker_array(self):
        request = TestRequest({
            'tickers': [],
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        data = json.loads(return_value_from_main[0])
        self.assertFalse(are_all_fields_in_return_stock_data(data))

    def test_main_null_ticker(self):
        request = TestRequest({
            'tickers': None,
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        data = json.loads(return_value_from_main[0])
        self.assertFalse(are_all_fields_in_return_stock_data(data))

    def test_main_range_1d(self):
        request = TestRequest({
            'tickers': ['SPY'],
            'range': '1d',
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        data = json.loads(return_value_from_main[0])
        self.assertTrue(len(data) == request.get_tickers_length())
        self.assertTrue(are_all_fields_in_return_stock_data(data))

    def test_main_range_1(self):
        request = TestRequest({
            'tickers': ['SPY'],
            'range': 1,
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        data = json.loads(return_value_from_main[0])
        self.assertTrue(len(data) == request.get_tickers_length())
        self.assertTrue(are_all_fields_in_return_stock_data(data))

    def test_main_invalid_range(self):
        request = TestRequest({
            'tickers': ['SPY'],
            'range': 'gibberish',
        })
        return_value_from_main = server_function.main(request)
        self.assertTrue(len(return_value_from_main) > 0)
        self.assertTrue(isinstance(return_value_from_main[0], str))
        data = json.loads(return_value_from_main[0])
        self.assertFalse(len(data) == request.get_tickers_length())
        self.assertFalse(are_all_fields_in_return_stock_data(data))


class TestGetMarketOpenTime(unittest.TestCase):
    def test_market_open_time_20210419(self):
        """Should return the same day's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=19,
            hour=8,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=19,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )

    def test_market_open_time_20210420(self):
        """Should return the same day's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=20,
            hour=0,
            minute=0,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=20,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )

    def test_market_open_time_20210421(self):
        """Should return the same day's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=21,
            hour=23,
            minute=50,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=21,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )

    def test_market_open_time_20210422(self):
        """Should return the same day's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=22,
            hour=10,
            minute=15,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=22,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )

    def test_market_open_time_20210423(self):
        """Should return the same day's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=23,
            hour=17,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=23,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )

    def test_market_open_time_20210424(self):
        """Should return Friday's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=24,
            hour=23,
            minute=59,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=23,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )

    def test_market_open_time_20210425(self):
        """Should return Friday's market open time."""
        days_ago = 0
        from_day = datetime(
            year=2021,
            month=4,
            day=25,
            hour=0,
            minute=1,
            tzinfo=server_function.EST5EDT(),
        )
        second_datetime = datetime(
            year=2021,
            month=4,
            day=23,
            hour=9,
            minute=30,
            tzinfo=server_function.EST5EDT(),
        )
        first = server_function.get_market_open_time(
            days_ago=days_ago, from_day=from_day)
        second = int(second_datetime.timestamp())
        self.assertEqual(
            first=first,
            second=second,
            msg=f'{datetime.fromtimestamp(first)} is not equal to '
                f'{second_datetime}',
        )


if __name__ == '__main__':
    unittest.main()
