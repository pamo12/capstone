from airflow.models import DAG
from airflow.operators import DataQualityOperator
from airflow.operators import LoadDimensionOperator

import load_statements


def load_dimensions(parent_dag_name, child_dag_name, start_date, redshift_conn_id):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        start_date=start_date,
    )

    load_vehicle_model_dimension = LoadDimensionOperator(
        task_id='load_vehicle_models',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_VEHICLE_MODELS,
        table='dim_vehicle_models',
        refresh_table=True
    )

    load_company_dimension = LoadDimensionOperator(
        task_id='load_companies',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_COMPANIES,
        table='dim_companies',
        refresh_table=True
    )

    load_category_dimension = LoadDimensionOperator(
        task_id='load_categories',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_CATEGORIES,
        table='dim_categories',
        refresh_table=True
    )

    load_vehicle_dimension = LoadDimensionOperator(
        task_id='load_vehicles',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_VEHICLES,
        table='dim_vehicles',
        refresh_table=True
    )

    load_rental_zone_dimension = LoadDimensionOperator(
        task_id='load_rental_zones',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_RENTAL_ZONES,
        table='dim_rental_zones',
        refresh_table=True
    )

    load_date_dimension = LoadDimensionOperator(
        task_id='load_dates',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_DATES,
        table='dim_date',
        refresh_table=True
    )

    load_weather_dimension = LoadDimensionOperator(
        task_id='load_weather',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_WEATHER,
        table='dim_weather',
        refresh_table=True
    )

    run_quality_checks_base_dims = DataQualityOperator(
        task_id='data_quality_checks_base_dims',
        dag=dag,
        tables='dim_companies,dim_vehicle_models,dim_date,dim_weather',
        redshift_conn_id=redshift_conn_id,
        sql='SELECT COUNT(*) FROM {}'
    )

    run_quality_checks_dep_dims = DataQualityOperator(
        task_id='data_quality_checks_dep_dims',
        dag=dag,
        tables='dim_vehicles,dim_categories,dim_rental_zones',
        redshift_conn_id=redshift_conn_id,
        sql='SELECT COUNT(*) FROM {}'
    )

    load_vehicle_model_dimension >> run_quality_checks_base_dims
    load_company_dimension >> run_quality_checks_base_dims
    load_date_dimension >> run_quality_checks_base_dims
    load_weather_dimension >> run_quality_checks_base_dims

    run_quality_checks_base_dims >> load_category_dimension
    run_quality_checks_base_dims >> load_vehicle_dimension
    run_quality_checks_base_dims >> load_rental_zone_dimension

    load_category_dimension >> run_quality_checks_dep_dims
    load_vehicle_dimension >> run_quality_checks_dep_dims
    load_rental_zone_dimension >> run_quality_checks_dep_dims

    return dag
