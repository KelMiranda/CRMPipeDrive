import os
from database.sql_server_connection import SQLServerDatabase
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from datetime import datetime
import time


class PipelineTable:
    def __init__(self, table):
        self.table = table

    def validator(self):
        pipe = PipedriveAPI('TOKEN_CRM')
        result = pipe.get_all_pipelines().get('data')
        db = SQLServerDatabase('SERVER', 'DATABASE2', 'USERNAME_', 'PASSWORD')
        db.connect()
        for row in result:
            time.sleep(1)
            query = f"Select * from {self.table} where id_pipeline = {row.get('id')}"
            if not db.execute_query(query, True):
                add_time = row.get('add_time')
                add_time_obj = datetime.strptime(add_time, "%Y-%m-%d %H:%M:%S")
                update_time = row.get('update_time')
                update_time_obj = datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
                time.sleep(2)
                query = f"INSERT into {self.table} (id_pipeline, name, url_title, active, deal_probability, add_time, update_time, selected) Values ({row.get('id')}, '{row.get('name')}','{row.get('url_title')}','{row.get('active')}','{row.get('deal_probability')}','{add_time_obj.date()}','{update_time_obj.date()}','{row.get('selected')}')"
                print(query)
                print(db.execute_query(query, False))

        print(
            '''#######################################################################################################''')
        db.disconnect()
