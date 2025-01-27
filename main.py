import time
import asyncio
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
from telegram.apitelegram import TelegramBot

if __name__ == '__main__':

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