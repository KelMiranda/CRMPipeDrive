import time
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from database.sql_server_connection import SQLServerDatabase
from processes.deals import get_all_option_for_fields_in_deals
from processes.deals import dictionary_invert
from pipedrive.users_pipedrive import GetIdUser


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
        query = f"Select * from {self.table} Where Pais = '{self.country}' AND Vendedor_Asignado != 'SIN CARTERA ASIGNADA'"
        print(query)
        self.db.connect()
        result = self.db.execute_query(query)
        self.db.disconnect()
        return result

    def get_all_values_of_assigned_salesperson(self):
        query = f"Select distinct Vendedor_Asignado from {self.table} Where Pais = '{self.country}' AND Vendedor_Asignado != 'SIN CARTERA ASIGNADA'"
        self.db.connect()
        not_salesperson_in_crm = {}
        all_salesperson = self.db.execute_query(query)
        values = get_all_option_for_fields_in_deals([12521])
        for row in all_salesperson:
            validator = values.get('12521').get(row[0])
            if validator is None:
                not_salesperson_in_crm[f'{row[0]}'] = 'No existe en el crm'
        self.db.disconnect()
        return not_salesperson_in_crm

    def assign_owner_in_the_crm(self):
        result = self.get_customers_from_a_table()
        for row in result:
            print(row[15])
            time.sleep(1)
            print(GetIdUser(f'{row[15]}').get_user_id_and_sector())


