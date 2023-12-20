from processes.cotizaciones import Cotizaciones
from mail.JinjaTemplateManager import JinjaTemplateManager
from datetime import datetime
from mail.mail import Mail

if __name__ == '__main__':
    datos = {}
    pais = ['SV', 'GT']
    cont = 0
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    for row in pais:
        proceso = Cotizaciones(f'{row}').validar_cotizacion()
        cont = cont + 1
        datos[cont] = {'#documentos': proceso[0],
                    '#errores': proceso[1]
                    }
    
    contenido = JinjaTemplateManager()
    mail = Mail('SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD')
    html = contenido.render_template(template_name='notificacion.html', nombre_vendedor = 'Kelvin Miranda', fecha_actual=fecha_actual, datos=datos)
    mail.enviar_correo('kelvin.miranda@grupopelsa.com', 'Automatizacíon Cierre de cotización', html)
        

    
        
