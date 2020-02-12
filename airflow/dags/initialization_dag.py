from datetime import datetime

import sub_init_stage
import sub_init_dims
import sub_init_facts
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator

from airflow import DAG

dag = DAG('initialization_dag',
          description='Create necessary Tables to run further jobs',
          schedule_interval='0 * * * *',
          catchup=False,
          start_date=datetime(2020, 1, 1, 0, 0, 0, 0)
          )

start_operator = DummyOperator(task_id='initialization_start', dag=dag)
end_operator = DummyOperator(task_id='initialization_end', dag=dag)

init_stage_sub_dag = SubDagOperator(
    subdag=sub_init_stage.init_stage_sub_dag(
        'initialization_dag',
        'init_stage_sub_dag',
        datetime(2020, 1, 1, 0, 0, 0, 0),
        'redshift'
    ),
    task_id='init_stage_sub_dag',
    dag=dag,
)

init_dims_sub_dag = SubDagOperator(
    subdag=sub_init_dims.init_dims_sub_dag(
        'initialization_dag',
        'init_dims_sub_dag',
        datetime(2020, 1, 1, 0, 0, 0, 0),
        'redshift'
    ),
    task_id='init_dims_sub_dag',
    dag=dag,
)

init_facts_sub_dag = SubDagOperator(
    subdag=sub_init_facts.init_facts_sub_dag(
        'initialization_dag',
        'init_facts_sub_dag',
        datetime(2020, 1, 1, 0, 0, 0, 0),
        'redshift'
    ),
    task_id='init_facts_sub_dag',
    dag=dag,
)


start_operator >> init_stage_sub_dag
init_stage_sub_dag >> end_operator
start_operator >> init_dims_sub_dag
init_dims_sub_dag >> end_operator
start_operator >> init_facts_sub_dag
init_facts_sub_dag >> end_operator
