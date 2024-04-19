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

    def execute_query_with_params(self, query, params=None, return_results=True):
            """
            Ejecuta una consulta SQL con parámetros opcionales y devuelve los resultados o el número de filas afectadas.

            Args:
            - query (str): Consulta SQL a ejecutar.
            - params (tuple/list/dict, optional): Parámetros para la consulta SQL. Default is None.
            - return_results (bool): Si es True, devuelve los resultados de la consulta; si es False, imprime el número de filas afectadas.

            Returns:
            - list/tuple: Resultados de la consulta si return_results es True.
            - None: Si return_results es False, no devuelve nada pero imprime el número de filas afectadas.
            """
            try:
                with self.connection as conn:
                    cursor = conn.cursor()
                    cursor.execute(query, params)  # Pasar los parámetros al método execute.

                    if return_results:
                        results = cursor.fetchall()  # Obtener todos los resultados de la consulta.
                        return results
                    else:
                        print(f"Número de filas afectadas: {cursor.rowcount}")  # Imprimir el número de filas afectadas.
                        return None
            except Exception as e:
                print(f"Ocurrió un error al ejecutar la consulta: {e}")
                return None


