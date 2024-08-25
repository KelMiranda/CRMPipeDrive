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
        result = ct.cotizaciones_diarias(1)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')

    '''
    '''ct = IngresoDeCotizaciones('SV')
    print(ct.cotizacionesDiarias())
    #print(ct.comparar_registros_clientes('C219380'))'''

    # Crear una instancia de la clase OrganizationTable
    cliente = OrganizationTable(None, 'GT')

    # Obtener los datos de la tabla y la vista
    clienteCRM = cliente.hashTablaClientes('C2443', 'DatosClientes')
    clienteCRM = clienteCRM.reset_index(drop=True)  # Asegurar que el índice esté alineado
    print(clienteCRM.iloc[0])  # Imprimir el primer registro completo del DataFrame

    clienteVista = cliente.hashTablaClientes('C2443', '[dbo].[VW_DATOS_CLIENTES_GT]')
    clienteVista = clienteVista.reset_index(drop=True)  # Asegurar que el índice esté alineado
    print(clienteVista.iloc[0])  # Imprimir el primer registro completo del DataFrame

    # Comparar los hashes entre ambos DataFrames
    hash_comparison = clienteCRM['hash'] == clienteVista['hash']

    # Verificar si todos los hashes son iguales
    if hash_comparison.all():
        print("El Hash de la tabla es igual al de la vista")
    else:
        print("Se encontraron diferencias en los hashes entre clienteCRM y clienteVista.")
        # Mostrar las filas con diferencias
        diferencias = pd.concat([clienteCRM, clienteVista], axis=1, keys=['clienteCRM', 'clienteVista'])
        diferencias = diferencias[~hash_comparison]
        print("Diferencias encontradas:")
        print(diferencias)


