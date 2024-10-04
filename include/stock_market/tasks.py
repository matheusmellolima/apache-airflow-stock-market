"""Tasks for the stock market app."""
from io import BytesIO
import json
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowNotFoundException
from minio import Minio


BUCKET_NAME = "stock-market"
S3_BUCKET_NAME = f"s3://{BUCKET_NAME}"


def _get_minio_client() -> Minio:
    minio = BaseHook.get_connection('minio')
    client = Minio(
        endpoint=minio.extra_dejson["endpoint"].split("//")[1],
        access_key=minio.login,
        secret_key=minio.password,
        secure=False
    )
    return client


def _get_stock_prices(symbol: str) -> str:
    """Get stock prices from the API."""
    api = BaseHook.get_connection('stock_market_api')
    base_url = f"{api.host}{api.extra_dejson['endpoint']}"
    url = f"{base_url}/{symbol}?metrics=high?&interval=1d&range=1y"
    response = requests.get(
        url, headers=api.extra_dejson['headers'], timeout=10)
    result = response.json()["chart"]["result"][0]
    return json.dumps(result)


def _store_stock_prices(stock: str) -> str:
    """Store stock prices in the Minio bucket."""
    minio = _get_minio_client()
    if not minio.bucket_exists(BUCKET_NAME):
        minio.make_bucket(BUCKET_NAME)

    stock = json.loads(stock)
    symbol = stock["meta"]["symbol"]
    data = json.dumps(stock, ensure_ascii=False).encode('utf-8')
    # Store the data in the database
    obj = minio.put_object(
        bucket_name=BUCKET_NAME,
        object_name=f"{symbol}/prices.json",
        data=BytesIO(data),
        length=len(data)
    )
    return f"{obj.bucket_name}/{symbol}"


def _get_transformed_stock_market_data(csv_file_location: str = "stock-market/NVDA"):
    minio = _get_minio_client()
    prefix = f"{csv_file_location.split("/")[1]}/transform/"
    objects = minio.list_objects(BUCKET_NAME, prefix=prefix, recursive=True)
    for obj in objects:
        if obj.object_name.endswith(".csv"):
            return obj.object_name

    raise AirflowNotFoundException(
        f"No transformed data found for {csv_file_location}")
