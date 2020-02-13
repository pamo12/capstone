from airflow.models import DAG
from airflow.operators import StageS3ToRedshiftOperator
from airflow.operators import DataQualityOperator


def load_stage(parent_dag_name, child_dag_name, start_date, redshift_conn_id, aws_creds, s3_bucket):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        start_date=start_date,
    )

    stage_vehicles_to_redshift = StageS3ToRedshiftOperator(
        task_id='stage_vehicles',
        dag=dag,
        target_table='stage_vehicles',
        redshift_conn_id=redshift_conn_id,
        aws_credentials_id=aws_creds,
        s3_bucket=s3_bucket,
        s3_key='flinkster/OPENDATA_VEHICLE_CARSHARING.csv',
        json_path='auto'
    )

    stage_rental_zones_to_redshift = StageS3ToRedshiftOperator(
        task_id='stage_rental_zones',
        dag=dag,
        target_table='stage_rental_zones',
        redshift_conn_id=redshift_conn_id,
        aws_credentials_id=aws_creds,
        s3_bucket=s3_bucket,
        s3_key='flinkster/OPENDATA_RENTAL_ZONE_CARSHARING.csv',
        json_path='auto'
    )

    stage_categories_to_redshift = StageS3ToRedshiftOperator(
        task_id='stage_categories',
        dag=dag,
        target_table='stage_categories',
        redshift_conn_id=redshift_conn_id,
        aws_credentials_id=aws_creds,
        s3_bucket=s3_bucket,
        s3_key='flinkster/OPENDATA_CATEGORY_CARSHARING.csv',
        json_path='auto'
    )

    stage_bookings_to_redshift = StageS3ToRedshiftOperator(
        task_id='stage_bookings',
        dag=dag,
        target_table='stage_bookings',
        redshift_conn_id=redshift_conn_id,
        aws_credentials_id=aws_creds,
        s3_bucket=s3_bucket,
        s3_key='flinkster/OPENDATA_BOOKING_CARSHARING.csv',
        json_path='auto'
    )

    run_quality_checks_stage = DataQualityOperator(
        task_id='data_quality_checks',
        dag=dag,
        tables='stage_vehicles,stage_rental_zones,stage_bookings,stage_categories',
        redshift_conn_id=redshift_conn_id,
        sql='SELECT COUNT(*) FROM {}'
    )

    stage_vehicles_to_redshift >> run_quality_checks_stage
    stage_rental_zones_to_redshift >> run_quality_checks_stage
    stage_categories_to_redshift >> run_quality_checks_stage
    stage_bookings_to_redshift >> run_quality_checks_stage

    return dag
