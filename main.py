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

    pais = ['SV', 'GT', 'HN']
    '''for row in pais:
        ct = IngresoDeCotizaciones(f'{row}')
        result = ct.cotizaciones_diarias(3)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')'''

    ct = Cotizaciones('HN')
    cotizacion = ct.datos_de_la_cotizacion(5939,8950)
    print(cotizacion)
    '''for row in pais:
        ct = IngresoDeCotizaciones(f'{row}')
        print(ct.proceso_clientes_dias(1))
        print(ct.proceso_cotizaciones_dia(1))'''

    '''cliente = Cliente('SV')
    cliente.ingresando_cliente('C057239870')'''

    ct = IngresoDeCotizaciones('SV')
    print(ct.proceso_cotizacion_validador())
