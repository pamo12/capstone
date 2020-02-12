from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook


class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    truncate_sql = """
        TRUNCATE TABLE {};
    """

    default_sql = """
        INSERT into {}
        DEFAULT VALUES;
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 sql,
                 table,
                 refresh_table,
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
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

            self.log.info(f'Going to insert a Default Entry into {self.table}')
            formatted_default_sql = LoadDimensionOperator.default_sql.format(
                self.table
            )
            redshift.run(formatted_default_sql)

        self.log.info(f'Going to execute {self.sql}')
        redshift.run(self.sql)
