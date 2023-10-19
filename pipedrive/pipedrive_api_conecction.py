import requests
from urllib.parse import urljoin


class PipedriveAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.pipedrive.com/v1"

    def make_request(self, endpoint):
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params={"api_token": self.api_token}
            )
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return []

    def get_deals(self, id_deal):
        return self.make_request(f"deals/{id_deal}")

    def get_stages(self, id_stages):
        return self.make_request(f"stages/{id_stages}")

    def get_pipeline(self, id_pipeline):
        return self.make_request(f"pipelines/{id_pipeline}")