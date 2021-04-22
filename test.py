from server_function import get_daily_stock_data, get_range_stock_data
import json


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


test()
