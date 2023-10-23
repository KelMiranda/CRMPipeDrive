from database.sql_server_connection import SQLServerDatabase
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from datetime import datetime
import time


class StageTable:
    def __init__(self, table):
        self.table = table

    def validator(self):
        pipe = PipedriveAPI('TOKEN_CRM')
        result = pipe.get_all_stages().get('data')
        db = SQLServerDatabase('SERVER', 'DATABASE2', 'USERNAME_', 'PASSWORD')
        db.connect()
        for row in result:
            time.sleep(1)
            query = f"select * from {self.table} where id_stage = {row.get('id')}"
            if not db.execute_query(query, True):
                time.sleep(2)
                add_time = row.get('add_time')
                add_time_obj = datetime.strptime(add_time, "%Y-%m-%d %H:%M:%S")
                update_time = row.get('update_time')
                update_time_obj = datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
                query = f"INSERT into {self.table} (id_stage, order_nr, name, active_flag, deal_probability, pipeline_id, rotten_flag, rotten_days, add_time, update_time, pipeline_name, pipeline_deal_probability) Values ({row.get('id')}, {row.get('order_nr')}, '{row.get('name')}', '{row.get('active_flag')}','{row.get('deal_probability')}', {row.get('pipeline_id')}, '{row.get('rotten_flag')}', '{row.get('rotten_days')}', '{add_time_obj.date()}','{update_time_obj.date()}','{row.get('pipeline_name')}', '{row.get('pipeline_deal_probability')}')"
                db.execute_query(query, False)
        print(
            '''#######################################################################################################''')
        db.disconnect()
