from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

import init_statements


def init_stage_sub_dag(parent_dag_name, child_dag_name, start_date, redshift_conn_id):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        start_date=start_date
    )

    drop_stage_vehicles_task = PostgresOperator(
        task_id='drop_stage_vehicles',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_STAGE_VEHICLES
    )

    drop_stage_rental_zones_task = PostgresOperator(
        task_id='drop_stage_rental_zones',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_STAGE_RENTAL_ZONES
    )

    drop_stage_categories_task = PostgresOperator(
        task_id='drop_stage_categories',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_STAGE_CATEGORIES
    )

    drop_stage_bookings_task = PostgresOperator(
        task_id='drop_stage_bookings',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_STAGE_BOOKINGS
    )

    drop_stage_weather_stations_task = PostgresOperator(
        task_id='drop_stage_weather_stations',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_STAGE_WEATHER_STATIONS
    )

    drop_stage_weather_data_task = PostgresOperator(
        task_id='drop_stage_weather_data',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_STAGE_WEATHER_DATA
    )

    create_stage_categories_task = PostgresOperator(
        task_id='create_stage_categories',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_STAGE_CATEGORIES
    )

    create_stage_rental_zones_task = PostgresOperator(
        task_id='create_stage_rental_zones',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_STAGE_RENTAL_ZONES
    )

    create_stage_vehicles_task = PostgresOperator(
        task_id='create_stage_vehicles',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_STAGE_VEHICLES
    )

    create_stage_bookings_task = PostgresOperator(
        task_id='create_stage_bookings',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_STAGE_BOOKINGS
    )

    create_stage_weather_stations_task = PostgresOperator(
        task_id='create_stage_weather_stations',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_STAGE_WEATHER_STATIONS
    )

    create_stage_weather_data_task = PostgresOperator(
        task_id='create_stage_weather_data',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_STAGE_WEATHER_DATA
    )

    drop_stage_vehicles_task >> create_stage_vehicles_task
    drop_stage_rental_zones_task >> create_stage_rental_zones_task
    drop_stage_categories_task >> create_stage_categories_task
    drop_stage_bookings_task >> create_stage_bookings_task
    drop_stage_weather_stations_task >> create_stage_weather_stations_task
    drop_stage_weather_data_task >> create_stage_weather_data_task

    return dag
