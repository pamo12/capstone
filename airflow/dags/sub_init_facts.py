from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

import init_statements


def init_facts_sub_dag(parent_dag_name, child_dag_name, start_date, redshift_conn_id):
    dag = DAG(
        '%s.%s' % (parent_dag_name, child_dag_name),
        start_date=start_date
    )

    drop_fact_bookings_task = PostgresOperator(
        task_id='drop_fact_bookings',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.DROP_TABLE_FACT_BOOKINGS
    )

    create_fact_bookings_task = PostgresOperator(
        task_id='create_fact_bookings',
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=init_statements.CREATE_TABLE_FACT_BOOKINGS
    )

    drop_fact_bookings_task >> create_fact_bookings_task

    return dag
