"""
Simple Hello World DAG for Airflow Training

This DAG demonstrates basic Airflow concepts:
- DAG definition
- Task creation using PythonOperator
- Task dependencies
- Scheduling
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def print_hello():
    """Simple function that prints Hello World"""
    print("Hello World from Airflow!")
    return "Hello World!"


def print_date():
    """Function that prints the current date"""
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current date and time: {current_date}")
    return current_date


def print_goodbye():
    """Function that prints Goodbye"""
    print("Goodbye! DAG execution completed.")
    return "Goodbye!"


# Define the DAG
with DAG(
    'example_hello_world',
    default_args=default_args,
    description='A simple Hello World DAG for training',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'training'],
) as dag:

    # Task 1: Print Hello World
    hello_task = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )

    # Task 2: Print current date using Python
    date_task = PythonOperator(
        task_id='print_date',
        python_callable=print_date,
    )

    # Task 3: Echo message using Bash
    bash_task = BashOperator(
        task_id='echo_message',
        bash_command='echo "This is a bash command in Airflow!"',
    )

    # Task 4: Print Goodbye
    goodbye_task = PythonOperator(
        task_id='print_goodbye',
        python_callable=print_goodbye,
    )

    # Define task dependencies
    # hello_task runs first, then date_task and bash_task run in parallel,
    # finally goodbye_task runs after both are complete
    hello_task >> [date_task, bash_task] >> goodbye_task