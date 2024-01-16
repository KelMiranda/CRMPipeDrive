import os
from database.sql_server_connection import SQLServerDatabase
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from datetime import datetime
import time


class PipelineTable:
    def __init__(self):
        self.pipe = PipedriveAPI('Token')

    def obteniendo_todos_los_embudos(self):
        resultado = self.pipe.get_all_pipelines()['data']
        return resultado
