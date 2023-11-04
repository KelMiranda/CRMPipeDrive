from processes.deals import dictionary_invert
from processes.deals import get_all_option_for_fields_in_deals
from processes.deals import get_all_deals
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import DealTable


if __name__ == '__main__':

    result = DealTable('DatosProyectos_PipeDrive', 'GT').order_by_doc_status()
    print(result[0].get('583'))
    for row in result[0]:
        print(row)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
