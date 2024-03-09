import time
import json

from pipedrive.pipedrive_api_conecction import PipedriveAPI
from database.sql_server_connection import SQLServerDatabase
from datetime import datetime

def get_id_pipedrive():
    user_ids = {
        # User for IGO
        'IGO': {
            'SANDRA DOÑAN': [13581921, 'sandra.donan@grupopelsa.com', 'VEND86'],
            'ALVARO AVILES': [13581921, 'alvaro.aviles@grupopelsa.com', 'VEND100'],
            'CARLOS AVILES': [13581921, 'nilson.doradea@grupopelsa.com', '' ],
            'WILLIAM RAMIREZ': [13581932, 'william.ramirez@grupopelsa.com'],
            'ALEX ORELLANA': [13581932, 'alex.orellana@grupopelsa.com'],
            'JOSE ESTRADA': [13581943, 'vendedor.industria2@grupopelsa.com'], 
            'JOSE MENA.': [13581943, 'vendedor.industria1@grupopelsa.com'],
            'JOSE PEREZ': [13581943, 'grandesclientes.pelsa@grupopelsa.com'],
            'PABLO FLORES': [13045165, 'nilson.doradea@grupopelsa.com'],
            'GERENCIA AV': [13045165, 'nilson.doradea@grupopelsa.com'],
            'WILFREDO DIAZ': [13045165, 'nilson.doradea@grupopelsa.com']
        },

        # User for Contra
        'CONTRA': {
            'VICTOR ESCOBAR': [13582075, 'victor.escobar@grupopelsa.com'],
            'MARLON VIDES': [13582075, 'marlon.vides@grupopelsa.com'],
            'MARY LANDAVERDE': [13582086, 'maria.landaverde@grupopelsa.com'],
            'GERMAN CATIVO': [13582086, 'german.cativo@grupopelsa.com'],
            'MERCEDES CRUZ': [13582097, 'mercedes.cruz@grupopelsa.com'],
            'EDUARDO MARTINEZ': [13582097, 'eduardo.martinez@grupopelsa.com'],
            'ESTHER GUERRERO': [13582097, 'esther.guerrero@grupopelsa.com'],
            'GERENCIA FB': [13042899, 'esau.osegueda@grupopelsa.com']
        },

        # User for Retail-FB
        'RETAIL - FB': {
            'ERIKA ESTHEFANY JOVEL ARCE (FLOR BLANCA)': [13738660, 'ventas.salafb@grupopelsa.com'],
            'ROBERTO GONZALES CARTERA': [13738649, 'roberto.gonzalez@grupopelsa.com'],
            'ROBERTO GONZALEZ': [13738649, 'roberto.gonzalez@grupopelsa.com'],
            'CESAR NAVIDAD': [13738649, 'cesar.navidad@grupopelsa.com'],
            'CESAR NAVIDAD CARTERA': [13738649, 'cesar.navidad@grupopelsa.com'],
            'EDUARDO ACEVEDO': [13091607, 'eduardo.acevedo@grupopelsa.com'],
            'EDWIN BARAHONA': [13091607, 'edwin.barahona@grupopelsa.com'],
            'VILMA MEMBRENO': [13738660, 'ventas.salafb@grupopelsa.com'],
            'SIN CARTERA ASIGNADA': [13091607, 'carmen.rivera@grupopelsa.com']
        },

        # User for Retail - AV
        'RETAIL - AV': {
            'EMILY ORELLANA': [13738638, 'emily.orellana@grupopelsa.com'],
            'JOSSELYNE HERNANDEZ': [13738638, 'jhosselyn.corvera@grupopelsa.com'],
            'MARIA LUISA': [13091607, 'carmen.rivera@grupopelsa.com'],
            'MARTIN OSEGUEDA': [13738638, 'martinh.osegueda@grupopelsa.com'],
            'MARTIN OSEGUEDA CARTERA': [13738638, 'martinh.osegueda@grupopelsa.com'],
            'SAUL RIVAS': [13091607, 'carmen.rivera@grupopelsa.com'],
        },

        # User for Retail - SM
        'RETAIL- SM': {
            'MISAEL CHAVEZ': [13738671, 'misael.chavez@grupopelsa.com'],
            'NELSON GUEVARA': [13091607, 'julio.guevara@grupopelsa.com'],
            'RENE LOPEZ': [13738671, 'rene.lopez@grupopelsa.com'],
            'WILMAN ORELLANA': [13091607, '	julio.guevara@grupopelsa.com'],
        },

        # User for ING
        'ING': {
            'CARLOS HERNANDEZ': [13545610, ''],
            'HUGO CERRITOS': [13545610, ''],
            'WILLIAM MOLINA': [13814725, ''],
            'GONZALO CHAVARRI': [13814725, ''],
            'WILLAN MEJIA': [13814736, ''],
            'FATIMA FLORES': [13814747, ''],
            'JOSE PREZA': [13814747, ''],
            'JAMIL PALMA': [13814747, ''],
            'ALEX  CAMPOS': [14592007, ''],
        },

        # User for Mayo
        'MAYO': {
            'ASTRID MORAN': [14592007, 'astrid.moran@grupopelsa.com'],
            'LUIS PACHECO GUARDADO': [14592007, 'mayoreo4.es@grupopelsa.com'],
            'ALEX  CAMPOS': [14592007, 'mayoreo1.es@grupopelsa.com'],
            'MARVIN RAMIREZ': [14592018, 'marvin.ramirez@grupopelsa.com'],
            'DAVID ISAAC ORELLANA VASQUEZ': [14592018, ' mayoreo3.sm@grupopelsa.com'],
            'NICOLAS QUINTANILLA': [14592018, 'mayoreo2.sm@grupopelsa.com'],
            'ERNESTO CAMPOS': [13060961, 'jefatura.mayoreo@grupopelsa.com'],
            'GERENTE MAYOREO': [13060961, 'jefatura.mayoreo@grupopelsa.com'],
        },

        # User for Utili
        'UTIL': {
            'JOSE ORTEGA': [14065624, 'jose.ortega@grupopelsa.com']
        },

        # User for Admin
        'ADMIN': {
            'GRUPO PELSA': [12806795, 'kelvin.miranda@grupopelsa.com']
        },

        #User for Guatemala
        'GUATEMALA': {
            '4 - ROBERTO ROMERO': [13013045, ''],
            '33 - MYNOR GARCIA': [13004509, ''],
            'JULIO JOSUE CANO LOPEZ': [13013045, ''],
            'WALTER ENRIQUEZ': [13013045, ''],
            'AMANDA BOCHE': [13004509, ''],
            'GERENCIA': [12992629, ''],
            'RUBEN ESCOBAR': [12992629, '']
        }
    }
    return user_ids


