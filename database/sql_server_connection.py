import os

import pyodbc


class SQLServerDatabase:
    def __init__(self, server, database, username, password):
        self.server = os.getenv(server)
        self.database = os.getenv(database)
        self.username = os.getenv(username)
        self.password = os.getenv(password)

    def connect(self):
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.connection = pyodbc.connect(connection_string)
            print("Connected to SQL Server.")
        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from SQL Server.")
            self.connection = None
        else:
            print("No active connection to disconnect from.")

    def execute_query(self, query, return_results=True):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                if return_results:
                    results = cursor.fetchall()
                    return results
                else:
                    print(f"Número de filas afectadas: {cursor.rowcount}")
                    return None

        except pyodbc.Error as ex:
            print('Error connecting to database:', ex)
            return None

