from server_function import get_daily_stock_data, get_range_stock_data, get_market_open_time, EST5EDT
from datetime import datetime
import json
from time import perf_counter


def test():
    requested_tickers = ["GME", "TSLA", "GOOG", "VTI", "VTSAX", "ARKK"]
    # requested_tickers = ["GME", ]

    # Daily
    print(f'get_daily_stock_data = {get_daily_stock_data(requested_tickers)}\n')

    # 1 day
    start_time = perf_counter()
    print(f'"1d" = {get_range_stock_data(requested_tickers, "1d")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'1 = {get_range_stock_data(requested_tickers, 1)}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # NOTE: It looks like the requested_range of "1d" will return the most
    # recent closing price if it's afterhours.

    # 5 day
    start_time = perf_counter()
    print(f'"5d" = {get_range_stock_data(requested_tickers, "5d")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'5 = {get_range_stock_data(requested_tickers, 5)}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 1 month
    start_time = perf_counter()
    print(f'"1mo" = {get_range_stock_data(requested_tickers, "1mo")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'30 = {get_range_stock_data(requested_tickers, 30)}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 6 month
    start_time = perf_counter()
    print(f'"6mo" = {get_range_stock_data(requested_tickers, "6mo")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'180 = {get_range_stock_data(requested_tickers, 180)}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # 1 year
    start_time = perf_counter()
    print(f'"1y" = {get_range_stock_data(requested_tickers, "1y")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    start_time = perf_counter()
    print(f'365 = {get_range_stock_data(requested_tickers, 365)}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # year-to-date
    start_time = perf_counter()
    print(f'"ytd" = {get_range_stock_data(requested_tickers, "ytd")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # max
    start_time = perf_counter()
    print(f'"max" = {get_range_stock_data(requested_tickers, "max")}')
    end_time = perf_counter()
    print(f'took {end_time - start_time} seconds\n')

    # print(json.dumps(get_daily_stock_data(requested_tickers)))

    # Thanksgiving market open time (if market was actually open)
    # print(get_market_open_time(days_ago=0, from_day=datetime(
    #     year=2020,
    #     month=11,
    #     day=26,
    #     hour=0,
    #     minute=0,
    #     tzinfo=EST5EDT(),
    # )))
    # print(get_market_open_time(days_ago=147,))

    # Yesterday's market open time
    # print(get_market_open_time(days_ago=1,))


if __name__ == '__main__':
    test()