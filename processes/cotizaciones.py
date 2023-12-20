from database.sql_server_connection import SQLServerDatabase


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
    
    def validando_cotizacion(self, ord=None, docnum=None, serie=None):
        documentos_actualizados=[]
        if ord is None and docnum is None and serie is None:
            result = self.cierre_de_cotizaciones()
            total = len(result)
            count = -1
            for row in result:
                count = count + 1
                iter = total - count
                print(f"-------------#Documentos Faltantes: {iter}---------------------------")
                query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{row[2]}',{row[3]},'{row[4]}'"
                self.db.connect()
                print(self.db.execute_query(query))
                self.db.disconnect() 
                documentos_actualizados.append(row[3])
        else:
            query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{ord}',{docnum},'{serie}'"
            self.db.connect()
            print(query)
            documentos_actualizados.append(docnum)
            #self.db.execute_query(query)
            self.db.disconnect
        print('######################Finalizando Proceso##########################################')
        return documentos_actualizados
        
