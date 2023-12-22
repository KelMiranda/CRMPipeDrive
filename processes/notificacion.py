from xhtml2pdf import pisa

def convert_html_to_pdf(source_html, output_filename):
    # Abrir una conexión de archivo binario para escribir el PDF.
        with open(output_filename, "w+b") as result_file:
            # Convertir HTML a PDF
            pisa_status = pisa.CreatePDF(
                source_html,                # Contenido HTML a convertir
                dest=result_file)           # Archivo a escribir PDF

            # Retornar True en caso de éxito y False en caso contrario
        return pisa_status.err

class Notificaciones():
    def __init__(self, ):
        pass