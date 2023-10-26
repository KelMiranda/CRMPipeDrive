import requests
import os
from urllib.parse import urljoin


class PipedriveAPI:
    def __init__(self, api_token):
        self.api_token = os.getenv(api_token)
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
                return None
        except requests.exceptions.RequestException as e:
            # print(f"Request Error: {e}")
            return None

    def get_deals(self, id_deal):
        return self.make_request(f"deals/{id_deal}")

    def get_stages(self, id_stages):
        return self.make_request(f"stages/{id_stages}")

    def get_pipeline(self, id_pipeline):
        return self.make_request(f"pipelines/{id_pipeline}")

    def get_all_pipelines(self):
        return self.make_request("pipelines")

    def get_all_stages(self):

        return self.make_request(f"stages")

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
        vendedores = {}
        response = self.make_request(f"dealFields/{id_deal_field}")
        if response:
            vendedores = {row['label']: row['id'] for row in response['data']['options']}
        else:
            print("No tiene opciones")
        return vendedores
