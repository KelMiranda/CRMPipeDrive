import os

import pyodbc


class SQLServerDatabase:
    def __init__(self, server, database, username, password):
        self.server = os.getenv(server)
        self.database = os.getenv(database)
        self.username = os.getenv(username)
        self.password = os.getenv(password)
        self.connection = None

    def connect(self):
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.connection = pyodbc.connect(connection_string)
            print("Connected to SQL Server.")
        except pyodbc.Error as e:
            print(connection_string)
            print(f"Error connecting to SQL Server: {e}")

    def execute_query(self, query, params=None):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
            except pyodbc.Error as e:
                print(f"Error executing query: {e}")
        else:
            print("No database connection.")

    def insert_query(self, query, params=None):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.rowcount
            except pyodbc.Error as e:
                print(f"Error executing query: {e}")
        else:
            print("No database connection.")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
        else:
            print("No connection to close.")
