from mail.mail import Mail
from mail.JinjaTemplateManager import TemplateRenderer


if __name__ == '__main__':

    productos = {
        1: {'nombre': 'Manzana', 'precio': 0.50, 'descripción': 'Roja y jugosa'},
        2: {'nombre': 'Banana', 'precio': 0.30, 'descripción': 'Madura y dulce'},
        3: {'nombre': 'Cereza', 'precio': 2.00, 'descripción': 'Fresca y deliciosa'}
    }
    renderer = TemplateRenderer()
    renderer.prueba()
    #html = renderer.render(None, nombre_vendedor="Nombre Vendedor", productos=productos)
    #print(html)
    #mail = Mail('SMTP_SERVER',  'SMTP_USERNAME', 'SMTP_PASSWORD')
    #mail.enviar_correo('kelvin.miranda@grupopelsa.com', 'test', '<p>Contenido del mensaje en HTML</p>')
