import os
from processes.stages import StageTable
from processes.pipeline import PipelineTable
from processes.deals import DealTable
from pipedrive.pipedrive_api_conecction import PipedriveAPI


if __name__ == '__main__':
    #PipelineTable('pipeline').validator()
    #StageTable('stages').validator()
    DealTable('deals').make_all_deals()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
