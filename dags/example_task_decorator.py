"""Example of a DAG definition using the task decorator."""
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator


def _task_c():
    print('Task C')
    return 42


@dag(
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['example'],
)
def example_task_decorator():
    """DAG definition for task example."""
    @task
    def task_a(value: int):
        print('Task A')
        return value

    @task
    def task_b(value: int):
        print('Task B')
        print(value)

    task_c = PythonOperator(
        task_id='task_c',
        python_callable=_task_c,
    )

    task_b(task_a(task_c.output))


example_task_decorator()
