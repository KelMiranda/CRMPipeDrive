from unittest import result
import pandas as pd
from processes.cotizaciones import Cotizaciones
from processes.proceso_cliente import Cliente
import datetime as dt
from database.sql_server_connection import SQLServerDatabase
from processes.cotizaciones import Cotizaciones
import time
import json


class IngresoDeCotizaciones:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.ct = Cotizaciones(f'{self.pais}')
        self.cliente = Cliente(f'{self.pais}')

    def cotizaciones_diarias(self, days):
        errores = []
        result = []
        today = dt.date.today()
        one_day = dt.timedelta(days=days)
        yesterday = today-one_day
        ct = Cotizaciones(f'{self.pais}')
        self.db.connect()
        for row in ct.cotizaciones_del_dia(f"{yesterday}")[0]:
            time.sleep(5)
            print(row)
            query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{row[3]}', {row[1]}, '{row[0]}', '{row[2]}'"
            try:
                #print(query)
                #print(self.cliente.ingresar_o_actualizar_cliente_pipedrive(f'{row[2]}'))
                self.db.execute_query(query, False)
                result.append({'DocNum': row[1], 'Codigo Del Cliente': f"{row[2]}"})

            except Exception as e:
                errores.append({'DocNum': row[1], 'Codigo Del Cliente': f"{row[2]}", 'msg_error': str(e)})
            finally:
                print(
                    f"##########################Terminando el analisis#####################################################")

        self.db.disconnect()
        output = {
            'resultados': result,
            'errores': errores,
        }
        return output

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

    #Esta funcion traera todas las cotizaciones del dia.
    def cotizacionesDiarias(self):
        try:
            today = dt.date.today()
            result = self.ct.cotizaciones_del_dia(f'{today}')[0]

            # Convertir la lista plana en una lista de tuplas
            result_list = [list(tup) for tup in result]
            columnas = ['Serie', 'DocNum', 'CardCode', 'ORD', 'DocEntry']
            dataFrame = pd.DataFrame(result_list, columns=columnas)

            # Verificación en la base de datos
            resultados = []

            for index, row in dataFrame.iterrows():
                query = f"""
                    SELECT COUNT(*)
                    FROM DatosProyectos_PipeDrive
                    WHERE Serie = '{row['Serie']}'
                    AND DocNum = {row['DocNum']}
                    AND ORD = '{row['ORD']}'
                """
                #self.db.connect()
                #count = self.db.execute_query(query)[0][0]

                #resultados.append(count > 0)
                print(query)

            # Agregar los resultados al DataFrame
            dataFrame['Existe'] = resultados

            print(dataFrame)
            return dataFrame

        except Exception as e:
            print(f"Error al ejecutar cotizacionesDiarias: {e}")
            return None










