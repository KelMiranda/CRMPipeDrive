import os
import database.sql_server_connection as db
from pipedrive.pipedrive_api_conecction import PipedriveAPI


def server_crm():
    data_server = {'server': os.getenv('SERVER'),
                   'database': os.getenv('DATABASE'),
                   'username': os.getenv('USERNAME_'),
                   'password': os.getenv('PASSWORD')}
    valores = [valor for valor in data_server.values()]
    valor_separados = ', '.join(valores)
    return valores


if __name__ == '__main__':
    token = os.getenv('TOKEN_CRM')
    pipe = PipedriveAPI(token)
    print(pipe.get_deals(6311))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
