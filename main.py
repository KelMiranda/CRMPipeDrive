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

    pais = ['SV', 'GT']
    #result = IngresoDeCotizaciones('SV').validacion_cliente(0)
    #print(result)

    '''for row in pais:
        ct = IngresoDeCotizaciones(f'{row}')
        result = ct.cotizaciones_diarias(1)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')
        save_json(result_act, f'Cotizaciones_actualizadas_{row}')
    '''
    #Cliente('GT').ingresar_o_actualizar_cliente_pipedrive('C2584')
    print(Cotizaciones('SV').datos_de_la_cotizacion(16206, 21156))


