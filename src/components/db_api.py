from datetime import datetime

import logging
logger = logging.getLogger(__name__)

import mysql.connector

from config.config import app_config


TABLES = {}
TABLES['timers'] = (
    "CREATE TABLE timers ("
    " timer_id BINARY(16) PRIMARY KEY,"
    " timer_url VARCHAR(2083)"
    " timer_status ENUM ('waiting','executing','done','failed') NOT NULL,"
    " timer_invoke_time DATETIME NOT NULL)"
    " ENGINE=InnoDB"
)

class DbApi():

    def __init__(self,
                 user,password,host,database) -> None:           
        try:
            self.db_connection = self.connect_to_db(user=user, password=password, host=host, database=database)
            logger.info(f"Connected to DB. HOST={host}, DATABASE={database}")
        except Exception as err:
            logger.error(f"Couldn't connect to DB: {err}")

    def insert_timer(self, timer_url, timer_invoke_date: datetime) -> str:

        insert_query = "INSERT INTO timers (timer_id,timer_status,timer_invoke_time) VALUES (UUID_TO_BIN(UUID()),%(timer_url)s,%(timer_date)s)"
        db_cursor = self.db_connection.cursor()

        insert_data = {
            "timer_url": str(timer_url),
            "timer_date": timer_invoke_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            db_cursor.execute(insert_query,insert_data )
        except mysql.connector.Error as err:
            if err.errno == 1146: # Table doesn't exists
                self.create_table(TABLES["timers"])
            db_cursor.execute(insert_query,insert_data )
        except Exception as err:
            if db_cursor:
                db_cursor.close()
            logger.error(f"Unexpected Error: {err}")
        breakpoint()
        # //timer_id = db_cursor
        db_cursor.close()

        pass

    def get_timer_status(self, timer_uuid):
        pass

    def connect_to_db(self, user,password,host,database):
        try:
            return mysql.connector.connect(user=user,
                                    password=password,
                                    host=host,
                                    database=database)
        except mysql.connector.Error as err:
            if err.errno == 1049: # No database
                self.create_db(mysql.connector.connect(user=user,password=password,host=host), database=database)
                return self.connect_to_db(user=user, password=password, host=host, database=database)
        except Exception as err:
            breakpoint()

    def create_table(self, table_query):
        try:
            breakpoint()
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(table_query)

            db_cursor.close()
        except Exception as err:
            logger.error(f"Failed to create table: {err}")

    def create_db(self, connection, database):
        try:
            db_cursor = connection.cursor()
            query_data = {
                "database": database
            }

            db_cursor.execute(f"CREATE DATABASE {database}")

            # db_cursor.commit()
            db_cursor.close()
            connection.close()
        except Exception as err:
            logger.error(f"Unexpected error while create db: {err}")
            breakpoint()

    def __del__(self):
        try:
            if (self.db_connection):
                self.db_connection.close()
            logger.info("Connection to db is closed")
        except Exception as err:
            logger.error(f"Couldn't close DB Connection: {err}")

db_instance = DbApi(user=app_config.db_user,
                    password=app_config.db_password,
                    host=app_config.db_host,
                    database=app_config.db_name)