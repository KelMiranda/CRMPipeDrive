from database.sql_server_connection import SQLServerDatabase
from processes.cotizaciones import Cotizaciones
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import dictionary_invert


def comparar_registros_cliente(registro1, registro2):
    # Normalizar nombres de campos
    campos = [
        ('CardCode', 'CardCode'),
        ('CardName', 'CardName'),
        ('Address', 'Address'),
        ('Phone1', 'Phone1'),
        ('Municipio', 'Municipio'),
        ('Departamento', 'Departamento'),
        ('E_Mail', 'E_Mail'),
        ('id_PipeDrive', 'id_PipeDrive'),
        ('fecha_registro', 'CreateDate'),
        ('Fecha_Modificacion', 'UpdateDate'),
        ('Sector', 'Sector'),
        ('Validador', 'Validador'),
        ('Coordenadas', 'Coordenadas'),
        ('Pais', 'Pais'),
        ('Vendedor_Asignado', 'SlpName'),
    ]
    
    diferencias = []
    for campo1, campo2 in campos:
        valor1 = registro1.get(campo1)
        valor2 = registro2.get(campo2)
        if str(valor1) != str(valor2):
            diferencias.append(f"Diferencia en {campo1}/{campo2}: '{valor1}' vs '{valor2}'")
    
    return diferencias


class Cliente:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.ct = Cotizaciones(self.pais)
        self.pipe = PipedriveAPI('Token')

    def validadorCliente(self, CardCode):
        query = f"[dbo].[SP_VALIDADOR_DE_CLIENTE] '{CardCode}', '{self.pais}'"
        errores = []
        result = {}

        try:
            self.db.connect()
            consulta = self.db.execute_query(query)[0]

            if consulta[0] is None and consulta[1] is not None:
                result.update({
                    'CardCode': CardCode,
                    'id_Pipedrive': consulta[0],
                    'Validador': consulta[1],
                    'action': 1,
                    'comentario': 'El cliente no existe en pipedrive.'
                })
            elif consulta[0] is None and consulta[1] is None:
                result.update({
                    'CardCode': CardCode,
                    'action': 2,
                    'comentario': 'El cliente no esta en la tabla y tampoco en pipedrive.'
                })
            else:
                result.update({
                    'CardCode': CardCode,
                    'action': 3,
                    'comentario': 'El cliente Existe en pipedrive y tambien en la tabla.'
                })

        except Exception as e:
            error_message = f"Error al ejecutar la consulta. El error es: {str(e)}"
            errores.append(error_message)
        finally:
            if self.db:  # Verifica si db está definido y conectado
                self.db.disconnect()

        return result, errores

    def ingresar_o_actualizar_cliente_pipedrive(self, codigo_cliente):
        resultado = self.ct.datos_cliente(codigo_cliente)
        datos_POS = resultado.get('datos_POS')
        cuenta_asignada = (f"Select b.PipedriveId from [PipeDrive].[dbo].[vendedores] AS A INNER JOIN [PipeDrive]."
                           f"[dbo].[users] AS B ON (A.id_vendedores = B.id_vendedores) "
                           f"Where a.SlpName = '{datos_POS.get('Vendedor_Asignado')}'")
        self.db.connect()
        cuenta_asignada = self.db.execute_query(cuenta_asignada)[0]
        lista = resultado.get('lista')
        datos = {
            'name': datos_POS.get('CardName'),
            'bd4aa325c2375edc367c1d510faf509422f71a5b': datos_POS.get('CardCode'),
            '8b8121d03ef920b724ffa68b0f6177fdf281ad3f': lista.get('4023').get(f"{datos_POS.get('Sector')}"),
            '99daf5439284d6a809aee36c4d52a53c9826300b': lista.get('4025').get(f"{datos_POS.get('Municipio')}"),
            'deca3dd694894b2ca93df56db39f66468cb3885d': lista.get('4024').get(f"{datos_POS.get('Departamento')}"),
            '3ed19788ef9c8ebeaf0f24f58394f67ac784684c': datos_POS.get('Coordenadas'),
            'fd0f15b9338615a55ca56a3cada567919ec33306': lista.get('4028').get(f"{datos_POS.get('Vendedor_Asignado')}"),
            'label': 1,
            'owner_id': cuenta_asignada[0],
            'followers': 13046551
        }

        if resultado.get('datos_pipe') == 'No existe en pipedrive':
            print(self.pipe.post_organization(datos))
        else:
            if resultado.get('Diferencia de datos entre POS y pipeDrive') is True:
                print('El usuario existe en pipedrive, pero tiene datos diferentes a la base de datos')
            else:
                print('No tiene ningun cambio este cliente')