def vendedor_sector(sector):
    vendedores = get_id_pipedrive()
    return vendedores.get(f'{sector}')


class GetIdUser:
    def __init__(self, name=None):
        self.name = name
        self.pipe = PipedriveAPI('Token')
        self.db = SQLServerDatabase('SERVER', 'DATABASE2', 'USERNAME_', 'PASSWORD')

    def get_user_id_and_sector(self):
        result = {}
        sector = {
            'CONTRA',
            'IGO',
            'ING',
            'MAYO',
            'RETAIL - AV',
            'RETAIL - FB',
            'RETAIL- SM',
            'UTIL',
            'ADMIN',
            'GUATEMALA'
        }
        for row in sector:
            all_sales_person = get_id_pipedrive().get(f'{row}')
            if self.name in all_sales_person:
                result = {
                    'sector': row,
                    'id_user_pipedrive': all_sales_person.get(f'{self.name}')[0],
                    'name': self.name,
                    'mail_pelsa': all_sales_person.get(f'{self.name}')[1],
                }
                break
            else:
                result = {
                    'id_user_pipedrive': 12806795
                }
        return result

    def get_all_user_pipedrive(self):
        usuarios = []
        error = []
        try:
            for user in self.pipe.get_all_user().get('data', []):
                usuarios.append({
                    'PipedriveId': user.get('id'),
                    'name': user.get('name'),
                    'email': user.get('email'),
                    'created': datetime.strptime(user.get('created'), "%Y-%m-%d %H:%M:%S").date(),
                    'last_login': datetime.strptime(user.get('last_login'), "%Y-%m-%d %H:%M:%S").date(),
                    'modified': datetime.strptime(user.get('modified'), "%Y-%m-%d %H:%M:%S").date()
                })
        except Exception as e:
            error.append({
                'mensaje': f"Ocurrió un error al obtener los usuarios: {e}"
            })

        return usuarios, error

    def validador_de_usuarios(self):
        usuarioIngresado = []
        usuarioModificado = []
        usuarioError = []
        try:
            valores = self.get_all_user_pipedrive()
            self.db.connect()
            for usuario in valores[0]:
                time.sleep(1)
                try:
                    query = f"SELECT COUNT(*) FROM users WHERE PipedriveId = {usuario.get('PipedriveId')}"
                    validador = self.db.execute_query(query)
                    if validador[0][0] == 0:
                        query2 = f"INSERT INTO users (PipedriveId, name, email, created, last_login, modified) VALUES ({usuario.get('PipedriveId')}, '{usuario.get('name')}', '{usuario.get('email')}', '{usuario.get('created')}', '{usuario.get('last_login')}', '{usuario.get('modified')}')"
                        # Suponiendo que execute_query ejecuta y confirma la inserción
                        self.db.execute_query(query2, False)
                        usuarioIngresado.append({
                            f'{usuario.get("name")}': "Fue Ingresado con exito"
                        })
                    else:
                        usuarioModificado.append({
                            f'{usuario.get("name")}': "Fue modificado con exito"
                        })
                except Exception as e_inner:
                    # Añade el usuario y el error específico al listado de errores
                    usuarioError.append({
                        "usuario": usuario.get('name'), "error": str(e_inner)
                    })
        except Exception as e:
            print(f"Ocurrió un error al procesar los usuarios: {e}")
        finally:
            if self.db.connection:
                self.db.disconnect()

        output = {
            'ingresados': usuarioIngresado,
            'modificados': usuarioModificado,
            'con error': usuarioError
        }
        return output  # Devuelve el resultado como un string en formato JSON



