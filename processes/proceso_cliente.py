from database.sql_server_connection import SQLServerDatabase
from processes.cotizaciones import Cotizaciones
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.deals import dictionary_invert
from processes.organizations import OrganizationTable


def comparar_registros_cliente(registro1, registro2):
    # Normalizar nombres de campos
    campos = [
        ('CardCode', 'CardCode'),
        ('CardName', 'CardName'),
        ('Address', 'Address'),
        ('Phone1', 'Phone1'),
        ('Municipio', 'Municipio'),
        ('Departamento', 'Departamento'),
        ('E_Mail', 'E_Mail'),
        ('id_PipeDrive', 'id_PipeDrive'),
        ('fecha_registro', 'CreateDate'),
        ('Fecha_Modificacion', 'UpdateDate'),
        ('Sector', 'Sector'),
        ('Validador', 'Validador'),
        ('Coordenadas', 'Coordenadas'),
        ('Pais', 'Pais'),
        ('Vendedor_Asignado', 'SlpName'),
    ]
    
    diferencias = []
    for campo1, campo2 in campos:
        valor1 = registro1.get(campo1)
        valor2 = registro2.get(campo2)
        if str(valor1) != str(valor2):
            diferencias.append(f"Diferencia en {campo1}/{campo2}: '{valor1}' vs '{valor2}'")
    
    return diferencias


