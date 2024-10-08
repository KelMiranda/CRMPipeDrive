import time
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from pipedrive.users_pipedrive import GetIdUser
from database.sql_server_connection import SQLServerDatabase
from datetime import datetime
from processes.pipeline import PipelineTable
from processes.stages import  StageTable
import json
import os


def create_folder_structure():
    # Obtenemos la fecha actual
    now = datetime.now()

    # Creamos una carpeta principal para el año
    year_folder = now.strftime("%Y")
    os.makedirs(year_folder, exist_ok=True)

    # Creamos una carpeta para el mes dentro de la carpeta del año
    month_folder = now.strftime("%Y-%m")
    os.makedirs(os.path.join(year_folder, month_folder), exist_ok=True)

    # Creamos una carpeta para el día dentro de la carpeta del mes
    day_folder = now.strftime("%Y-%m-%d")
    os.makedirs(os.path.join(year_folder, month_folder, day_folder), exist_ok=True)

    return year_folder, month_folder, day_folder


def save_json(data, variable):
    year_folder, month_folder, day_folder = create_folder_structure()

    # Obtenemos la fecha actual para el nombre del archivo JSON
    now = datetime.now()
    file_name = now.strftime("%Y-%m-%d.json")
    test = '{}-{}'.format(variable, file_name)

    # Creamos la ruta completa del archivo JSON
    file_path = os.path.join(year_folder, month_folder, day_folder, test)

    # Guardamos los datos en el archivo JSON
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

    print(f"El archivo {format(test)} ha sido creado exitosamente.")


def dictionary_invert(my_dictionary, valor):
    if valor is None:
        clave_correspondiente = 'None'
        return clave_correspondiente
    else:
        valor = int(valor)
        dictionary_invert_v = {v: k for k, v in my_dictionary.items()}
        valor_buscado = valor
        # print(my_dictionary, dictionary_invert_v)

        if valor_buscado in dictionary_invert_v:
            clave_correspondiente = dictionary_invert_v[valor_buscado]
            return clave_correspondiente
        else:
            clave_correspondiente = 'None'
            return clave_correspondiente


def get_all_option_for_fields_in_deals(id_field_deal):
    my_dictionary = {}
    for row in id_field_deal:
        my_dictionary[f"{row}"] = PipedriveAPI('Token').get_deal_field_id(row)
    return my_dictionary


def get_all_deals():
    id_fields_deals = [12527, 12546, 12521, 12523]
    values = get_all_option_for_fields_in_deals(id_fields_deals)
    valores_embudos = PipelineTable().obteniendo_todos_los_embudos()
    valores_estados = StageTable().obteniendo_todos_los_estados()

    def obteniendo_embudo(id_number):
        for item in valores_embudos:
            if item['id'] == int(id_number):
                return item['name']

    def obteniendo_estado(id_number):
        for item in valores_estados:
            if item['id'] == int(id_number):
                return item['name']

    data = {
        "company_domain": "grupopelsa",
        "start": 0,
        "limit": 100,
    }
    result = PipedriveAPI('Token').get_records('deals', data)
    deals = {}

    for row in result:
        deals[f"{row.get('id')}"] = {
            'stage_id': obteniendo_estado(row.get('stage_id')),
            'title': row.get('title'),
            'value': row.get('value'),
            'add_time': row.get('add_time'),
            'update_time': row.get('update_time'),
            'stage_change_time': row.get('stage_change_time'),
            'status': row.get('status'),
            'probability': row.get('probability'),
            'lost_reason': row.get('lost_reason'),
            'close_time': row.get('close_time'),
            'pipeline_id': obteniendo_embudo(row.get('pipeline_id')),
            'won_time': row.get('won_time'),
            'org_name': row.get('org_name'),
            'CardCode': row.get('060d979042413ee06230b755710f42901b6b0a92'),
            'DocStatus': dictionary_invert(values.get('12527'), row.get('6fe64586c7f0e32e9caabde4b5c1d7a2ea697748')),
            'ProjectType': dictionary_invert(values.get('12546'), row.get('6840b183ea0a8dd8a55b4f7cd773a4d1f73e442a')),
            'SlpName': dictionary_invert(values.get('12521'), row.get('bdc9870365278bf245effd816618a8a9bff8fad9')),
            'U_Jefe': dictionary_invert(values.get('12523'), row.get('057ae06bd90a1bcecb68ebceb30b99fb8be94801'))
        }
        if row.get('6aba016cdd852ee60aa6ae2ced2af84b9105d78c') == '187':
            pais = {
                'pais': 'SV'
            }
            deals[f"{row.get('id')}"].update(pais)
        elif row.get('6aba016cdd852ee60aa6ae2ced2af84b9105d78c') == '189':
            pais = {
                'pais': 'GT'
            }
            deals[f"{row.get('id')}"].update(pais)

    save_json(deals, 'deals')
    return deals


