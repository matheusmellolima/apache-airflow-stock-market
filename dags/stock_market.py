"""DAG definition for stock market data processing."""
from datetime import datetime
import requests

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

from include.stock_market.tasks import _get_stock_prices, _store_stock_prices


SYMBOL = "NVDA"  # Nvidia stock symbol


@dag(
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,  # always triggers the last dag run
    tags=['stock_market'],
)
def stock_market():  # This will be the DAG ID in Airflow
    """DAG definition for stock market data processing."""
    # Tasks will be defined here

    @task.sensor(
        mode='poke',
        poke_interval=30,  # Check every 30 seconds
        timeout=300,  # Stop checking after 5 minutes
    )
    def is_api_available() -> PokeReturnValue:
        # Check if the stock market is open
        api = BaseHook.get_connection('stock_market_api')
        url = f"{api.host}{api.extra_dejson['endpoint']}"
        print(f"API URL: {url}")
        response = requests.get(
            url, headers=api.extra_dejson['headers'], timeout=10)
        data = {}
        try:
            data = response.json()
            data = data["finance"]["result"]
        except requests.JSONDecodeError:
            print("API response is not valid JSON.")
            return False
        except KeyError:
            print("API response does not contain the expected data.")
            return False

        return PokeReturnValue(is_done=data is None)

    get_stock_prices = PythonOperator(
        task_id='get_stock_prices',
        python_callable=_get_stock_prices,
        op_kwargs={
            'url': '{{ task_instance.xcom_pull(task_ids="is_api_available") }}', 'symbol': SYMBOL},
    )

    store_stock_prices = PythonOperator(
        task_id="store_stock_prices",
        python_callable=_store_stock_prices,
        op_kwargs={
            'stock': '{{ task_instance.xcom_pull(task_ids="get_stock_prices") }}'},
    )

    stock_prices_transform = DockerOperator(
        task_id="stock_prices_transform",
        image="airflow/spark-stock-transform-app",
        container_name="stock_prices_transform",
        api_version="auto",
        auto_remove=True,
        docker_url="tcp://docker-proxy:2375",
        network_mode="container:spark-master",
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False,
        environment={
            "SPARK_STOCK_PRICES_FILE_LOCATION": "{{ task_instance.xcom_pull(task_ids='store_stock_prices') }}",
        }
    )

    # Define the task dependencies and execution order
    is_api_available() >> get_stock_prices >> store_stock_prices >> stock_prices_transform


stock_market()  # This will register the DAG in Airflow
