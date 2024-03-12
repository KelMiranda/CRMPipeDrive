import time

from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable
from processes.cotizaciones import Cotizaciones
from database.sql_server_connection import SQLServerDatabase

if __name__ == '__main__':
    '''ct = IngresoDeCotizaciones('SV')
    result = ct.cotizaciones_diarias(1)
    save_json(result, 'Cotizaciones_Diarias')
    result1 = ct.cotizaciones_actualizadas()
    save_json(result1, 'Cotizaciones_Actualizadas')'''
    db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
    query = "Select * from DatosClientes Where Pais = 'GT'"
    db.connect()
    result = db.execute_query(query)
    resultado = []
    for row in result:
        time.sleep(0.1)
        valor = Cotizaciones('GT').datos_cliente(row[1])
        if valor.get('Diferencia de datos entre POS y VW_POS'):
            query2 = f"EXEC [dbo].[SP_VALIDADOR_CLIENTE_MERGE_GT] '{row[1]}'"
            ingress = db.execute_query(query2, False)
            dato = {
                'Codigo de cliente': row[1],
                'Mensaje': 'Se Modifico este cliente'
            }
            resultado.append(dato)
    print(resultado)
