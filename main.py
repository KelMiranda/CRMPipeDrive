from mail.mail import Mail
<<<<<<< HEAD
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
=======
from mail.JinjaTemplateManager import JinjaTemplateManager

if __name__ == '__main__':
  
  



  mail = Mail('SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD')
  template_manager = JinjaTemplateManager()
  productos = {
    1: {'nombre': 'Manzana', 'precio': 0.50, 'descripción': 'Roja y jugosa'},
    2: {'nombre': 'Banana', 'precio': 0.30, 'descripción': 'Madura y dulce'},
    3: {'nombre': 'Cereza', 'precio': 2.00, 'descripción': 'Fresca y deliciosa'}
    }
  html = template_manager.render_template(template_name='base_correo.html', nombre_vendedor="Nombre Vendedor", productos=productos)
  mail.enviar_correo('kelvin.miranda@grupopelsa.com', 'test', html)
>>>>>>> 3e21ce72f4dff0fec2fe93ac1e28c3f9c4502f58
