import os
import time
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from database.sql_server_connection import SQLServerDatabase
from processes.deals import get_all_option_for_fields_in_deals
from processes.deals import dictionary_invert
from processes.deals import save_json
from pipedrive.users_pipedrive import GetIdUser
import hashlib
import pandas as pd
import configparser


def generar_hash_sha256(data):
    """
    Genera un hash SHA-256 a partir de los datos proporcionados.

    Parámetros:
    data (iterable): Un conjunto de datos (como una fila de un DataFrame).
                     Convierte cada valor en una cadena, manejando valores None de manera específica.

    Retorna:
    str: El hash SHA-256 generado como una cadena hexadecimal.
    """
    # Convertir cada valor a una cadena, manejando valores None como 'NULL'
    data_str = '|'.join([str(valor) if valor is not None else 'NULL' for valor in data])

    # Crear un objeto hash SHA-256
    hash_obj = hashlib.sha256()

    # Actualizar el objeto hash con los datos en formato de bytes
    hash_obj.update(data_str.encode('utf-8'))

    # Devolver el hash como una cadena hexadecimal
    return hash_obj.hexdigest()

def get_all_option_for_fields_in_get_all_organization(id_field_organization):
    my_dictionary = {}
    for row in id_field_organization:
        my_dictionary[f"{row}"] = PipedriveAPI('Token').get_organization_field_id(row)
    return my_dictionary

def get_all_organization():
    data = {
        "company_domain": "grupopelsa",
        "start": 0,
        "limit": 100,
    }
    result = PipedriveAPI('Token').get_records('organizations', data)
    return result

