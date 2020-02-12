from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

import init_statements


def init_dims_sub_dag(parent_dag_name, child_dag_name, start_date, redshift_conn_id):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        start_date=start_date
    )

    drop_dim_vehicles_task = PostgresOperator(
        task_id='drop_dim_vehicles',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_DIM_VEHICLES
    )

    drop_dim_vehicle_models_task = PostgresOperator(
        task_id='drop_dim_vehicle_models',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_DIM_VEHICLE_MODELS
    )

    drop_dim_rental_zones_task = PostgresOperator(
        task_id='drop_dim_rental_zones',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_DIM_RENTAL_ZONES
    )

    drop_dim_companies_task = PostgresOperator(
        task_id='drop_dim_companies',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_DIM_COMPANIES
    )

    drop_dim_categories_task = PostgresOperator(
        task_id='drop_dim_categroies',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_DIM_CATEGORIES
    )

    drop_dim_date_task = PostgresOperator(
        task_id='drop_dim_date',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_DIM_DATE
    )

    create_dim_vehicles_task = PostgresOperator(
        task_id='create_dim_vehicles',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_DIM_VEHICLES
    )

    create_dim_vehicle_models_task = PostgresOperator(
        task_id='create_dim_vehicle_models',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_DIM_VEHICLE_MODELS
    )

    create_dim_rental_zones_task = PostgresOperator(
        task_id='create_dim_rental_zones',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_DIM_RENTAL_ZONES
    )

    create_dim_companies_task = PostgresOperator(
        task_id='create_dim_companies',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_DIM_COMPANIES
    )

    create_dim_categories_task = PostgresOperator(
        task_id='create_dim_categories',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_DIM_CATEGORIES
    )

    create_dim_date_task = PostgresOperator(
        task_id='create_dim_date',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_DIM_DATE
    )

    drop_dim_vehicles_task >> create_dim_vehicles_task
    drop_dim_vehicle_models_task >> create_dim_vehicle_models_task
    drop_dim_rental_zones_task >> create_dim_rental_zones_task
    drop_dim_companies_task >> create_dim_companies_task
    drop_dim_categories_task >> create_dim_categories_task
    drop_dim_date_task >> create_dim_date_task

    return dag
