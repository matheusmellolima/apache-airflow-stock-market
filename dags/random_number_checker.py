"""DAG definition for checking if a number is even or odd."""
import random

from datetime import datetime
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['example'],
    description="A simple DAG to generate and check random numbers."
)
def random_number_checker():
    """DAG definition for checking if a number is even or odd."""

    @task
    def generate_random_number():
        return random.randint(1, 100)

    @task
    def check_even_odd(number: int):
        result = "even" if number % 2 == 0 else "odd"
        print(f"The number {number} is {result}.")

    check_even_odd(generate_random_number())


random_number_checker()
