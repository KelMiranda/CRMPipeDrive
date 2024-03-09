from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable
from processes.cotizaciones import Cotizaciones

if __name__ == '__main__':
    ct = IngresoDeCotizaciones('SV')
    result = ct.cotizaciones_diarias()
    save_json(result, 'Cotizaciones_Diarias')
    result1 = ct.cotizaciones_actualizadas()
    save_json(result1, 'Cotizaciones_Actualizadas')
    '''
    result = GetIdUser().validador_de_usuarios()
    save_json(result, 'Reporte_Usuarios')
    OrganizationTable('DatosClientes', 'SV').cotizaciones_por_clientes()
    Cotizaciones('SV').datos_cliente('C1413250')'''

