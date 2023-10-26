from processes.deals import dictionary_invert
from processes.deals import get_all_option_for_fields_in_deals
from processes.deals import make_all_deals

if __name__ == '__main__':
    #PipelineTable('pipeline').validator()
    #StageTable('stages').validator()
    make_all_deals()
    #print(dictionary_invert(get_all_option_for_fields_in_deals([12527, 12546, 12521, 12523]).get('12523'), 180))
    print('fin')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
