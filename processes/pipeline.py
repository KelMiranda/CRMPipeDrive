import os
from pipedrive.pipedrive_api_conecction import PipedriveAPI
import time


class PipelineTable:
    def __int__(self):
        pass

    def validator(self):
        pipe = PipedriveAPI('TOKEN_CRM')
        result = pipe.get_all_pipelines().get('data')
        for row in result:
            time.sleep(1)
            print(row)
