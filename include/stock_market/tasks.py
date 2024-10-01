"""Tasks for the stock market app."""
from io import BytesIO
import json
import requests
from airflow.hooks.base import BaseHook
from minio import Minio


def _get_stock_prices(symbol: str):
    """Get stock prices from the API."""
    api = BaseHook.get_connection('stock_market_api')
    base_url = f"{api.host}{api.extra_dejson['endpoint']}"
    url = f"{base_url}/{symbol}?metrics=high?&interval=1d&range=1y"
    response = requests.get(
        url, headers=api.extra_dejson['headers'], timeout=10)
    result = response.json()["chart"]["result"][0]
    return json.dumps(result)


def _store_stock_prices(stock: dict):
    """Store stock prices in the Minio bucket."""
    minio = BaseHook.get_connection('minio')

    client = Minio(
        endpoint=minio.extra_dejson["endpoint"].split("//")[1],
        access_key=minio.extra_dejson["aws_access_key_id"],
        secret_key=minio.extra_dejson["aws_access_secret_key"],
        secure=False
    )
    bucket_name = "stock-market"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    symbol = stock["meta"]["symbol"]
    data = json.dumps(stock, ensure_ascii=False).encode('utf-8')
    # Store the data in the database
    obj = client.put_object(
        bucket_name=bucket_name,
        object_name=f"{symbol}/prices.json",
        data=BytesIO(data),
        length=len(data)
    )
    return f"{obj.bucket_name}/{symbol}"
