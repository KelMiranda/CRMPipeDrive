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


def ingreso_o_actualizacion_de_cliente(Pais):
    ct = Cotizaciones(Pais)
    cl = Cliente(Pais)
    resultado = ct.clientes_por_sector_validador('U')
    total = resultado[1]
    count = 0
    for row in resultado[0]:
        faltante = total - count
        time.sleep(0.2)
        print(f"----------------------Cliente: {row[0]}     Faltan: {faltante}------------------------------------------")
        cl.ingresar_o_actualizar_cliente_pipedrive(row[0])
        count = count + 1


if __name__ == '__main__':

    pais = ['SV', 'GT']
    result = IngresoDeCotizaciones('SV').validacion_cliente(0)
    print(result)

    for row in pais:
        '''ct = IngresoDeCotizaciones(f'{row}')
        result = ct.cotizaciones_diarias(2)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')
        save_json(result_act, f'Cotizaciones_actualizadas_{row}')'''


