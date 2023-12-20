from processes.cotizaciones import Cotizaciones

if __name__ == '__main__':
    db = Cotizaciones('SV')
    db.validando_cotizacion()
