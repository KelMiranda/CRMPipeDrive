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
        print(query)
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
        self.db.connect()
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
            self.db.disconnect()
        return clientesModificados

    def obtener_id_pipedrive_vendedor(self, vendedor_asignado):
        query = f"""
                SELECT COALESCE((
                    SELECT PipedriveId 
                    FROM [PipeDrive].[dbo].[VendedoresConCredenciales]
                    WHERE SlpName = '{vendedor_asignado}'
                ), NULL) AS PipedriveId
            """
        self.db.connect()
        resultado = self.db.execute_query(query, [vendedor_asignado])
        self.db.disconnect()
        return resultado[0] if resultado else None

    def construir_datos_cliente(self, resultado):
        datos_POS = resultado.get('datos_POS')
        lista = resultado.get('lista')
        cuenta_asignada = self.obtener_id_pipedrive_vendedor(datos_POS.get('Vendedor_Asignado'))
        datos_cliente = {
            'name': datos_POS.get('CardName'),
            'bd4aa325c2375edc367c1d510faf509422f71a5b': datos_POS.get('CardCode'),
            '8b8121d03ef920b724ffa68b0f6177fdf281ad3f': self.obtener_valor_lista(lista, '4023', datos_POS,
                                                                                 'Sector'),
            '99daf5439284d6a809aee36c4d52a53c9826300b': self.obtener_valor_lista(lista, '4025', datos_POS,
                                                                                 'Municipio'),
            'deca3dd694894b2ca93df56db39f66468cb3885d': self.obtener_valor_lista(lista, '4024', datos_POS,
                                                                                 'Departamento'),
            'fd0f15b9338615a55ca56a3cada567919ec33306': self.obtener_valor_lista(lista, '4028', datos_POS,
                                                                                 'Vendedor_Asignado'),
            '2d4edef00aec72dcc0fd1a240f7897fb0eb34465': self.obtener_valor_lista(lista, '4026', datos_POS,
                                                                                 'Pais'),
            '3ed19788ef9c8ebeaf0f24f58394f67ac784684c': datos_POS.get('Coordenadas'),
            'owner_id': cuenta_asignada[0],
            'address': datos_POS.get('address'),
            'label': 1
        }
        return datos_cliente, resultado.get('id_pipedrive')

    def obtener_valor_lista(self, lista, key, datos_POS, campo):
        return lista.get(key).get(f"{datos_POS.get(campo)}")

    def datos_cliente_existente(self, codigo_cliente, clienteTabla=True):
        resultado = self.ct.datos_cliente_vw_table_pipedrive(codigo_cliente)
        if resultado.get('id_pipedrive') is not None:
            return self.construir_datos_cliente(resultado)
        elif not clienteTabla:
            return self.construir_datos_cliente(resultado)
        return None

    def actualizar_tablas(self, id_pipedrive, id_registro):
        query = F"UPDATE [CRM].[dbo].[DatosClientes] SET id_PipeDrive = {id_pipedrive}, Validador =  'Ñ' Where id_clientes = {id_registro}"
        self.db.connect()
        self.db.execute_query(query, False)
        self.db.disconnect()
        return "-----------------idPipeDrive ingresado-------------------"

    def actualizarCliente(self, codigo_cliente):
        try:
            # Obtener los datos del cliente
            resultado = self.ct.datos_cliente_vw_table_pipedrive(codigo_cliente)
            id_registro = resultado.get('id_registro')
            id_pipedrive = resultado.get('id_pipedrive')

            # Construir los datos del cliente para la actualización
            data = self.construir_datos_cliente(resultado)[0]

            # Actualizar la organización en Pipedrive
            insert = self.pipe.put_organization_id(id_pipedrive, data)

            if insert.get('success'):
                # Actualizar las tablas locales si la actualización en Pipedrive fue exitosa
                print(id_pipedrive, id_registro)
                self.actualizar_tablas(id_pipedrive, id_registro)
                return {"id_registro": id_registro, "id_pipedrive": id_pipedrive}
            else:
                return {"error": "No se pudo actualizar el cliente en Pipedrive."}

        except Exception as e:
            return {"error": f"Error al actualizar el cliente: {str(e)}"}

    def ingresandoCliente(self, codigo_cliente):
        try:
            # Obtener los datos del cliente
            resultado = self.ct.datos_cliente_vw_table_pipedrive(codigo_cliente)

            # Verificar si el cliente existe en la base de datos
            if resultado.get('Status') == 'No Existe Cliente en la tabla':
                return {"error": "El cliente no existe en la tabla de datos."}

            id_registro = resultado.get('id_registro')

            # Construir los datos del cliente para la inserción
            data = self.construir_datos_cliente(resultado)[0]

            # Insertar la organización en Pipedrive
            insert = self.pipe.post_organization(data)

            if insert.get('success'):
                # Actualizar las tablas locales si la inserción en Pipedrive fue exitosa
                id_pipedrive = insert.get('data').get('id')
                self.actualizar_tablas(id_pipedrive, id_registro)
                return {"id_registro": id_registro, "id_pipedrive": id_pipedrive}
            else:
                return {"error": "No se pudo insertar el cliente en Pipedrive."}

        except Exception as e:
            return {"error": f"Error al ingresar el cliente: {str(e)}"}

    def ingresando_cliente(self, codigo_cliente):
        self.db.connect()
        query = f"EXEC [dbo].[SP_VALIDADOR_DE_CLIENTE] '{codigo_cliente}', '{self.pais}'"
        result = self.db.execute_query(query)
        print(result)



