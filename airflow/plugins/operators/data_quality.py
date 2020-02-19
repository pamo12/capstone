from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):
    
    ui_color = '#89DA59'

    information_sql = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{}'
            AND is_nullable = 'NO'
        """

    null_sql = """
            SELECT COUNT(*)
            FROM {}
            WHERE {} is null
    """

    @apply_defaults
    def __init__(self,
                 tables,
                 redshift_conn_id,
                 sql,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        self.sql = sql

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)
        
        tables = [x.strip() for x in self.tables.split(',')]
        checks_passed = True
        affected_tables = []
        
        # checks quality for each given table 
        for table in tables:
            formatted_sql = self.sql.format(table)
            self.log.info(f'Data quality check executed will be executed for Table {table}')
            self.log.info(f'SQL to be executed: {formatted_sql}')
            records = redshift.get_records(formatted_sql)
            num_records = records[0][0]

            if len(records) < 1 or num_records < 1:
                checks_passed = False
                affected_tables.append(table)

        if not checks_passed:
            raise ValueError(f'Data quality check failed for Tables {affected_tables}')

        null_checks_passed = True
        null_affected_tables = []
        # null checks for each given table
        for table in tables:
            formatted_information_sql = DataQualityOperator.information_sql.format(table)
            self.log.info(f'SQL to be executed: {formatted_information_sql}')
            records = redshift.get_records(formatted_information_sql)
            self.log.info(f'records {records}, len: {len(records)}')

            x = len(records)
            if x > 0:
                for i in range(x):
                    formatted_null_sql = DataQualityOperator.null_sql.format(table, records[0][0])
                    self.log.info(f'SQL to be executed: {formatted_null_sql}')
                    null_records = redshift.get_records(formatted_null_sql)
                    num_null_records = null_records[0][0]

                    if num_null_records > 0:
                        null_checks_passed = False
                        null_affected_tables.append(table)

        if not null_checks_passed:
            raise ValueError(f'Data quality NULL check failed for Tables {null_affected_tables}')

        self.log.info(f'Data quality checks have been successful for {self.tables}')
