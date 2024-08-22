import time
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable
from processes.cotizaciones import Cotizaciones
from database.sql_server_connection import SQLServerDatabase
from processes.deals import DealTable
from processes.proceso_cliente import Cliente

if __name__ == '__main__':

    '''pais = ['SV', 'GT']
    for row in pais:
        ct = IngresoDeCotizaciones(f'{row}')
        result = ct.cotizaciones_diarias(1)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')'''

    ct = IngresoDeCotizaciones('SV')
    print(ct.cotizacionesDiarias())
    #print(ct.comparar_registros_clientes('C219380'))