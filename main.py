from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable
from processes.cotizaciones import Cotizaciones

if __name__ == '__main__':
    '''ct = IngresoDeCotizaciones('SV')
    result = ct.cotizaciones_diarias(1)
    save_json(result, 'Cotizaciones_Diarias')
    result1 = ct.cotizaciones_actualizadas()
    save_json(result1, 'Cotizaciones_Actualizadas')'''
    valor = Cotizaciones('GT').datos_cliente('C1041')
    print(valor)

