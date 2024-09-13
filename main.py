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

    '''pais = ['SV', 'GT', 'HN']
    for row in pais:
        try:
            ct = IngresoDeCotizaciones(f'{row}')
            print(ct.proceso_clientes_dias(1))
            print(ct.cotizaciones_actualizadas())
            print(ct.proceso_cotizaciones_dia(1))
            print(ct.proceso_cotizaciones_pipedrive())
        except Exception as e:
            print(f'Ocurrió un error con el país {row}: {e}')'''



