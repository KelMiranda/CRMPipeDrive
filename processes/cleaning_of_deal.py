import os
import database.sql_server_connection as db
from pipedrive.pipedrive_api_conecction import PipedriveAPI


class DealsTable:
    def __init__(self, server, database, username, password, country):
        self.server = os.getenv(server)
        self.database = os.getenv(database)
        self.username = os.getenv(username)
        self.password = os.getenv(password)
        self.country = country

    def make_all_deals(self):
        connection = db.SQLServerDatabase(self.server, self.database, self.username, self.password)
        query = (f'''Select id_deal from DatosProyectos_PipeDrive Where Pais = '{self.country}' AND id_deal is not null 
                    order by id_deal''')
        connection.connect()
        return connection.execute_query(query)

    '''def match_with_pipedrive(self):
        request = self.make_all_deals()
        deals_not_in_pipedrive = []
        counter = 0
        total = len(request)
        for row in request:
            rest = total - counter
            print(f"Restan un total de: {rest}")
            counter = counter + 1
            pipe = PipedriveAPI(os.getenv('TOKEN_CRM'))
            if pipe.get_deals(row[0]) is None:
                deals_not_in_pipedrive.append(row[0])
        print(f"Los tratos que no se encuentran son: {deals_not_in_pipedrive}")'''




