from processes.deals import dictionary_invert
from processes.deals import get_all_option_for_fields_in_deals
from processes.deals import get_all_deals
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import DealTable
from processes.organizations import get_all_organization


if __name__ == '__main__':
<<<<<<< HEAD
    #PipelineTable('pipeline').validator()
    #StageTable('stages').validator()
    #get_all_deals()
    #print(dictionary_invert(get_all_option_for_fields_in_deals([12527, 12546, 12521, 12523]).get('12523'), 180))
    #print(PipedriveAPI('TOKEN_CRM').get_deals(2287).get('data').get('6fe64586c7f0e32e9caabde4b5c1d7a2ea697748'))
    #DealTable('DatosProyectos_PipeDrive', 'GT').distinct()
    print(get_all_organization())
    print(len(get_all_organization()))
=======

    result = DealTable('DatosProyectos_PipeDrive', 'GT').order_by_doc_status()
    print(result[0].get('583'))
    for row in result[0]:
        print(row)
>>>>>>> 69f71921740a9802b098013de19a7a43285e82d9

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
