from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import StageS3ToRedshiftOperator


dag = DAG('data_load',
          description='Populate Immigration data to Redshift',
          schedule_interval='0 * * * *',
          catchup=False,
          start_date=datetime(2020, 1, 1, 0, 0, 0, 0)
          )

start_operator = DummyOperator(task_id='data_load_start', dag=dag)
end_operator = DummyOperator(task_id='data_load_end', dag=dag)

stage_vehicles_to_redshift = StageS3ToRedshiftOperator(
    task_id='stage_vehicles',
    dag=dag,
    target_table='stage_vehicles',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='pm-udacity-capstone',
    s3_key='flinkster/OPENDATA_VEHICLE_CARSHARING.csv',
    json_path='auto'
)

start_operator >> stage_vehicles_to_redshift
stage_vehicles_to_redshift >> end_operator
