import requests
from urllib.parse import urljoin


class PipedriveAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.pipedrive.com/v1"

    def get_deals(self, id_deal):
        try:
            response = requests.get(
                f"{self.base_url}/deals/{id_deal}",
                params={"api_token": self.api_token}
            )
            #print(response.raise_for_status())

            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return []

    def get_stages(self, id_stages):

        try:
            response = requests.get(
                f"{self.base_url}/stages/{id_stages}",
                params={"api_token": self.api_token}
            )
            #print(response.raise_for_status())

            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return []

    def get_pipeline(self, id_pipeline):

        try:
            response = requests.get(
                f"{self.base_url}/pipelines/{id_pipeline}",
                params={"api_token": self.api_token}
            )
            #print(response.raise_for_status())

            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return []