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
from telegram.apitelegram import TelegramBot
from processes.proceso_cliente import Cliente

if __name__ == '__main__':

    #datos= Cotizaciones('SV').datos_de_la_cotizacion(546533,716118)
    #print(datos)


    pais = ['SV', 'GT', 'HN']
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
    bot.send_message(1947314689)

    #print(get_all_deals())

    #print(Cliente('SV').ingresando_cliente('C1809835'))
    #print(Cliente('SV').validadorCliente('C1649364'))
    #print(Cliente('SV').construir_datos_cliente('C1649364'))



    '''ct = IngresoDeCotizaciones('SV')
    print(ct.proceso_cotizaciones_pipedrive())'''

    '''ct = IngresoDeCotizaciones('SV')
    #print(ct.cotizaciones_actualizadas())
    print(ct.proceso_cotizaciones_pipedrive())'''