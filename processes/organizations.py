from pipedrive.pipedrive_api_conecction import PipedriveAPI
from database.sql_server_connection import SQLServerDatabase


def get_all_organization():
    data = {
        "company_domain": "grupopelsa",
        "start": 0,
        "limit": 100,
    }
    result = PipedriveAPI('TOKEN_CRM').get_records('organizations', data)
    return result


class OrganizationTable:
    def __int__(self, table, country):
        self.table = table
        self.country = country
        self.database = SQLServerDatabase('SERVER', 'DATABASE','USERNAME_', 'PASSWORD')
