from processes.cotizaciones import Cotizaciones

if __name__ == '__main__':
    db = Cotizaciones('SV')
    print(db.validar_cotizacion())
