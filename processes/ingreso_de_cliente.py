
from database.sql_server_connection import SQLServerDatabase


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

    def validadorCliente(self, CardCode):
        query = f"[dbo].[SP_VALIDADOR_DE_CLIENTE_SV]'{CardCode}', '{self.pais}'"
        errores =[]
        result = []
        try:
            self.db.connect()
            consulta = self.db.execute_query(query)[0]
            if consulta[0] == 0:
                result.append({
                    'CardCode': CardCode,
                    'id_Pipedrive': consulta[0],
                    'Validador': consulta[1],
                    'action': 1,
                    'comentario': 'El cliente no esta en PipeDrive'
                })
            elif consulta[0] is None:
                result.append({
                    'CardCode': CardCode,
                    'action': 2,
                    'comentario': 'El cliente no esta en PipeDrive y tampoco en la tabla'
                })
            else:
                result.append({
                    'CardCode': CardCode,
                    'action': 3,
                    'comentario': 'El Cliente existe en PipeDrive y en la tabla'
                })

        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def ingresar_cliente(self, action):
        errores = []
        result = []
        try:
            self.db.connect()
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores




