from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook


class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    truncate_sql = """
        TRUNCATE TABLE {};
    """

    sql = """
        INSERT INTO {}
        {}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 select_sql,
                 table,
                 refresh_table,
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.select_sql = select_sql
        self.table = table
        self.refresh_table = refresh_table

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.refresh_table:
            self.log.info(f'Going to truncate Table {self.table}')
            formatted_truncate_sql = LoadDimensionOperator.truncate_sql.format(
                self.table
            )
            redshift.run(formatted_truncate_sql)

        redshift.run(self.select_sql)

        self.log.info('Operator not yet implemented')