class DealTable:
    def __init__(self, table, country):
        self.table = table
        self.country = country
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.pipe = PipedriveAPI('Token')

    def get_all_the_deals_in_table(self):
        query = f"Select * from {self.table} Where Pais = '{self.country}'"
        '''query = f"Select * from {self.table} Where Pais = '{self.country}' AND  SlpName != 'SIN CARTERA ASIGNADA' AND id_deal is not null AND id_deal >= 3326 Order By id_deal"'''
        self.db.connect()
        result = self.db.execute_query(query)
        self.db.disconnect()
        return result

    def distinct(self):
        array = {}
        problem = {}
        result = self.get_all_the_deals_in_table()
        a = len(result)
        cont = 0
        for row in result:
            cont = cont + 1
            total = a - cont
            query = f"Select top 1 * from [dbo].[VW_CRM_POS_{self.country}] Where DocNum = {row[1]} AND ORD = '{row[13]}' order by Serie desc"
            self.db.connect()
            result2 = self.db.execute_query(query)
            self.db.disconnect()
            print(f"Los valores que faltan son : {total}")
            if result2 is not None and len(result2) > 0 and len(result2[0]) > 1:
                if row[2] != result2[0][1]:
                    array[f"{row[0]}"] = 'Dato Diferente'
            else:
                problem[f"{row[0]}"] = 'Dato erroneo en vista'

        save_json(array, f'Arreglo_Diferentes_{self.country}')
        save_json(problem, f'Registros_Problemas_{self.country}')

        return array

    # get id_deal in the Json
    def order_by_doc_status(self):
        result = self.get_all_the_deals_in_table()
        open = {}
        closed = {}
        processed = {}
        for row in result:
            match row[4]:
                case 'O':
                    open[f'{row[15]}'] = row
                case 'C':
                    closed[f"{row[15]}"] = row
                case 'P':
                    processed[f"{row[15]}"] = row
        return [open, closed, processed]

    def update_deals(self):
        query = f"Select * from {self.table} Where DocStatus in ('C', 'P') AND status_crm is null AND Pais = '{self.country}'"
        result = self.db.execute_query(query)

    def remove_followers(self, id_deal):
        result = self.pipe.get_deals(id_deal)
        followers_result = self.pipe.get_followers_deals(id_deal)['data']
        value_customer = result['data']['bdc9870365278bf245effd816618a8a9bff8fad9']
        customer = self.pipe.get_deal_field_id(12521)
        customer_name = dictionary_invert(customer, value_customer)
        id_customer = str(GetIdUser(f'{customer_name}').get_user_id_and_sector()['id_user_pipedrive'])

        if result['data']['followers_count'] == 0:
            data = {
                "user_id": 14592018
            }
            print(self.pipe.post_followers_in_deals(id_deal, data)['success'])
        else:
            for row in followers_result:
                id_row = row.get('user_id')
                if str(id_row) == id_customer:
                    print(f'el dueño es: {id_row}')
                else:
                    print(f'el vendedor:{id_row}, deja de seguir este trato')
                    print(self.pipe.delete_followers_in_deals(id_deal, int(row.get('id'))).get('success'))

    def nombres_vendedor_cotizado(self):
        si_existe = []
        no_existe = []
        query = f"Select distinct UserName from {self.table} Where Pais = '{self.country}'"
        self.db.connect()
        valores = self.db.execute_query(query)
        opciones = get_all_option_for_fields_in_deals([12522]).get('12522')
        for valor in valores:
            if opciones.get(f'{valor[0]}'):
                si_existe.append({f'{valor[0]}': 'Existe'})
            else:
                no_existe.append({f'{valor[0]}': 'No Existe'})

        output = {'Si Existen': si_existe,
                  'No Existe': no_existe}
        return output

    def nombres_vendedor_asignado(self):
        si_existe = []
        no_existe = []
        query = f"Select distinct SlpName from {self.table} Where Pais = '{self.country}'"
        self.db.connect()
        valores = self.db.execute_query(query)
        opciones = get_all_option_for_fields_in_deals([12521]).get('12521')
        for valor in valores:
            if opciones.get(f'{valor[0]}'):
                si_existe.append({f'{valor[0]}': 'Existe'})
            else:
                no_existe.append({f'{valor[0]}': 'No Existe'})

        output = {'Si Existen': si_existe,
                  'No Existe': no_existe}
        return output