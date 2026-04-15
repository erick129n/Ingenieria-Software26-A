from src.utils.logger import Logger
import mysql.connector
from decouple import config
import traceback

class Connection:
    def __init__(self):
        self.user = config('MYSQL_USER')
        self.password = config('MYSQL_PASSWORD')
        self.database = config('MYSQL_DATABASE')
        self.host = config('MYSQL_HOST')
        self.port = config('MYSQL_PORT')
        self.conn = None

    def open(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conn.is_connected():
                return self.conn
            else:
                return None
        except mysql.connector.Error as err:
            Logger.add_to_log('error', "Mysql error: " + str(err))
            Logger.add_to_log('error', traceback.format_exc())
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
            return None

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
        self.conn = None

    def print(self):
        try:
            self.conn = mysql.connector.connect()
            query = "select * from taller.usuarios"
            cursor = self.conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
        except Exception as e:
            Logger.add_to_log('error', str(e))
            Logger.add_to_log('error', traceback.format_exc())
        finally:
            self.conn.close()
            self.conn = None