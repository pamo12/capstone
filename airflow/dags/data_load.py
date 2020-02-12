from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import StageS3ToRedshiftOperator
from airflow.operators import DataQualityOperator
from airflow.operators import LoadDimensionOperator
from airflow.operators import LoadFactOperator
from airflow.operators.subdag_operator import SubDagOperator

import load_statements
import sub_load_dimensions
import sub_load_stage
import sub_load_facts


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

stage_rental_zones_to_redshift = StageS3ToRedshiftOperator(
    task_id='stage_rental_zones',
    dag=dag,
    target_table='stage_rental_zones',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='pm-udacity-capstone',
    s3_key='flinkster/OPENDATA_RENTAL_ZONE_CARSHARING.csv',
    json_path='auto'
)

stage_categories_to_redshift = StageS3ToRedshiftOperator(
    task_id='stage_categories',
    dag=dag,
    target_table='stage_categories',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='pm-udacity-capstone',
    s3_key='flinkster/OPENDATA_CATEGORY_CARSHARING.csv',
    json_path='auto'
)

stage_bookings_to_redshift = StageS3ToRedshiftOperator(
    task_id='stage_bookings',
    dag=dag,
    target_table='stage_bookings',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket='pm-udacity-capstone',
    s3_key='flinkster/OPENDATA_BOOKING_CARSHARING.csv',
    json_path='auto'
)

run_quality_checks_stage = DataQualityOperator(
    task_id='data_quality_checks',
    dag=dag,
    tables='stage_vehicles,stage_rental_zones,stage_bookings,stage_categories',
    redshift_conn_id='redshift',
    sql='SELECT COUNT(*) FROM {}'
)

load_vehicle_model_dimension = LoadDimensionOperator(
    task_id='load_vehicle_models',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_VEHICLE_MODELS,
    table='dim_vehicle_models',
    refresh_table=True
)

load_company_dimension = LoadDimensionOperator(
    task_id='load_companies',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_COMPANIES,
    table='dim_companies',
    refresh_table=True
)

load_category_dimension = LoadDimensionOperator(
    task_id='load_categories',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_CATEGORIES,
    table='dim_categories',
    refresh_table=True
)

load_vehicle_dimension = LoadDimensionOperator(
    task_id='load_vehicles',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_VEHICLES,
    table='dim_vehicles',
    refresh_table=True
)

load_rental_zone_dimension = LoadDimensionOperator(
    task_id='load_rental_zones',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_RENTAL_ZONES,
    table='dim_rental_zones',
    refresh_table=True
)

load_date_dimension = LoadDimensionOperator(
    task_id='load_dates',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_DATES,
    table='dim_date',
    refresh_table=True
)

load_fact_bookings = LoadFactOperator(
    task_id='load_bookings',
    dag=dag,
    redshift_conn_id='redshift',
    sql=load_statements.LOAD_BOOKING_FACTS,
    table='fact_bookings'
)

run_quality_checks_base_dims = DataQualityOperator(
    task_id='data_quality_checks_base_dims',
    dag=dag,
    tables='dim_companies,dim_vehicle_models,dim_date',
    redshift_conn_id='redshift',
    sql='SELECT COUNT(*) FROM {}'
)

run_quality_checks_dep_dims = DataQualityOperator(
    task_id='data_quality_checks_dep_dims',
    dag=dag,
    tables='dim_vehicles,dim_categories,dim_rental_zones',
    redshift_conn_id='redshift',
    sql='SELECT COUNT(*) FROM {}'
)

run_quality_checks_facts = DataQualityOperator(
    task_id='data_quality_checks_facts',
    dag=dag,
    tables='fact_bookings',
    redshift_conn_id='redshift',
    sql='SELECT COUNT(*) FROM {}'
)


start_operator >> stage_vehicles_to_redshift
stage_vehicles_to_redshift >> run_quality_checks_stage

start_operator >> stage_rental_zones_to_redshift
stage_rental_zones_to_redshift >> run_quality_checks_stage

start_operator >> stage_categories_to_redshift
stage_categories_to_redshift >> run_quality_checks_stage

start_operator >> stage_bookings_to_redshift
stage_bookings_to_redshift >> run_quality_checks_stage

run_quality_checks_stage >> load_vehicle_model_dimension
run_quality_checks_stage >> load_company_dimension
run_quality_checks_stage >> load_date_dimension

load_vehicle_model_dimension >> run_quality_checks_base_dims
load_company_dimension >> run_quality_checks_base_dims
load_date_dimension >> run_quality_checks_base_dims

run_quality_checks_base_dims >> load_category_dimension
run_quality_checks_base_dims >> load_vehicle_dimension
run_quality_checks_base_dims >> load_rental_zone_dimension

load_category_dimension >> run_quality_checks_dep_dims
load_vehicle_dimension >> run_quality_checks_dep_dims
load_rental_zone_dimension >> run_quality_checks_dep_dims

run_quality_checks_dep_dims >> load_fact_bookings
load_fact_bookings >> run_quality_checks_facts
run_quality_checks_facts >> end_operator
