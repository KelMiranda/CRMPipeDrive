import os
from database.sql_server_connection import SQLServerDatabase
from pipedrive.pipedrive_api_conecction import PipedriveAPI
import time


class PipelineTable:
    def __int__(self, database_pipedrive):
        self.database_pipedrive = database_pipedrive

    def validator(self):
        pipe = PipedriveAPI('TOKEN_CRM')
        result = pipe.get_all_pipelines().get('data')
        for row in result:
            time.sleep(1)
            print(row.get('id'))
            query = f"Select * from pipeline where id_pipeline = {row.get('id')}"
            db = SQLServerDatabase('SERVER', 'DATABASE2', 'USERNAME_', 'PASSWORD')
            db.connect()
            if not db.execute_query(query):
                query = f"INSERT into pipeline (id_pipeline, name, url_title, active, deal_probability, add_time, update_time, selected) Values ({row.get('id')}, {row.get('name')},{row.get('url_title')},{row.get('active')},{row.get('deal_probability')}, {row.get('add_time')},{row.get('update_time')},{row.get('selected')})"
                #db.insert_query(query)
            db.close_connection()
