from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

import time 

import logging
logger = logging.getLogger(__name__)

import mysql.connector

from config.config import app_config
from classes.response_objects import TimerStatus
from classes.timer import TimerInformation

TABLES = {}
TABLES['timers'] = (
    "CREATE TABLE timers ("
    " timer_id BINARY(16) PRIMARY KEY,"
    " timer_url VARCHAR(2083),"
    " timer_status ENUM ('waiting','executing','done','failed') NOT NULL,"
    " timer_invoke_time DATETIME NOT NULL)"
    " ENGINE=InnoDB"
)

class DbApi():
    db_connection = None
    reconnect_tries = 0
    def __init__(self,
                 user,password,host,database) -> None:           
        try:
            self.user = user
            self.password = password
            self.host=host
            self.database=database
            self.db_connection = self.connect_to_db()

        except Exception as err:
            logger.error(f"Couldn't connect to DB: {err}")

    def insert_timer(self, timer_url, timer_invoke_date: datetime) -> str:
        
        insert_query = "INSERT INTO timers (timer_id,timer_url, timer_status,timer_invoke_time) VALUES (UUID_TO_BIN(%(timer_id)s),%(timer_url)s,%(timer_status)s,%(timer_date)s)"

        

        insert_data = TimerInformation(timer_id=str(uuid4()),
                                       timer_url=str(timer_url),
                                       timer_status=TimerStatus.waiting.value,
                                       timer_date=timer_invoke_date)
        db_cursor = None
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(insert_query,insert_data.for_sql_query())
            self.db_connection.commit()
        except mysql.connector.Error as err:
            if err.errno != 1146:
                self.__error_handler__(err)
            self.create_table(TABLES["timers"])
            db_cursor.execute(insert_query,insert_data)
        except Exception as err:
            self.__error_handler__(err)
        finally:
            if db_cursor:
                db_cursor.close()
        return insert_data.timer_id


    
    def get_timer_information(self, timer_uuid) -> TimerInformation:
        
        get_query = "SELECT BIN_TO_UUID(timer_id), timer_url, timer_status, timer_invoke_time from timers where timer_id=UUID_TO_BIN(%(timer_id)s)"

        

        select_data = {
            "timer_id": timer_uuid
        }
        db_cursor = None
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(get_query,select_data)
            response = db_cursor.fetchone()
        except mysql.connector.Error as err:
            if err.errno!=1411:
                self.__error_handler__(err)
            raise HTTPException(status_code=400, detail="Illegal UUID")
        except Exception as err:
            self.__error_handler__(err)
        finally:
            if db_cursor:
                db_cursor.close()
        if not response:
            return None
        timer_id, timer_url, timer_status, timer_invoke_time = response
        return TimerInformation(timer_id=timer_id, timer_url=timer_url, timer_status=timer_status, timer_date=timer_invoke_time)

    

    def connect_to_db(self):
        if self.reconnect_tries > app_config.RETRY_NUMBER:
            self.reconnect_tries=0
            raise HTTPException(status_code=503,detail="Can't establish connection to DB (10 reties)")
        try:
            self.reconnect_tries+=1
            connection = mysql.connector.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    database=self.database)
            self.reconnect_tries = 0
            logger.info(f"Connected to DB. HOST={self.host}, DATABASE={self.database}")
            return connection
        except mysql.connector.Error as err:
            if err.errno == 1049: # No database
                self.create_db(mysql.connector.connect(user=self.user,password=self.password,host=self.host), database=self.database)
                return self.connect_to_db(user=self.user, password=self.password, host=self.host, database=self.database)
            self.__error_handler__(err)
        except Exception as err:
            self.__error_handler__(err)

    def create_table(self, table_query):
        try:
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
            if (self.current_cursor):
                    self.current_cursor.close()
            if (self.db_connection):
                self.db_connection.close()
            logger.info("Connection to db is closed")
        except Exception as err:
            logger.error(f"Couldn't close DB Connection: {err}")

    def __error_handler__(self,err):
        if not self.db_connection:
            self.__db_reconnect_handler__()
        if type(err) in (mysql.connector.errors.OperationalError, mysql.connector.errors.DatabaseError, mysql.connector.Error):
            if 'MySQL Connection not available' in str(err) or err.errno in (2013,2003):
                self.__db_reconnect_handler__()
            logger.error(f"Unexpected DB Error: {err}")
            raise HTTPException(status_code=503, detail=f"Cannot Communicate with DB")
        logger.error(f"Unexpected Error: {err}")
        raise HTTPException(status_code=500, detail=f"Unexpected Internal Error")

    def __db_reconnect_handler__(self):
        logger.error(f"Lost Connection to DB. Sleep for {app_config.RECONNECT_WAIT_TIME} seconds and reconnect again")
        time.sleep(app_config.RECONNECT_WAIT_TIME)
        self.db_connection=self.connect_to_db()
        if not self.db_connection:
            raise HTTPException(status_code=503, detail="Could not Reconnect to DB ") 
        return
    
db_instance = DbApi(user=app_config.DB_USER,
                    password=app_config.DB_PASSWORD,
                    host=app_config.DB_HOST,
                    database=app_config.DB_NAME)