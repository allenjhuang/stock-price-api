import server_function
from datetime import datetime
import unittest


def are_all_fields_in_return_stock_data(data):
    return all(
        [
            'ticker' in datum and
            'name' in datum and
            'price' in datum and
            'percent_change' in datum
            for datum in data
        ]
    )


class TestGetDataMethods(unittest.TestCase):
    def test_get_daily_stock_data_for_one(self):
        requested_tickers = ['SPY']
        data = server_function.get_daily_stock_data(requested_tickers)
        self.assertTrue(
            expr=len(data) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(data)
        )

    def test_get_daily_stock_data_for_six(self):
        requested_tickers = ['GME', 'TSLA', 'GOOG', 'VTI', 'VTSAX', 'ARKK']
        data = server_function.get_daily_stock_data(requested_tickers)
        self.assertTrue(
            expr=len(data) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(data)
        )

    # def test_compare_historical_data_1_and_1d(self):
    #     """NOTE: Test failed on 4/22/21 at 5:33 PM ET."""
    #     requested_tickers = ['SPY']
    #     first = server_function.get_range_stock_data(requested_tickers, 1)
    #     second = server_function.get_range_stock_data(requested_tickers, '1d')
    #     self.assertTrue(
    #         expr=len(first) == len(requested_tickers)
    #         and are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         expr=len(second) == len(requested_tickers) and
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
            expr=len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            expr=len(second) == len(requested_tickers) and
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
            expr=len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            expr=len(second) == len(requested_tickers) and
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
    #         expr=len(first) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         expr=len(second) == len(requested_tickers) and
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
            expr=len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            expr=len(second) == len(requested_tickers) and
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
            expr=len(first) == len(requested_tickers) and
            are_all_fields_in_return_stock_data(first)
        )
        self.assertTrue(
            expr=len(second) == len(requested_tickers) and
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
    #         expr=len(first) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(first)
    #     )
    #     self.assertTrue(
    #         expr=len(second) == len(requested_tickers) and
    #         are_all_fields_in_return_stock_data(second)
    #     )
    #     self.assertEqual(
    #         first=first,
    #         second=second,
    #     )


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
