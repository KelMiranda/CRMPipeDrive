from unittest import result
import pandas as pd
from processes.cotizaciones import Cotizaciones
from processes.proceso_cliente import Cliente
import datetime as dt
from database.sql_server_connection import SQLServerDatabase
from processes.cotizaciones import Cotizaciones
import time
import json
from processes.proceso_cliente import log_error


class IngresoDeCotizaciones:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.ct = Cotizaciones(f'{self.pais}')
        self.cliente = Cliente(f'{self.pais}')

    def comparar_registros_clientes(self, card_code):
        """
        Ejecuta el procedimiento almacenado CompararRegistrosClientes_SV para comparar los registros de un cliente.

        Parámetros:
        - card_code (str): Código único del cliente a comparar.

        Retorna:
        - None: Si no se encontraron registros para el cliente.
        - True: Si los registros son diferentes.
        - False: Si no hay cambios en los registros.
        """
        try:
            # Crear la consulta SQL para ejecutar el procedimiento almacenado
            query = f"EXEC CompararRegistrosClientes_{self.pais} @CardCode = '{card_code}'"

            # Ejecutar el procedimiento almacenado y obtener el resultado
            result = self.db.execute_query(query)

            # Interpretar el resultado
            if result:
                resultado_comparacion = result[0][0]
                if resultado_comparacion is None:
                    return None  # No se encontraron registros
                elif resultado_comparacion == 1:
                    return True  # Registros diferentes
                elif resultado_comparacion == 0:
                    return False  # No hay cambios
            else:
                return None  # En caso de que no haya resultados

        except Exception as e:
            print(f"Error al ejecutar comparar_registros_clientes: {e}")
            return None

    def cotizaciones_actualizadas(self):
        errores = []
        result = []
        cotizaciones = self.ct.cierre_de_cotizaciones()[0]
        self.db.connect()
        for row in cotizaciones:
            time.sleep(5)
            try:
                ultima_version = self.ct.ultima_version(row[3], row[2], row[6])[0]
                query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}] '{ultima_version[0][0]}', {ultima_version[0][1]}, '{ultima_version[0][2]}', '{ultima_version[0][3]}'"
                self.db.execute_query(query, False)
                result.append(
                    {'DocNum': row[3], 'Codigo Del Cliente': f"{row[6]}", 'msg': 'Se ha actualizado el documento'})
            except Exception as e:
                errores.append({'DocNum': row[3], 'Codigo Del Cliente': f"{row[6]}", 'msg_error': str(e)})
            finally:
                print(
                    f"##########################Terminando el analisis#####################################################")

        self.db.disconnect()
        output = {
            'resultados': result,
            'errores': errores,
        }
        return output

    def cotizaciones_este_dia(self, days):
        """
        Esta función trae todas las cotizaciones del día y verifica si el cliente y la cotización existen en la base de datos.
        Crea un DataFrame con la información de las cotizaciones y añade dos columnas adicionales:
        - CT_E: Indica si la cotización ya existe en la base de datos (True o False).
        - C_E: Indica si el cliente ya existe en la base de datos (True o False).
        - C_M: Indica si hay cambios en los datos del cliente (True, False, o None).
        """
        try:
            # Verifica si la conexión ya está abierta
            already_connected = self.db.is_connected()
            if not already_connected:
                self.db.connect()

            today = dt.date.today()
            one_day = dt.timedelta(days=days)
            yesterday = today-one_day
            result = self.ct.cotizaciones_del_dia(f'{yesterday}')[0]

            # Convertir la lista plana en una lista de tuplas
            result_list = [list(tup) for tup in result]
            columnas = ['Serie', 'DocNum', 'CardCode', 'ORD', 'DocEntry']
            dataFrame = pd.DataFrame(result_list, columns=columnas)

            # Verificación en la base de datos
            resultados_cotizacion = []
            resultados_cliente = []
            resultados_comparacion = []

            for index, row in dataFrame.iterrows():
                card_code = row['CardCode']

                # Verificar si los datos del cliente han cambiado
                resultado_comparacion = self.comparar_registros_clientes(card_code)
                resultados_comparacion.append(resultado_comparacion)

                # Verificar si la cotización ya existe en la base de datos
                query_cotizacion = f"""
                    SELECT COUNT(*)
                    FROM DatosProyectos_PipeDrive
                    WHERE Serie = '{row['Serie']}'
                    AND DocNum = {row['DocNum']}
                    AND ORD = '{row['ORD']}' 
                    AND PAIS = '{self.pais}'
                """
                count_cotizacion = self.db.execute_query(query_cotizacion)
                if count_cotizacion:
                    resultados_cotizacion.append(count_cotizacion[0][0] > 0)
                else:
                    resultados_cotizacion.append(False)

                # Verificar si el cliente ya existe en la base de datos
                query_cliente = f"""
                    SELECT COUNT(*)
                    FROM DatosClientes
                    WHERE CardCode = '{row['CardCode']}' 
                    AND PAIS = '{self.pais}'
                """
                count_cliente = self.db.execute_query(query_cliente)
                if count_cliente:
                    resultados_cliente.append(count_cliente[0][0] > 0)
                else:
                    resultados_cliente.append(False)

            # Agregar los resultados al DataFrame
            dataFrame['CT_E'] = resultados_cotizacion
            dataFrame['C_E'] = resultados_cliente
            dataFrame['C_M'] = resultados_comparacion

            return dataFrame

        except Exception as e:
            print(f"Error al ejecutar cotizacionesDiarias: {e}")
            return None

        finally:
            # Desconectar solo si la conexión no estaba ya abierta antes
            if not already_connected:
                self.db.disconnect()

    def proceso_clientes_dias(self, days):
        try:
            count = 0
            dt = self.cotizaciones_este_dia(days)
            if dt is not None:
                # Filtrar las filas donde C_M es True o C_E es False
                dt_filtered = dt[(dt['C_M'] == True) | (dt['C_E'] == False)]
                try:
                    self.db.connect()
                    for index, row in dt_filtered.iterrows():
                        count = count + 1
                        query = f"exec [dbo].[SP_VALIDADOR_CLIENTE_MERGE_{self.pais}] '{row['CardCode']}'"
                        try:
                            self.db.execute_query(query, False)
                        except Exception as e:
                            error_message = f"Error al ejecutar la consulta para CardCode '{row['CardCode']}': {e}"
                            log_error(error_message)
                        try:
                            self.cliente.ingresando_cliente(row['CardCode'])
                        except Exception as e:
                            error_message = f"Error al ejecutar la funcion ingresando cliente para CardCode '{row['CardCode']}': {e}"
                            log_error(error_message)
                except Exception as e:
                    error_message = f"Error al conectar a la base de datos: {e}"
                    log_error(error_message)
                finally:
                    self.db.disconnect()

                # Mostrar el DataFrame filtrado
                print(dt_filtered)
            else:
                error_message = "No se pudo obtener las cotizaciones para el día especificado."
                log_error(error_message)
        except Exception as e:
            error_message = f"Error en el proceso de cotizaciones del día: {e}"
            log_error(error_message)

    def proceso_cotizaciones_dia(self, days):
        count = 0
        try:
            dt = self.cotizaciones_este_dia(days)
            if dt is not None:
                dt_filtered = dt[(dt['CT_E'] == False)]
                try:
                    self.db.connect()
                    for index, row in dt_filtered.iterrows():
                        time.sleep(3)
                        count = count + 1
                        query = f"[dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}] '{row['ORD']}', '{row['DocNum']}', '{row['Serie']}', '{row['CardCode']}'"
                        try:
                            self.db.execute_query(query, False)
                        except Exception as e:
                            error_message = f"Error al ejecutar la consulta para CardCode '{row['CardCode']}': {e}"
                            log_error(error_message)
                        try:
                            print(f"-------------------------------Cotizacion #{count}--------------------------------")
                            #self.cliente.ingresando_cliente(row['CardCode'])
                        except Exception as e:
                            error_message = f"Error al ejecutar la funcion ingresando cliente para CardCode '{row['CardCode']}': {e}"
                            log_error(error_message)
                except Exception as e:
                    error_message = f"Error al conectar a la base de datos: {e}"
                    log_error(error_message)
                finally:
                    self.db.disconnect()

                # Mostrar el DataFrame filtrado
                print(dt_filtered)
            else:
                error_message = "No se pudo obtener las cotizaciones para el día especificado."
                log_error(error_message)
        except Exception as e:
            error_message = f"Error en el proceso de cotizaciones del día: {e}"
            log_error(error_message)

    def proceso_cotizacion_validador(self):
        try:
            self.db.connect()

            # Realizamos una sola consulta para ambos validadores 'C' y 'U'
            query = f"""
                Select DocNum, DocEntry, id_proyecto, Validador, id_deal 
                from DatosProyectos_PipeDrive 
                Where Validador IN ('C', 'U') 
                AND Pais = '{self.pais}'"""

            result = self.db.execute_query(query)

            # Convertimos los resultados en una lista de listas
            result_list = [list(tup) for tup in result]

            # Definimos las columnas, incluyendo la nueva columna 'Validador'
            columnas = ['DocNum', 'DocEntry', 'id_proyecto', 'Validador', 'id_deal']

            # Creamos el DataFrame con los resultados
            dataFrame = pd.DataFrame(result_list, columns=columnas)

            # Mostramos el DataFrame
            return dataFrame

        except Exception as e:
            # Si ocurre un error, lo registramos en el archivo error.log
            log_error(f"Error en proceso_cotizacion_validador: {str(e)}")

    def proceso_cotizaciones_pipedrive(self):
        try:
            dt = self.proceso_cotizacion_validador()
            if dt is not None:
                dt_filtered = dt[(dt['Validador'] == 'C')]
                try:
                    self.db.connect()
                    for index, row in dt_filtered.iterrows():
                        time.sleep(3)
                        count = count + 1
                        datos = self.ct.datos_de_la_cotizacion()
                        try:
                            print(datos)
                        except Exception as e:
                            error_message = f"Error al ejecutar la consulta para CardCode '{row['CardCode']}': {e}"
                            log_error(error_message)
                        try:
                            print(f"-------------------------------Cotizacion #{count}--------------------------------")
                            # self.cliente.ingresando_cliente(row['CardCode'])
                        except Exception as e:
                            error_message = f"Error al ejecutar la funcion ingresando cliente para CardCode '{row['CardCode']}': {e}"
                            log_error(error_message)
                except Exception as e:
                    error_message = f"Error al conectar a la base de datos: {e}"
                    log_error(error_message)
                finally:
                    self.db.disconnect()

                # Mostrar el DataFrame filtrado
                print(dt_filtered)
            else:
                error_message = "No se pudo obtener las cotizaciones para el día especificado."
                log_error(error_message)
        except Exception as e:
            error_message = f"Error en el proceso de cotizaciones del día: {e}"
            log_error(error_message)







