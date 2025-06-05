import time
import asyncio
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from processes.deals import get_all_deals
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable, generar_hash_sha256
from processes.cotizaciones import Cotizaciones
from database.sql_server_connection import SQLServerDatabase
from processes.deals import DealTable
from processes.proceso_cliente import Cliente
import pandas as pd
import numpy as np
from telegram.apitelegram import TelegramBot
from processes.proceso_cliente import Cliente
import pipedrive.pipedrive_api_conecction as connection
#from IPython.display import display
from app import procesar_usuarios

if __name__ == '__main__':

    #datos= Cotizaciones('SV').datos_de_la_cotizacion(546533,716118)
    #print(datos)Lenovo legion


    '''pais = ['HN', 'SV', 'GT']
    for row in pais:
        try:
            print(f"#############################Inicio de los proceso para {row}###################################")
            ct = IngresoDeCotizaciones(f'{row}')
            print(ct.proceso_clientes_dias(1))
            print(f"#####################Finalizando proceso clientes dias para {row}###############################")
            print(ct.cotizaciones_actualizadas())
            print(f"#####################Finalizando cotizaciones actualizadas para {row}###########################")
            print(ct.proceso_cotizaciones_dia(1))
            print(f"#####################Finalizando proceso cotizaciones dias para {row}###########################")
            print(ct.proceso_cotizaciones_pipedrive())
            print(f"#####################Finalizando proceso cotizaciones pipedrive para {row}######################")
            print(f"##############################Finalizando proceso para {row}####################################")
            # Usar asyncio.sleep en lugar de time.sleep para no bloquear el proceso
        except Exception as e:
            print(f'Ocurrió un error con el país {row}: {e}')

    bot = TelegramBot(None)
    bot.send_message(1947314689)'''


    data = procesar_usuarios()
    print(data)
    #arr = np.array(data)
    #  print(arr.shape)


    #all_deals = get_all_deals()
    #df = pd.read_json("./2025/2025-05/2025-05-19/deals-2025-05-19.json")
    #display(df.head(10))

    #print(Cliente('SV').ingresando_cliente('C5223'))
    #print(Cliente('SV').validadorCliente('C5223'))
    #usuarios = connection.PipedriveAPI('Token').get_all_user()
    #print(usuarios)
    #print(Cliente('SV').construir_datos_cliente('C1649364'))



    '''ct = IngresoDeCotizaciones('SV')
    print(ct.proceso_cotizaciones_pipedrive())'''

    '''ct = IngresoDeCotizaciones('SV')
    #print(ct.cotizaciones_actualizadas())
    print(ct.proceso_cotizaciones_pipedrive())'''