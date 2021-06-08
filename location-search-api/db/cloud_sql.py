from typing import List
from system import Configurator
from pandas import DataFrame
import pandas as pd, pymysql, os


class CloudSql:
    """
    Helper class to interact with Google Cloud SQL
    """

    def __init__(self, configurator: Configurator):
        required_configuration = {'cloud_sql', 'cloud_sql.host', 'cloud_sql.username', 'cloud_sql.password',
                                  'cloud_sql.database', 'cloud_sql.instance_connection_name'}
        for key in required_configuration:
            if configurator.get(key) is None:
                raise ValueError('[Error] Configuration `{}` is not defined.'.format(key))
        self.db_connection_name = configurator.get('cloud_sql.instance_connection_name')
        self.db_host = configurator.get('cloud_sql.host')
        self.db_user = configurator.get('cloud_sql.username')
        self.db_password = configurator.get('cloud_sql.password')
        self.db_name = configurator.get('cloud_sql.database')

    def __connect(self) -> bool:
        """Create connection to Cloud SQL for both run locally and on App Engine"""

        try:
            # When deployed to App Engine, the `GAE_ENV` environment variable will be set to `standard`
            if os.environ.get('GAE_ENV') == 'standard':
                # If deployed, use the local socket interface for accessing Cloud SQL
                unix_socket = '/cloudsql/{}'.format(self.db_connection_name)
                connection = pymysql.connect(user=self.db_user, password=self.db_password,
                                             unix_socket=unix_socket, db=self.db_name)
            else:
                # If running locally, use the TCP connections instead
                connection = pymysql.connect(user=self.db_user, password=self.db_password,
                                             host=self.db_host, db=self.db_name)
            self.connection = connection

            return True
        except Exception as e:
            print('ERROR:', e)
            return False

    def __close_connection(self) -> bool:
        """Close MySQL (on Cloud SQL) connection"""

        self.connection.close()
        return True

    def query(self, sql: str) -> List:
        """Enquiry data according to supplied SQL command"""

        if self.__connect():
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            self.__close_connection()

        return result

    def query_df(self, sql: str) -> DataFrame:
        """Enquiry data and return data set in DataFrame format"""

        df = None
        if self.__connect():
            df = pd.read_sql(sql, self.connection)
            self.__close_connection()

        return df

