from airflow.models import DAG
from airflow.operators import DataQualityOperator
from airflow.operators import LoadFactOperator

import load_statements


def load_facts(parent_dag_name, child_dag_name, start_date, redshift_conn_id):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        start_date=start_date,
    )

    load_fact_bookings = LoadFactOperator(
        task_id='load_bookings',
        dag=dag,
        redshift_conn_id=redshift_conn_id,
        sql=load_statements.LOAD_BOOKING_FACTS,
        table='fact_bookings'
    )

    run_quality_checks_facts = DataQualityOperator(
        task_id='data_quality_checks_facts',
        dag=dag,
        tables='fact_bookings',
        redshift_conn_id=redshift_conn_id,
        sql='SELECT COUNT(*) FROM {}'
    )

    load_fact_bookings >> run_quality_checks_facts

    return dag
