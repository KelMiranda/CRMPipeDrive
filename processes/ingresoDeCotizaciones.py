from unittest import result
from processes.cotizaciones import Cotizaciones
import datetime as dt
from database.sql_server_connection import SQLServerDatabase
import time
import json


class IngresoDeCotizaciones:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.ct = Cotizaciones(f'{self.pais}')

    def cotizaciones_diarias(self):
        errores = []
        result = []
        today = dt.date.today()
        one_day = dt.timedelta(days=1)
        yesterday = today - one_day
        ct = Cotizaciones(f'{self.pais}')
        self.db.connect()
        for row in ct.cotizaciones_del_dia(f"'{yesterday}'")[0]:
            time.sleep(5)
            print(row)
            query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{row[3]}', {row[1]}, '{row[0]}', '{row[2]}'"
            try:
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

    def trato_pipedrive(self, DocNum, DocEntry):
        data = {}
        datosFamilia = self.ct.familia_padre_de_la_cotizacion(DocNum, DocEntry)
        datosCotizacion = self.ct.datos_de_la_cotizacion(DocNum, DocEntry)


