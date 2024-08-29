import time
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable, generar_hash_sha256
from processes.cotizaciones import Cotizaciones
from database.sql_server_connection import SQLServerDatabase
from processes.deals import DealTable
from processes.proceso_cliente import Cliente
import pandas as pd

if __name__ == '__main__':

    '''pais = ['SV', 'GT']
    for row in pais:
        ct = IngresoDeCotizaciones(f'{row}')
        result = ct.cotizaciones_diarias(3)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')'''

    print(Cliente('SV').ingresando_cliente('C000091857'))
    '''ct_sv = Cotizaciones('GT')
    va = ct_sv.datos_cliente_vw_table_pipedrive('C1065')
    print(va)
    valores = ct_sv.obtener_datos_vw('C1581')
    print(ct_sv.cliente_con_keys_pipedrive(valores))'''