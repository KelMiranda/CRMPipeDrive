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
        pass