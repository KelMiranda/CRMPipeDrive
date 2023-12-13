from jinja2 import Environment, FileSystemLoader

class TemplateRenderer:
    def __init__(self, template_dir='./templates', default_template='base.html'):
        # Inicializa el entorno de Jinja2 con el directorio de plantillas
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.default_template = default_template

    def load_template(self, template_name=None):
        # Carga una plantilla específica, o la predeterminada si no se proporciona una
        template_name = template_name or self.default_template
        return self.env.get_template(template_name)

    def render(self, template_name=None, **kwargs):
        # Carga y renderiza la plantilla con los datos proporcionados
        template = self.load_template(template_name)
        return template.render(**kwargs)