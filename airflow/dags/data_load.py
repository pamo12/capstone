from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator

import sub_load_dimensions
import sub_load_stage
import sub_load_facts


dag = DAG('data_load',
          description='Populate Car Sharing data',
          schedule_interval='0 * * * *',
          catchup=False,
          start_date=datetime(2020, 1, 1, 0, 0, 0, 0)
          )

start_operator = DummyOperator(task_id='data_load_start', dag=dag)
end_operator = DummyOperator(task_id='data_load_end', dag=dag)

load_stage_sub_dag = SubDagOperator(
    subdag=sub_load_stage.load_stage(
        'data_load',
        'load_stage_sub_dag',
        datetime(2020, 1, 1, 0, 0, 0, 0),
        'redshift',
        'aws_credentials',
        'pm-udacity-capstone'
    ),
    task_id='load_stage_sub_dag',
    dag=dag,
)

load_dimensions_sub_dag = SubDagOperator(
    subdag=sub_load_dimensions.load_dimensions(
        'data_load',
        'load_dimensions_sub_dag',
        datetime(2020, 1, 1, 0, 0, 0, 0),
        'redshift'
    ),
    task_id='load_dimensions_sub_dag',
    dag=dag,
)

load_facts_sub_dag = SubDagOperator(
    subdag=sub_load_facts.load_facts(
        'data_load',
        'load_facts_sub_dag',
        datetime(2020, 1, 1, 0, 0, 0, 0),
        'redshift'
    ),
    task_id='load_facts_sub_dag',
    dag=dag,
)

start_operator >> load_stage_sub_dag
load_stage_sub_dag >> load_dimensions_sub_dag
load_dimensions_sub_dag >> load_facts_sub_dag
load_facts_sub_dag >> end_operator
