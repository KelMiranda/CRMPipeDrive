import requests
import os
from urllib.parse import urljoin
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class PipedriveAPI:
    BASE_URL = "https://api.pipedrive.com/v1"

    def __init__(self, api_token):
        #self.api_token = os.getenv(api_token)
        self.api_token = config[f'{api_token}']['api_token']

    def get_request(self, endpoint, params=None):
        """
        Realiza una solicitud a la API de Pipedrive.

        Args:
        - endpoint (str): El endpoint de la API.
        - params (dict): Parámetros adicionales para la solicitud.

        Returns:
        - dict or None: Los datos de la respuesta JSON o None si hay un error.
        """
        try:
            params = {"api_token": self.api_token}
            response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            # Puedes imprimir o registrar el error para facilitar la depuración
            print(f"Request Error: {e}")
            return None

    def put_request(self, endpoint, data):
        """
        Actualiza datos en la API de Pipedrive utilizando el método PUT.

        Args:
        - endpoint (str): El endpoint de la API.
        - data (dict): Los datos a actualizar.

        Returns:
        - dict or None: Los datos de la respuesta JSON o None si hay un error.
        """
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            params = {"Content-Type": "application/json", "api_token": self.api_token}
            response = requests.put(url, json=data, params=params)
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            # Puedes imprimir o registrar el error para facilitar la depuración
            print(f"Request Error: {e}")
            return None

    def delete_request(self, endpoint):
        """
        Elimina datos en la API de Pipedrive utilizando el método DELETE.

        Args:
        - endpoint (str): El endpoint de la API.

        Returns:
        - dict or None: Los datos de la respuesta JSON o None si hay un error.
        """
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            params = {"Content-Type": "application/json", "api_token": self.api_token}
            response = requests.delete(url, params=params)
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            # Puedes imprimir o registrar el error para facilitar la depuración
            print(f"Request Error: {e}")
            return None

    def post_request(self, endpoint, data=None):
        """
        Realiza una solicitud POST a la API de Pipedrive.

        Args:
        - endpoint (str): El endpoint de la API.
        - data (dict): El cuerpo de la solicitud para la API.

        Returns:
        - dict or None: Los datos de la respuesta JSON o None si hay un error.
        """
        try:
            headers = {"Content-Type": "application/json"}
            params = {"api_token": self.api_token}
            response = requests.post(f"{self.BASE_URL}/{endpoint}", json=data, headers=headers, params=params)
            response.raise_for_status()

            # Verifica que el código de estado de la respuesta sea 201 (Creado)
            if response.status_code == 201:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            # Puedes imprimir o registrar el error para facilitar la depuración
            print(f"Request Error: {e}")
            return None

    def get_deals(self, id_deal):
        #print(self.api_token)
        return self.get_request(f"deals/{id_deal}")

    def get_stages(self, id_stages):
        return self.get_request(f"stages/{id_stages}")

    def get_pipeline(self, id_pipeline):
        return self.get_request(f"pipelines/{id_pipeline}")

    def get_all_pipelines(self):
        return self.get_request("pipelines")

    def get_all_stages(self):

        return self.get_request(f"stages")

    def get_records(self, object_type, params):
        company_domain = params["company_domain"]
        del params["company_domain"]

        data = {
            "api_token": self.api_token
        }

        params.update(data)

        print(params, company_domain, object_type)

        url = f"https://{company_domain}.pipedrive.com/api/v1/{object_type}"
        response = requests.get(url, params=params)
        result = response.json()

        records = []

        if "data" in result and result["data"]:
            records.extend(result["data"])

        if "additional_data" in result and "pagination" in result["additional_data"]:
            pagination = result["additional_data"]["pagination"]
            if pagination["more_items_in_collection"]:
                params["company_domain"] = company_domain
                params["start"] = pagination["next_start"]
                records.extend(self.get_records(object_type, params))

        return records

    def get_deal_field_id(self, id_deal_field):
        vendors = {}
        response = self.get_request(f"dealFields/{id_deal_field}")
        if response:
            vendors = {row['label']: row['id'] for row in response['data']['options']}
        else:
            print("this field don't have options")
        return vendors

    def put_organization_id(self, id_organization, data):
        return self.put_request(f'organizations/{id_organization}', data)

    def get_organization_id(self, id_organization):
        return self.get_request(f'organizations/{id_organization}')

    def get_organization_field_id(self, id_organization_field):
        vendors = {}
        response = self.get_request(f"organizationFields/{id_organization_field}")
        if response:
            vendors = {row['label']: row['id'] for row in response['data']['options']}
        else:
            print("this field don't have options")
        return vendors

    def delete_followers_in_organization(self, id_organization, id_user_pipedrive):
        return self.delete_request(f'organizations/{int(id_organization)}/followers/{int(id_user_pipedrive)}')

    def get_followers_deals(self, id_deals):
        return self.get_request(f'deals/{id_deals}/followers')

    def delete_followers_in_deals(self, id_deals, id_user_pipedrive):
        return self.delete_request(f'deals/{int(id_deals)}/followers/{int(id_user_pipedrive)}')

    def post_followers_in_deals(self, id_deals, data):
        return self.post_request(f'deals/{int(id_deals)}/followers', data)

    def get_all_user(self):
        return self.get_request('users')