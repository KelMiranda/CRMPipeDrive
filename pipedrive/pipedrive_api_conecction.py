import requests
from urllib.parse import urljoin


class PipedriveAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.pipedrive.com/v1/"

    def get_deals(self, deal_id):
        print(self.api_token)
        url = urljoin(self.base_url, f"deals/{deal_id}")
        print(url)
        params = {"api_token": self.api_token}
        response = requests.get(url, params=params)

        if response.ok:
            return response.json()
        else:
            return None