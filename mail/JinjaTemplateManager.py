
from jinja2 import Environment, FileSystemLoader


if __name__=='__main__':
    # Carga el entorno y la plantilla
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('base_correo.html')

    # Producto en un diccionario.
    productos = {
    1: {'nombre': 'Manzana', 'precio': 0.50, 'descripción': 'Roja y jugosa'},
    2: {'nombre': 'Banana', 'precio': 0.30, 'descripción': 'Madura y dulce'},
    3: {'nombre': 'Cereza', 'precio': 2.00, 'descripción': 'Fresca y deliciosa'}
}

    # Renderiza la plantilla con datos
    html = template.render(nombre_vendedor="Nombre Vendedor", productos=productos)

    print(html)