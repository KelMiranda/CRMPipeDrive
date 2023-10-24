import time

from pipedrive.pipedrive_api_conecction import PipedriveAPI
from datetime import datetime
import json
import os


class DealTable:
    def __init__(self, table):
        self.table = table
        pass

    def create_folder_structure(self):
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

    def save_json(self, data, variable):
        year_folder, month_folder, day_folder = self.create_folder_structure()

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

    def make_all_deals(self):
        data = {
            "company_domain": "grupopelsa",
            "start": 0,
            "limit": 100,
        }
        result = PipedriveAPI('TOKEN_CRM').get_records('deals', data)
        deals = {}
        for row in result:
            deals[f"{row.get('id')}"] = {
                'stage_id': row.get('stage_id'),
                'title': row.get('title'),
                'value': row.get('value'),
                'add_time': row.get('add_time'),
                'update_time': row.get('update_time'),
                'stage_change_time': row.get('stage_change_time'),
                'status': row.get('status'),
                'probability': row.get('probability'),
                'lost_reason': row.get('lost_reason'),
                'close_time': row.get('close_time'),
                'pipeline_id': row.get('pipeline_id'),
                'won_time': row.get('won_time'),
                'org_name': row.get('org_name'),
                'CardCode': row.get('060d979042413ee06230b755710f42901b6b0a92')
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

        self.save_json(deals, 'deals')

