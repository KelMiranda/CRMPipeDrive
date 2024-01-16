from processes.pipeline import PipelineTable
from processes.stages import StageTable
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import get_all_deals, save_json

if __name__ == '__main__':
    get_all_deals()
    #StageTable().obteniendo_todos_los_estados()
