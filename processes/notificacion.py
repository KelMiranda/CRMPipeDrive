from xhtml2pdf import pisa
from processes.cotizaciones import Cotizaciones
from mail.JinjaTemplateManager import JinjaTemplateManager
from mail.mail import Mail
from datetime import datetime
from processes.usuarios import Usuarios


def convert_html_to_pdf(source_html, output_filename):
    # Abrir una conexión de archivo binario para escribir el PDF.
    with open(output_filename, "w+b") as result_file:
        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(
            source_html,  # Contenido HTML a convertir
            dest=result_file)  # Archivo a escribir PDF

        # Retornar True en caso de éxito y False en caso contrario
    return pisa_status.err


class Notificaciones:
    def __init__(self, pais):
        self.pais = pais
        self.mail = Mail('SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD')
        self.cnt = JinjaTemplateManager()

    def cotizaciones_abiertas(self, SlpName, correo_vendedor):
        global result, fecha_actual
        errores = []
        try:
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            datos = {}
            cont = 0
            ct = Cotizaciones(f'{self.pais}')
            for row in ct.obtener_cotizaciones_abiertas(f'{SlpName}')[0]:
                cont = cont + 1
                datos[cont] = {
                    'cliente': row[2],
                    '#cotizaciones': row[3],
                    '#documentos': ct.obtener_docnum_cotizacion(f'{row[1]}')[0]
                }
            total_cotizaciones = sum(client['#cotizaciones'] for client in datos.values())
            contenido = self.cnt
            mail = self.mail
            html = contenido.render_template(template_name='cotizaciones_Abiertas.html', nombre_vendedor=f'{SlpName}',
                                             total_cotizaciones=total_cotizaciones, fecha_actual=fecha_actual,
                                             datos=datos)
            # convert_html_to_pdf(html, output_filename)

            result = mail.enviar_correo(f'{correo_vendedor}', 'Notificacion Cotizaciones', html)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            print(f'Se envio el correo a: {SlpName} con exito, el dia {fecha_actual}')
        return result, errores

    def notificacion_ultima_conexion(self, correo):
        global fecha_actual
        errores = []
        datos = {}
        result = []
        cont = 0
        nombre = correo.split('@')[0]
        try:
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            results = Usuarios().get_days4user()
            for row in results:
                valores = results.get(row)
                cont = cont + 1
                datos[cont] = {
                    'usuario': valores.get('usuario'),
                    '#dias': valores.get('#dias'),
                    'fecha': valores.get('fecha')
                }
            contenido = self.cnt
            mail = self.mail
            html = contenido.render_template(template_name='Notificacion_Usuarios.html', nombre=nombre, fecha_actual=fecha_actual, datos=datos)
            result = mail.enviar_correo(f'{correo}', ' Informe de Usuarios CRM - El Salvador', html)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            print(f'Se envio el correo a: Gerente Comercial con exito, el dia {fecha_actual}')
        return result, errores
