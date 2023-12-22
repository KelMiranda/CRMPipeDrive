from processes.cotizaciones import Cotizaciones
from mail.JinjaTemplateManager import JinjaTemplateManager
from datetime import datetime
from mail.mail import Mail
from processes.notificacion import convert_html_to_pdf
import io
from processes.deals import create_folder_structure

if __name__ == '__main__':

    year, month, day = create_folder_structure()
    print(f"Carpetas creadas: {year}, {month}, {day}")

    """output_filename = "documento.pdf"
    fecha_actual = datetime.now().strftime("%d/%m/%Y")    
    datos = {}
    cont = 0
    ct = Cotizaciones('SV')
    for row in ct.obtener_cotizaciones_abiertas('GERMAN CATIVO')[0]:
        cont = cont +1 
        datos[cont] = {
            'cliente': row[2],
            '#cotizaciones': row[3],
            '#documentos': ct.obtener_docnum_cotizacion(f'{row[1]}')[0]
        }
    contenido = JinjaTemplateManager()
    mail = Mail('SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD')
    html = contenido.render_template(template_name='cotizaciones_Abiertas.html', nombre_vendedor = 'GERMAN CATIVO', fecha_actual=fecha_actual, datos=datos)
    convert_html_to_pdf(html, output_filename)

    #mail.enviar_correo('kelvin.miranda@grupopelsa.com', 'Notificacion Cotizaciones', html)
    
    #print(Cotizaciones('SV').obtener_docnum_cotizacion('C2620611')[0])"""
        

    
        
