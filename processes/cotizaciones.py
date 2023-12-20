from database.sql_server_connection import SQLServerDatabase


def notificar_errores(errores):
        # Aquí puedes implementar la lógica para enviar notificaciones con la lista de errores
        print("Enviando notificación de errores:", errores)

        

class Cotizaciones:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
    

    def cierre_de_cotizaciones(self):
        self.db.connect()
        query = f'EXEC [dbo].[SP_CERRANDO_COTIZACIONES_{self.pais}]'
        result = self.db.execute_query(query)
        self.db.disconnect()
        return result
    
    def validar_cotizacion(self, ord=None, docnum=None, serie=None):
        documentos_actualizados = []
        errores = []

        if ord is None and docnum is None and serie is None:
            result = self.cierre_de_cotizaciones()
            total = len(result)

            for count, row in enumerate(result, start=1):
                iter = total - count
                print(f"-------------#Documentos Faltantes: {iter}---------------------------")
                query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{row[2]}',{row[3]},'{row[4]}'"
                try:
                    self.db.connect()
                    query_result = self.db.execute_query(query)
                    documentos_actualizados.append(row[3])
                    if not query_result:
                        errores.append(f"Consulta vacía en iteración {count}")
                except Exception as e:
                    error_message = f"Error al ejecutar consulta en iteración {count}: {str(e)}"
                    print(error_message)
                    errores.append(error_message)
                finally:
                    self.db.disconnect()

        else:
            query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{ord}',{docnum},'{serie}'"
            print(query)
            try:
                self.db.connect()
                query_result = self.db.execute_query(query)
                if not query_result:
                    errores.append("Consulta vacía")
                documentos_actualizados.append(docnum)
            except Exception as e:
                error_message = f"Error al ejecutar consulta: {str(e)}"
                print(error_message)
                errores.append(error_message)
            finally:
                self.db.disconnect()

        print('######################Finalizando Proceso##########################################')
        
        # Enviar notificación si hay errores
        if errores:
            notificar_errores(errores)
        
        return documentos_actualizados
