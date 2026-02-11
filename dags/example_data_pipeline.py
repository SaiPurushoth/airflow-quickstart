"""
Example Data Pipeline DAG for Airflow Training

This DAG demonstrates a simple ETL (Extract, Transform, Load) pipeline:
- Extract: Simulate data extraction
- Transform: Process the data
- Load: Simulate loading data to a destination
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import json


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def extract_data(**context):
    """Simulate extracting data from a source"""
    # Simulated data extraction
    data = {
        'users': [
            {'id': 1, 'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'id': 2, 'name': 'Bob', 'age': 25, 'city': 'San Francisco'},
            {'id': 3, 'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
            {'id': 4, 'name': 'Diana', 'age': 28, 'city': 'Boston'},
        ]
    }
    
    print(f"Extracted {len(data['users'])} user records")
    
    # Push data to XCom for next task
    context['task_instance'].xcom_push(key='raw_data', value=data)
    return "Data extraction completed"


def transform_data(**context):
    """Transform the extracted data"""
    # Pull data from previous task
    task_instance = context['task_instance']
    raw_data = task_instance.xcom_pull(task_ids='extract', key='raw_data')
    
    # Transform: Add a new field and filter users
    transformed_users = []
    for user in raw_data['users']:
        # Add age category
        if user['age'] < 30:
            age_category = 'Young'
        elif user['age'] < 35:
            age_category = 'Middle'
        else:
            age_category = 'Senior'
        
        transformed_user = {
            **user,
            'age_category': age_category,
            'processed_at': datetime.now().isoformat()
        }
        transformed_users.append(transformed_user)
    
    print(f"Transformed {len(transformed_users)} user records")
    
    # Push transformed data to XCom
    task_instance.xcom_push(key='transformed_data', value={'users': transformed_users})
    return "Data transformation completed"


def load_data(**context):
    """Simulate loading data to a destination"""
    # Pull transformed data
    task_instance = context['task_instance']
    transformed_data = task_instance.xcom_pull(task_ids='transform', key='transformed_data')
    
    # Simulate loading to database/data warehouse
    print("Loading data to destination...")
    for user in transformed_data['users']:
        print(f"Loading user: {user['name']} (Age Category: {user['age_category']})")
    
    print(f"Successfully loaded {len(transformed_data['users'])} records")
    return "Data loading completed"


def validate_pipeline(**context):
    """Validate the pipeline execution"""
    task_instance = context['task_instance']
    
    # Get data from extract and load tasks
    raw_data = task_instance.xcom_pull(task_ids='extract', key='raw_data')
    transformed_data = task_instance.xcom_pull(task_ids='transform', key='transformed_data')
    
    raw_count = len(raw_data['users'])
    transformed_count = len(transformed_data['users'])
    
    print(f"Validation: Extracted {raw_count} records, Loaded {transformed_count} records")
    
    if raw_count == transformed_count:
        print("✓ Pipeline validation successful!")
        return "Validation passed"
    else:
        raise ValueError("Data count mismatch!")


# Define the DAG
with DAG(
    'example_data_pipeline',
    default_args=default_args,
    description='A simple ETL pipeline DAG for training',
    schedule_interval='@daily',
    catchup=False,
    tags=['example', 'training', 'etl'],
) as dag:

    # Extract task
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        provide_context=True,
    )

    # Transform task
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True,
    )

    # Load task
    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
        provide_context=True,
    )

    # Validation task
    validate_task = PythonOperator(
        task_id='validate',
        python_callable=validate_pipeline,
        provide_context=True,
    )

    # Define pipeline: Extract -> Transform -> Load -> Validate
    extract_task >> transform_task >> load_task >> validate_task