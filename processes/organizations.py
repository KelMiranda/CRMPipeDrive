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
        self.pipe = PipedriveAPI('TOKEN_CRM')

    def get_customers_from_a_table(self):
        query = f"Select top 2 * from {self.table} Where Pais = '{self.country}' AND Vendedor_Asignado != 'SIN CARTERA ASIGNADA' AND id_PipeDrive > 0 order by id_PipeDrive"
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
        pipe = self.pipe
        data = {}
        for row in result:
            time.sleep(1)
            result2 = GetIdUser(f'{row[15]}').get_user_id_and_sector()

            id_empresa = result2.get('id_user_pipedrive')

            if id_empresa is None:
                data = {
                    "owner_id": 12806795,
                    "fd0f15b9338615a55ca56a3cada567919ec33306": 715
                }
            else:
                data = {
                    "owner_id": id_empresa,
                    "fd0f15b9338615a55ca56a3cada567919ec33306": pipe.get_organization_field_id('4028').get(f'{row[15]}')
                }
            request = pipe.put_organization_id(row[8], data)

            if request.get('success'):
                print(f'El Cliente {row[2]}, con un id: {row[8]} fue modificado')
            else:
                print(f'presento un problema el id: {row[8]}, el problema es: {request}')