class Cliente:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.ct = Cotizaciones(self.pais)
        self.pipe = PipedriveAPI('Token')
        self.org = OrganizationTable(None, self.pais)

    def validadorCliente(self, CardCode):
        query = f"[dbo].[SP_VALIDADOR_DE_CLIENTE] '{CardCode}', '{self.pais}'"
        errores = []
        result = {}

        try:
            self.db.connect()
            consulta = self.db.execute_query(query)[0]

            if consulta[0] is None and consulta[1] is not None:
                result.update({
                    'CardCode': CardCode,
                    'id_Pipedrive': consulta[0],
                    'Validador': consulta[1],
                    'action': 1,
                    'comentario': 'El cliente no existe en pipedrive.'
                })
            elif consulta[0] is None and consulta[1] is None:
                result.update({
                    'CardCode': CardCode,
                    'action': 2,
                    'comentario': 'El cliente no esta en la tabla y tampoco en pipedrive.'
                })
            else:
                result.update({
                    'CardCode': CardCode,
                    'action': 3,
                    'comentario': 'El cliente Existe en pipedrive y tambien en la tabla.'
                })

        except Exception as e:
            error_message = f"Error al ejecutar la consulta. El error es: {str(e)}"
            errores.append(error_message)
        finally:
            if self.db:  # Verifica si db está definido y conectado
                self.db.disconnect()

        return result, errores

    def actualizacionCliente(self, id_pipedrive, datos):
        clientesModificados = {}
        if self.pipe.put_organization_id(id_pipedrive, datos).get('success') is True:
            query = f"Update DatosClientes SET Validador = 'Ñ', Fecha_Modificacion = GETDATE() Where id_PipeDrive = {id_pipedrive}"
            self.org.remove_followers(id_pipedrive, datos.get('owner_id'))
            SeguidoresSV = [13092377, 13046551]
            SeguidoresGT = [12992629, 13046551]
            seguidores = []
            if self.pais == 'SV':
                seguidores = SeguidoresSV
            elif self.pais == 'GT':
                seguidores = SeguidoresGT

            for agre in seguidores:
                add = {
                    "user_id": agre
                }
                seguidor = self.pipe.post_followers_in_organization(id_pipedrive, add).get('success')
                clientesModificados.update({
                    f"el id: '{agre}'": seguidor
                })

            if self.db.execute_query(query, False) is None:
                clientesModificados.update({
                    'CardCode': datos.get('bd4aa325c2375edc367c1d510faf509422f71a5b'),
                    'id_pipedrive': id_pipedrive,
                    'mensaje': 'Modificacion con Exito en PipeDrive y Base de dato'
                })
        return clientesModificados

    def datosClienteExistente(self, codigo_cliente, clienteTabla=True):
        resultado = self.ct.datos_cliente(codigo_cliente)
        if resultado.get('id_pipedrive') is not None:
            datos_POS = resultado.get('datos_POS')
            cuenta_asignada_query = f"SELECT COALESCE((SELECT PipedriveId FROM [PipeDrive].[dbo].[vw_idUserPipeDrive]WHERE SlpName = '{datos_POS.get('Vendedor_Asignado')}'), NULL) AS PipedriveId;"
            self.db.connect()
            cuenta_asignada = self.db.execute_query(cuenta_asignada_query)[0]
            lista = resultado.get('lista')
            id_pipedrive = resultado.get('id_pipedrive')
            datos = {
                'name': datos_POS.get('CardName'),
                'bd4aa325c2375edc367c1d510faf509422f71a5b': datos_POS.get('CardCode'),
                '8b8121d03ef920b724ffa68b0f6177fdf281ad3f': lista.get('4023').get(f"{datos_POS.get('Sector')}"),
                '99daf5439284d6a809aee36c4d52a53c9826300b': lista.get('4025').get(f"{datos_POS.get('Municipio')}"),
                'deca3dd694894b2ca93df56db39f66468cb3885d': lista.get('4024').get(
                    f"{datos_POS.get('Departamento')}"),
                '3ed19788ef9c8ebeaf0f24f58394f67ac784684c': datos_POS.get('Coordenadas'),
                'fd0f15b9338615a55ca56a3cada567919ec33306': lista.get('4028').get(
                    f"{datos_POS.get('Vendedor_Asignado')}"),
                'label': 1,
                '2d4edef00aec72dcc0fd1a240f7897fb0eb34465': lista.get('4026').get(f"{datos_POS.get('Pais')}"),
                'owner_id': cuenta_asignada[0],
                'address': datos_POS.get('address')
            }
            return datos, id_pipedrive
        elif clienteTabla is False:
            resultado = self.ct.datos_cliente(codigo_cliente)
            datos_POS = resultado.get('datos_POS')
            cuenta_asignada_query = f"SELECT COALESCE((SELECT PipedriveId FROM [PipeDrive].[dbo].[vw_idUserPipeDrive]WHERE SlpName = '{datos_POS.get('Vendedor_Asignado')}'), NULL) AS PipedriveId;"
            self.db.connect()
            cuenta_asignada = self.db.execute_query(cuenta_asignada_query)[0]
            lista = resultado.get('lista')
            datos = {
                'name': datos_POS.get('CardName'),
                'bd4aa325c2375edc367c1d510faf509422f71a5b': datos_POS.get('CardCode'),
                '8b8121d03ef920b724ffa68b0f6177fdf281ad3f': lista.get('4023').get(f"{datos_POS.get('Sector')}"),
                '99daf5439284d6a809aee36c4d52a53c9826300b': lista.get('4025').get(f"{datos_POS.get('Municipio')}"),
                'deca3dd694894b2ca93df56db39f66468cb3885d': lista.get('4024').get(
                    f"{datos_POS.get('Departamento')}"),
                '3ed19788ef9c8ebeaf0f24f58394f67ac784684c': datos_POS.get('Coordenadas'),
                'fd0f15b9338615a55ca56a3cada567919ec33306': lista.get('4028').get(
                    f"{datos_POS.get('Vendedor_Asignado')}"),
                'label': 1,
                '2d4edef00aec72dcc0fd1a240f7897fb0eb34465': lista.get('4026').get(f"{datos_POS.get('Pais')}"),
                'owner_id': cuenta_asignada[0],
                'address': datos_POS.get('address')
            }
            return datos

    def ingresar_o_actualizar_cliente_pipedrive(self, codigo_cliente):
        resultado = self.ct.datos_cliente(codigo_cliente)

        if resultado.get('status') == 'No Existe Cliente en la tabla':
            query = F"EXEC [CRM].[dbo].[SP_VALIDADOR_CLIENTE_MERGE_{self.pais}] '{codigo_cliente}'"
            print(query)
        elif resultado.get('Status') == 'Si existe en pipedrive y tambien en la tabla':
            if resultado.get('Diferencia de datos entre POS y VW_POS') is False:
                query = F"EXEC [CRM].[dbo].[SP_VALIDADOR_CLIENTE_MERGE_{self.pais}] '{codigo_cliente}'"
                print(query)
                print(self.datosClienteExistente(codigo_cliente))
        elif resultado.get('Status') == 'No existe en pipedrive, pero si en la tabla':
            print("Estoy aqui"),
            print(self.datosClienteExistente(codigo_cliente, False))








