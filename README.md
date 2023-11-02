# Stock Price API
For use on Google Cloud Functions

Request body:
```
{
    "tickers": ["SPY", "AAPL"]
}
```

Response body:
```
[
    {
        'ticker': SPY,
        'price': 411.49,
        'percent_change': 0.0072701504,
    },
    {
        'ticker': AAPL,
        'price': 132.995,
        'percent_change': 0.020213213,
    },
]
```

## deploy with cloud tools command$ gcloud functions deploy python-http-function --gen2 --runtime=python311 --region=us-central1 --source=. --entry-point=main --trigger-http --allow-unauthenticated
