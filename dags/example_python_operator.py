"""A simple DAG to generate and check random numbers using PythonOperator."""
import random
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def generate_random_number(**context):
    """Generate a random number between 1 and 100."""
    ti = context['ti']
    number = random.randint(1, 100)
    ti.xcom_push(key='random_number', value=number)
    print(f"Generated random number: {number}")


def check_even_odd(**context):
    """Check if the number is even or odd."""
    ti = context['ti']
    number = ti.xcom_pull(task_ids='generate_number', key='random_number')
    result = "even" if number % 2 == 0 else "odd"
    print(f"The number {number} is {result}.")


with DAG(
    'example_python_operator',
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    description='A simple DAG to generate and check random numbers',
    catchup=False
) as dag:

    generate_task = PythonOperator(
        task_id='generate_number',
        python_callable=generate_random_number,
    )

    check_task = PythonOperator(
        task_id='check_even_odd',
        python_callable=check_even_odd,
    )

    generate_task >> check_task
