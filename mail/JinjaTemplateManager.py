from jinja2 import Environment, FileSystemLoader, TemplateNotFound

class JinjaTemplateManager:
    def __init__(self, template_dir='./templates', default_template='base_correo.html'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.default_template = default_template

    def render_template(self, template_name=None, **kwargs):
        # Usa la plantilla por defecto si no se proporciona una
        template_name = template_name or self.default_template
        try:
            # Carga la plantilla
            template = self.env.get_template(template_name)
            # Renderiza la plantilla con los datos proporcionados
            return template.render(**kwargs)
        except TemplateNotFound:
            # Retorna un mensaje de error si la plantilla no se encuentra
            return f"Error: La plantilla '{template_name}' no se encuentra en el directorio."