class OrganizationTable:
    def __init__(self, table=None, country=None):
        self.table = table
        self.country = country
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.pipe = PipedriveAPI('Token')

    def get_customers_from_a_table(self):
        query = f"Select * from {self.table} Where Pais = '{self.country}' AND Vendedor_Asignado != 'SIN CARTERA ASIGNADA' AND id_PipeDrive > 0 order by id_PipeDrive"
        print(query)
        self.db.connect()
        result = self.db.execute_query(query)
        self.db.disconnect()
        return result

    def get_all_values_of_assigned_salesperson(self):
        query = f"Select distinct Vendedor_Asignado from {self.table} Where Pais = '{self.country}' AND Vendedor_Asignado != 'SIN CARTERA ASIGNADA'"
        self.db.connect()
        not_salesperson_in_crm = {}
        all_salesperson = self.db.execute_query(query)
        values = get_all_option_for_fields_in_deals([12521])
        for row in all_salesperson:
            validator = values.get('12521').get(row[0])
            if validator is None:
                not_salesperson_in_crm[f'{row[0]}'] = 'No existe en el crm'
        self.db.disconnect()
        return not_salesperson_in_crm

    def assign_owner_in_the_crm(self):
        result = self.get_customers_from_a_table()
        pipe = self.pipe
        data = {}
        total = len(result)
        count = 0
        for row in result:
            count = count + 1
            time.sleep(1.5)
            result2 = GetIdUser(f'{row[15]}').get_user_id_and_sector()
            id_empresa = result2.get('id_user_pipedrive')
            if id_empresa is None:
                data = {
                    "owner_id": 12806795,
                    "fd0f15b9338615a55ca56a3cada567919ec33306": 715
                }
            else:
                data = {
                    "owner_id": id_empresa,
                    "fd0f15b9338615a55ca56a3cada567919ec33306": pipe.get_organization_field_id('4028').get(f'{row[15]}')
                }
            request = pipe.put_organization_id(row[8], data)

            if request.get('success'):
                print(f'El Cliente {row[2]}, con un id: {row[8]} fue modificado')
            else:
                print(f'presento un problema el id: {row[8]}, el problema es: {request}')

            self.remove_followers(row[8])
            iteration = total - count
            print(f'########----{iteration}------#########################################################')

    def remove_followers(self, id_organization, id_user_pipedrive=True):
        result = self.pipe.get_organization_id(id_organization)
        followers_result = result['additional_data']['followers']
        value_customer = result['data']['fd0f15b9338615a55ca56a3cada567919ec33306']
        customer = self.pipe.get_organization_field_id('4028')
        customer_name = dictionary_invert(customer, value_customer)
        if id_user_pipedrive is True:
            id_customer = str(GetIdUser(f'{customer_name}').get_user_id_and_sector()['id_user_pipedrive'])
        else:
            id_customer = id_user_pipedrive

        if len(followers_result) == 0:
            print('No tiene seguidores')
        else:
            for row in followers_result:
                result2 = followers_result.get(f'{row}')
                id_follower = result2.get('id')
                if row == id_customer:
                    print(f'el dueño es: {row}')
                else:
                    print(f'el vendedor:{row}, deja de seguir a este cliente')
                    print(self.pipe.delete_followers_in_organization(id_organization, id_follower).get('success'))

    def validador_de_clientes(self):
        client = get_all_organization()
        self.db.connect()

        # Inicializa las listas fuera del bucle
        noexiste = []
        existe = []
        problema = []

        for row in client:
            time.sleep(0.1)
            id_cliente = row.get('id')
            CardCode_Pipe = str(row.get('bd4aa325c2375edc367c1d510faf509422f71a5b'))
            query = f"Select top 1 * from DatosClientes Where id_PipeDrive = {id_cliente}"
            result = self.db.execute_query(query)

            if not result:
                # Añade un diccionario a la lista
                noexiste.append({'id_PipeDrive': id_cliente, 'Comentario': "no existe en la base de datos"})
            else:
                # Como result no está vacío, es seguro acceder a su contenido.
                CardCode_base = result[0][1]
                if CardCode_base == CardCode_Pipe:
                    existe.append({'id_PipeDrive': id_cliente, 'Comentario': "Son iguales en la base de datos"})
                else:
                    problema.append({'id_PipeDrive': id_cliente, 'Comentario': "Si existe en base, pero con diferente codigo"})
                    query2 = f"UPDATE DatosClientes SET CardCode = '{CardCode_Pipe}' Where id_PipeDrive = {id_cliente}"
                    time.sleep(1)
                    print(id_cliente, query2)
                    self.db.execute_query(query2, False)
        self.db.disconnect()

        # Imprime los resultados fuera del bucle
        save_json(noexiste, 'CardCode_NoExiste')
        save_json(existe, 'CardCode_Existe')
        save_json(problema, 'CardCode_Con_Problema')

    def nombres_vendedor_asignados_organizacion(self):
        si_existe = []
        no_existe = []
        query = f"Select distinct Vendedor_Asignado from {self.table} Where Pais = '{self.country}' AND id_PipeDrive != 0"
        self.db.connect()
        valores = self.db.execute_query(query)
        opciones = get_all_option_for_fields_in_get_all_organization([4028]).get('4028')
        for valor in valores:
            if opciones.get(f'{valor[0]}'):
                si_existe.append({f'{valor[0]}': 'Existe'})
            else:
                no_existe.append({f'{valor[0]}': 'No Existe'})

        output = {'Si Existen': si_existe,
                  'No Existe': no_existe}
        return output

    def cotizaciones_por_clientes(self):
        try:
            query = f"SELECT * FROM {self.table} WHERE Pais = '{self.country}'"
            self.db.connect()
            valores = self.db.execute_query(query)
            for valor in valores:
                codigo_cliente = valor[1]
                query2 = f"SELECT COUNT(*) AS Total_Trato FROM DatosProyectos_PipeDrive WHERE CardCode = '{codigo_cliente}' AND Pais = '{self.country}'"
                Numero_de_tratos = self.db.execute_query(query2)[0][0]
                query3 = f"UPDATE DatosClientes SET #cotizaciones = {Numero_de_tratos} WHERE CardCode = '{codigo_cliente}' AND Pais = '{self.country}'"
                modificando = self.db.execute_query(query3, False)
                if modificando is None:
                    print(f"El cliente con codigo: {codigo_cliente} tiene: {Numero_de_tratos} Cotizaciones")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.db.disconnect()

    def nombres_vendedor_asignado(self):
        si_existe = []
        no_existe = []
        query = f"Select distinct Vendedor_Asignado from {self.table} Where Pais = '{self.country}'"
        self.db.connect()
        valores = self.db.execute_query(query)
        opciones = get_all_option_for_fields_in_get_all_organization([4028]).get('4028')
        for valor in valores:
            if opciones.get(f'{valor[0]}'):
                si_existe.append({f'{valor[0]}': 'Existe'})
            else:
                no_existe.append({f'{valor[0]}': 'No Existe'})

        output = {'Si Existen': si_existe,
                  'No Existe': no_existe}
        return output

    def hashTablaClientes(self, codigoCliente, tabla):
        """
        Genera hashes para los registros de la tabla de clientes según el código del cliente y la tabla especificada.

        Parámetros:
        codigoCliente (str): El código del cliente que deseas consultar.
        tabla (str): El nombre de la tabla que deseas consultar.

        Retorna:
        pd.DataFrame: Un DataFrame con los datos del cliente y sus hashes generados.
        """
        # Establecemos la conexión a la base de datos
        self.db.connect()

        # Verificamos el nombre de la tabla y construimos el query SQL adecuado
        if tabla == 'DatosClientes':
            # Consulta SQL para la tabla 'DatosClientes'
            query = f"""
            Select CardCode, CardName, Address, Phone1, Municipio, Departamento, E_Mail, 
                   CONVERT(date, fecha_registro) AS CreateDate, 
                   CONVERT(DATE, Fecha_Modificacion) AS UpdateDate, 
                   Sector, Coordenadas, Vendedor_Asignado as SlpName, CodigoSAP as SlpCode 
            from {tabla} 
            where CardCode = '{codigoCliente}' AND Pais = '{self.country}'
            """
        elif tabla == '[dbo].[VW_DATOS_CLIENTES_SV]' or '[dbo].[VW_DATOS_CLIENTES_GT]' or '[dbo].[VW_DATOS_CLIENTES_HN]':
            # Consulta SQL para la vista 'VW_DATOS_CLIENTES_SV'
            query = f"""
            SELECT CardCode, CardName, Address, Phone1, Municipio, Departamento, E_Mail, 
                   CreateDate, UpdateDate, Sector, Coordenadas, SlpName, SlpCode 
            FROM {tabla} 
            where CardCode = '{codigoCliente}'
            """
        else:
            # Si la tabla no es ninguna de las anteriores, lanzamos un error
            raise ValueError("Tabla no soportada.")

        # Ejecutamos la consulta SQL
        result = self.db.execute_query(query)

        # Convertimos el resultado en un DataFrame
        df = pd.DataFrame(result)

        # Verificamos si el DataFrame tiene datos antes de aplicar el hash
        if not df.empty:
            # Aplicamos la función de hashing a cada fila del DataFrame
            df['hash'] = df.apply(lambda row: generar_hash_sha256(row), axis=1)
        else:
            print("No se encontraron datos para el cliente especificado.")

        # Devolvemos el DataFrame con los datos y la columna de hash generada
        return df

