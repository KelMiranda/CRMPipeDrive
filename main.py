from processes.pipeline import PipelineTable
from processes.usuarios import Usuarios
from processes.stages import StageTable
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import get_all_deals, save_json
from processes.notificacion import Notificaciones

if __name__ == '__main__':
    nt = Notificaciones('SV')
    nt.notificacion_ultima_conexion('kelvin.miranda@grupopelsa.com')