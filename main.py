import os
import database.sql_server_connection as db
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.cleaning_of_deal import DealsTable
import time


def server_crm():
    data_server = {'server': os.getenv('SERVER'),
                   'database': os.getenv('DATABASE'),
                   'username': os.getenv('USERNAME_'),
                   'password': os.getenv('PASSWORD')}
    valores = [valor for valor in data_server.values()]
    valor_separados = ', '.join(valores)
    return valores


if __name__ == '__main__':
    ps = DealsTable('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD', 'SV')
    pipe = PipedriveAPI('TOKEN_CRM')

    object_type = 'deals'
    params = {
        "company_domain": "grupopelsa",
        "start": 0,
        "limit": 100,
    }
    result = pipe.get_records(object_type, params)
    for row in result:
        time.sleep(0.5)
        print(row)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
