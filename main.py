from processes.stages import StageTable
from processes.pipeline import PipelineTable


if __name__ == '__main__':
    PipelineTable('pipeline').validator()
    StageTable('stages').validator()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
