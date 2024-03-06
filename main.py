from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable

if __name__ == '__main__':
    '''ct = IngresoDeCotizaciones('SV')
    #result = ct.cotizaciones_diarias()
    #save_json(result, 'Cotizaciones_Diarias')
    result = ct.cotizaciones_actualizadas()
    save_json(result, 'Cotizaciones_Actualizadas')'''

    deal = DealTable('DatosProyectos_PipeDrive', 'SV')
    print(deal.nombres_vendedor_cotizado())
    print(deal.nombres_vendedor_asignado())