import time
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from database.sql_server_connection import SQLServerDatabase
from processes.deals import get_all_option_for_fields_in_deals


def get_all_organization():
    data = {
        "company_domain": "grupopelsa",
        "start": 0,
        "limit": 100,
    }
    result = PipedriveAPI('TOKEN_CRM').get_records('organizations', data)
    return result


class OrganizationTable:
    def __init__(self, table, country):
        self.table = table
        self.country = country
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')

    def get_customers_from_a_table(self):
        query = f"Select * from {self.table} Where Validador = 'I' AND Pais = '{self.country}' AND Vendedor_Asignado != 'SIN CARTERA ASIGNADA'"
        print(query)
        self.db.connect()
        result = self.db.execute_query(query)
        self.db.disconnect
