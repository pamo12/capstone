from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

import sql_statements

dag = DAG('initialization_dag',
          description='Create necessary Tables to run further jobs',
          schedule_interval='0 * * * *',
          catchup=False,
          start_date=datetime(2020, 1, 1, 0, 0, 0, 0)
          )

start_operator = DummyOperator(task_id='initialization_start', dag=dag)
end_operator = DummyOperator(task_id='initialization_end', dag=dag)

drop_stage_vehicles_task = PostgresOperator(
    task_id='drop_stage_vehicles',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.DROP_TABLE_STAGE_VEHICLES
)

drop_stage_rental_zones_task = PostgresOperator(
    task_id='drop_stage_rental_zones',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.DROP_TABLE_STAGE_RENTAL_ZONES
)

drop_stage_categories_task = PostgresOperator(
    task_id='drop_stage_categories',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.DROP_TABLE_STAGE_CATEGORIES
)

drop_stage_bookings_task = PostgresOperator(
    task_id='drop_stage_bookings',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.DROP_TABLE_STAGE_BOOKINGS
)

create_stage_categories_task = PostgresOperator(
    task_id='create_stage_categories',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.CREATE_TABLE_STAGE_CATEGORIES
)

create_stage_rental_zones_task = PostgresOperator(
    task_id='create_stage_rental_zones',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.CREATE_TABLE_STAGE_RENTAL_ZONES
)

create_stage_vehicles_task = PostgresOperator(
    task_id='create_stage_vehicles',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.CREATE_TABLE_STAGE_VEHICLES
)

create_stage_bookings_task = PostgresOperator(
    task_id='create_stage_bookings',
    dag=dag,
    postgres_conn_id='redshift',
    sql=sql_statements.CREATE_TABLE_STAGE_BOOKINGS
)

start_operator >> drop_stage_vehicles_task
drop_stage_vehicles_task >> create_stage_vehicles_task
create_stage_vehicles_task >> end_operator

start_operator >> drop_stage_rental_zones_task
drop_stage_rental_zones_task >> create_stage_rental_zones_task
create_stage_rental_zones_task >> end_operator

start_operator >> drop_stage_categories_task
drop_stage_categories_task >> create_stage_categories_task
create_stage_categories_task >> end_operator

start_operator >> drop_stage_bookings_task
drop_stage_bookings_task >> create_stage_bookings_task
create_stage_bookings_task >> end_operator
