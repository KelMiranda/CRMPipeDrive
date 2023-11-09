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
    def __int__(self, table):
        self.table = table
        self.database = SQLServerDatabase('SERVER', 'DATABASE','USERNAME_', 'PASSWORD')

    def client_validator(self):
        pais = 'sv'
        cardcode = 'C000000'
        result_pipedrive = get_all_organization()
        for row in result_pipedrive:
            time.sleep(1)
            print(row.get('bd4aa325c2375edc367c1d510faf509422f71a5b'))
        #query = f"Select * from {self.table} Where Pais = '{pais}' AND CardCode = '{cardcode}'"
        #self.database.execute_query(query)