import main
from datetime import datetime, timedelta
import json
from time import perf_counter


def test():
    requested_tickers = ["GME", "TSLA", "GOOG", "VTI", "VTSAX", "ARKK"]
    # requested_tickers = ["GME", ]

    # Daily
    start_time = perf_counter()
    print(f'main.get_daily_stock_data = {main.get_daily_stock_data(requested_tickers)}\n')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 1 day
    start_time = perf_counter()
    print(f'"1d" = {main.get_time_since_stock_data(requested_tickers, "1d")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'1 = {main.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=main.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=1)).timestamp()))}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # NOTE: It looks like the requested_range of "1d" will return the most
    # recent closing price if it's afterhours.

    # 5 day
    start_time = perf_counter()
    print(f'"5d" = {main.get_time_since_stock_data(requested_tickers, "5d")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'5 = {main.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=main.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=5)).timestamp()))}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 1 month
    start_time = perf_counter()
    print(f'"1mo" = {main.get_time_since_stock_data(requested_tickers, "1mo")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'30 = {main.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=main.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=30)).timestamp()))}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 6 month
    start_time = perf_counter()
    print(f'"6mo" = {main.get_time_since_stock_data(requested_tickers, "6mo")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'180 = {main.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=main.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=180)).timestamp()))}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 1 year
    start_time = perf_counter()
    print(f'"1y" = {main.get_time_since_stock_data(requested_tickers, "1y")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'365 = {main.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=main.EST5EDT()).replace(hour=16, minute=0, second=0, microsecond=0) - timedelta(days=365)).timestamp()))}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # year-to-date
    start_time = perf_counter()
    print(f'"ytd" = {main.get_time_since_stock_data(requested_tickers, "ytd")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'beginning of year = {main.get_time_since_stock_data(requested_tickers, int((datetime.now(tz=main.EST5EDT()).replace(month=1, day=1, hour=16, minute=0, second=0, microsecond=0)).timestamp()))}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # max
    start_time = perf_counter()
    print(f'"max" = {main.get_time_since_stock_data(requested_tickers, "max")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # print(json.dumps(main.get_daily_stock_data(requested_tickers)))

    # Thanksgiving market open time (if market was actually open)
    # print(main.get_market_close_time(days_ago=0, from_day=datetime(
    #     year=2020,
    #     month=11,
    #     day=26,
    #     hour=0,
    #     minute=0,
    #     tzinfo=main.EST5EDT(),
    # )))
    # print(main.get_market_close_time(days_ago=147,))

    # Yesterday's market open time
    # print(main.get_market_close_time(days_ago=1,))
    
if __name__ == '__main__':
    test()
