from pipedrive.pipedrive_api_conecction import PipedriveAPI
from datetime import datetime


class Usuarios:
    def __init__(self):
        self.pipe = PipedriveAPI('Token')

    def get_last_connection(self):
        resultado = self.pipe.get_all_user()['data']
        grupos = {
            "contra": [13042899, 13582075, 13582086, 13582097],
            "igo": [13045165, 13581921, 13581932, 13581943],
            "retail": [13091607, 13738649, 13738660, 13738638, 13738671],
            "mayo": [14592007, 14592018, 13060961]
        }

        # Crear un diccionario para almacenar los resultados
        resultados = {grupo: [] for grupo in grupos}

        for user in resultado:
            for grupo, ids in grupos.items():
                if user['id'] in ids:
                    resultados[grupo].append([user['name'], user['last_login']])
                    break

        return resultados

    def get_days4user(self, ):
        fecha_actual = datetime.now()
        vendedores = self.get_last_connection()
        count = 0
        datos = {}
        for vender in vendedores:
            for user in vendedores.get(f'{vender}'):
                count = count + 1
                fecha_usuario = user[1]
                fecha_dada_objeto = datetime.strptime(fecha_usuario, '%Y-%m-%d %H:%M:%S')
                diferencia = fecha_actual - fecha_dada_objeto
                dias = diferencia.days
                datos[count] = {
                    'usuario': user[0],
                    '#dias': dias,
                    'fecha': fecha_usuario
                }
        return datos