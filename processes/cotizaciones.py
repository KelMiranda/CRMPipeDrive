from database.sql_server_connection import SQLServerDatabase
from time import sleep


def notificar_errores(errores):
        # Aquí puedes implementar la lógica para enviar notificaciones con la lista de errores
        print("Enviando notificación de errores:", errores)

        

class Cotizaciones:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
    

    def cierre_de_cotizaciones(self):
        errores = []
        query = f'EXEC [dbo].[SP_CERRANDO_COTIZACIONES_{self.pais}]'

        try:
            self.db.connect()
            result = self.db.execute_query(query)

        
        except Exception as e:
            error_message = f"Error al ejecutar la consulta dicho error es: {str(e)}"
            errores.append(error_message)

        finally:
            self.db.disconnect()
        
        if errores:
            notificar_errores(errores)
        
        return result, errores
    
    def validar_cotizacion(self, ord=None, docnum=None, serie=None):
        documentos_actualizados = []
        errores = []
        if ord is None and docnum is None and serie is None:
            result = self.cierre_de_cotizaciones()
            if len(result[0]) == 0:
                documentos_actualizados.append(f'No hay cotizaciones en la funcion de cierre en: {self.pais}')
                errores.append(f"No hay error en la funcion de cierre en: {self.pais}")
            else:
                total = len(result[0])
                for count, row in enumerate(result[0], start=1):
                    iter = total - count
                    print(f"-------------#Documentos Faltantes: {iter}---------------------------")
                    query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{row[2]}',{row[3]},'{row[4]}'"
                    try:
                        self.db.connect()
                        query_result = self.db.execute_query(query, False)
                        documentos_actualizados.append(row[3])
                        if query_result is not None:
                            errores.append(f"Consulta vacía en iteración {count}")
                    except Exception as e:
                        error_message = f"Error al ejecutar consulta en iteración {count}: {str(e)}"
                        errores.append(error_message)
                    finally:
                        self.db.disconnect()

        else:
            query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{ord}',{docnum},'{serie}'"
            query_validador = f"Select * from DatosProyectos_PipeDrive Where DocNum = {docnum} AND ORD ='{ord}'"
            self.db.connect()
            query_validador_result = self.db.execute_query(query_validador)
            if query_validador_result:
                try:
                    query_result = self.db.execute_query(query, False)
                    if query_result is not None:
                        errores.append("Consulta vacía")
                    documentos_actualizados.append(docnum)
                except Exception as e:
                    error_message = f"Error al ejecutar consulta: {str(e)}"
                    errores.append(error_message)
                finally:
                    self.db.disconnect()
            else:
                error_message = f"El numero de documento: {docnum}, no pertenece a la tabla ORD{ord}"
                errores.append(error_message)

        print('######################Finalizando Proceso##########################################')
        return documentos_actualizados, errores
   
    def obtener_cotizacion(self, sector, validador):
        errores = []
        query = f"EXEC [dbo].[SP_SECTOR]'{self.pais}', '{sector}', '{validador}'"
        try:
            self.db.connect()
            result = self.db.execute_query(query)

        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def obtener_cotizaciones_abiertas(self, SlpName):
        errores = []
        query = f"Select SlpName, CardCode, CardName, COUNT(*) AS #Cotizaciones from DatosProyectos_PipeDrive Where DocStatus = 'O' AND Pais = '{self.pais}' AND SlpName = '{SlpName}' Group By SlpName, CardCode, CardName Order By #Cotizaciones desc"
        try:
            self.db.connect()
            result = self.db.execute_query(query)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def obtener_docnum_cotizacion(self, codigo_cliente):
        errores = []
        query = f"Select DocNum from DatosProyectos_PipeDrive Where CardCode = '{codigo_cliente}' AND DocStatus = 'O'"
        try:
            self.db.connect()
            result = self.db.execute_query(query)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores
