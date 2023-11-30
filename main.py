from processes.deals import dictionary_invert
from processes.deals import get_all_option_for_fields_in_deals
from processes.deals import get_all_deals
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import DealTable
from processes.organizations import get_all_organization
from processes.organizations import OrganizationTable
from processes.deals import save_json
from pipedrive.users_pipedrive import GetIdUser
import json

if __name__ == '__main__':
    OrganizationTable('DatosClientes','SV').assign_owner_in_the_crm()

