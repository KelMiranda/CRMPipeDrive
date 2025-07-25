from stringprep import in_table_d1
from database.sql_server_connection import SQLServerDatabase
from time import sleep, time
from processes.deals import get_all_option_for_fields_in_deals
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.organizations import get_all_option_for_fields_in_get_all_organization
from processes.deals import dictionary_invert
import configparser
import os as cd
import datetime

familias_padres = {
    'CAJAS TERMICAS, BRK': 'c97bd1f994dce3b891f1189965c06ef775b53757',
    'CANALIZ Y ACC MONTAJ': 'd8b5d8cdff3533b40d7374a4f9cfbfd0584f2037',
    'CONDUCTOR Y ACC': 'c08631f1baceb0fb1cd7c34edaef621c6dd911fe',
    'CONTROL': '557101afbead32fca908341f294788fb6dd57dd9',
    'DESCONTINUADOS': '16b85bc05946a911000eda5f6c95578bb9b1db50',
    'ENSAMBLE ARMADO': '9bf8fb0b8840223389f599ad4a1ef25271abdb28',
    'ENSAMBLE PROYECTO': 'beaaabe8333b58df8b8971601d08a5257cf0fcb0',
    'EQUIPO, HERRAMIENTAS': '588ad42ea917eb08864d97c7b60b401bd5d9b864',
    'ILUMINACION Y ACC': 'def1bf7c50affda41b5f259ad136adb1eba39ecf',
    'INGENIERIA': '4cd3d321ecc87ace08b03aefc712f50df86dec48',
    'INTR, TOMA, PLACA': '71f471c6924d9bb1cce5b55c02ba8ce82ca4d77b',
    'LINEAS DISTRIB Y TEL': 'f65cdf161909babfada6f69d55c0503b0fa8cfe4',
    'POSTES': '57efa7dfd4669f9bf76c77287b859bbd3238caf7',
    'PRODUCTOS P/DATOS': 'df423477485bc5fa9c447c497fd9b45c4157850b',
    'PROTEC ALTA/BAJA T': '26b869616ea34b1dd7cae7b86b842f7f58a19882',
    'REGULADOR DE ENERGIA': 'fef3cd02a2a74170c9ef7a7c9105a56b9803aaca',
    'SERVICIO EXTERNO': '6065a5cb51451f337f93c2cf910bbaf52b1f2b69',
    'TRANSFORM Y ACC': 'b88c83c134b66846b742619004c6163b94c63024'
}
datos_cotizacion = {
    'vendedor_asignado': 'bdc9870365278bf245effd816618a8a9bff8fad9',
    'vendedor_cot': 'c0af428ccdb6d8605a475372986995a0a6ed0a69',
    'Sector_Vendedor': '057ae06bd90a1bcecb68ebceb30b99fb8be94801',
    'Pais': '6aba016cdd852ee60aa6ae2ced2af84b9105d78c',
    'obtener_estado_cotizacion': '6fe64586c7f0e32e9caabde4b5c1d7a2ea697748',
    'DocNum': '1b847f729d427a61ac42094df3070a2cee4a0286',
    'Serie': '801b170ad3139ba6ba293ac71270ddb96c8b8868',
    'Comentario_POS': 'c1cbb4df13d9054e0c1bb4f99535ab0a1e9e668c',
    'Descripcion_Pos': '9ac480743304f616d3575decabf7114625eddf53',
    'T_Sector_Cliente': '9a5bb72d44fb456c5c89624053ff099c291bced4',
    'expected_close_date': 'expected_close_date',
    'label': 'label',
    'Valor': 'value',
    'Título': 'title',
    'Organizacion': 'org_id',
    'DocDate': 'add_time',
    'DocDate1': '95b91ae97456e23b83e3a8a43f650a0156fff2f7',
    'Autorizado': '1b27f2b74dcfb24d3dd5e4dfb5611da7150afa20',
    'obtener_tipo_cotizacion': '6840b183ea0a8dd8a55b4f7cd773a4d1f73e442a',
    'CardName': '060d979042413ee06230b755710f42901b6b0a92'
}
datos_cliente = {
    'CardCode': 'bd4aa325c2375edc367c1d510faf509422f71a5b',  # Código del cliente
    'CardName': 'name',  # Nombre del cliente
    'address': 'address',  # Dirección del cliente
    'Municipio': '99daf5439284d6a809aee36c4d52a53c9826300b',  # Municipio del cliente
    'Departamento': 'deca3dd694894b2ca93df56db39f66468cb3885d',  # Departamento del cliente
    'Pais': '2d4edef00aec72dcc0fd1a240f7897fb0eb34465',  # País del cliente
    'Sector': '8b8121d03ef920b724ffa68b0f6177fdf281ad3f',  # Sector del cliente
    'Coordenadas': '3ed19788ef9c8ebeaf0f24f58394f67ac784684c',  # Coordenadas del cliente
    'Vendedor_Asignado': 'fd0f15b9338615a55ca56a3cada567919ec33306'  # Vendedor asignado al cliente
}
id_jefes_sector_sv = {
    'CONTRA': 13042899,
    'IGO': 13045165,
    'RETAIL - AV': 13091607,
    'RETAIL - FB': 13091607,
    'RETAIL- SM': 13091607,
    'MAYO': 13060961,
    'ING': 13046551,
    'UTIL': 12806795
}
id_jefes_sector_gt = {
    'GT': 12992629
}
id_jefes_sector_hn = {
    'HN': 21968289
}
currency_mapping = {'SV': 'USD', 'GT': 'GTQ', 'HN': 'HNL'}

def manejar_no_existencia_campo(field_id, value, metodo):
    error_message = (
        f"Para el campo '{field_id}', no existe el valor '{value}'. "
        f"Ruta del archivo: {cd.path.abspath(__file__)}, "
        f"Método: {metodo}"
    )

    # Aquí se registra el error en el archivo de log
    log_error_campos(error_message)

    # También puedes retornar el mensaje de error si necesitas manejarlo en otro lugar
    return {"error": error_message}
def notificar_errores(errores):
    # Aquí puedes implementar la lógica para enviar notificaciones con la lista de errores
    print("Enviando notificación de errores:", errores)
def log_error_campos(mensaje):
    with open("errores_de_selection.log", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {mensaje}\n")

class Cotizaciones:
    def __init__(self, pais):
        self.pais = pais
        self.db = SQLServerDatabase('SERVER', 'DATABASE', 'USERNAME_', 'PASSWORD')
        self.pipe = PipedriveAPI('Token')

    def cierre_de_cotizaciones(self):
        errores = []
        result = []
        query = f'EXEC [dbo].[SP_CERRANDO_COTIZACIONES_{self.pais}]'

        try:
            self.db.connect()
            result = self.db.execute_query(query)

        except Exception as e:
            error_message = f"Error al ejecutar la consulta dicho error es: {str(e)}"
            log_error_campos(error_message)

        finally:
            self.db.disconnect()

        if errores:
            notificar_errores(errores)

        return result, errores

    def validar_cotizacion(self, ord=None, docnum=None, serie=None, CardCode=None):
        documentos_actualizados = []
        errores = []

        if ord is None and docnum is None and serie is None and CardCode is None:
            result = self.cierre_de_cotizaciones()
            if len(result[0]) == 0:
                documentos_actualizados.append(f'No hay cotizaciones en la funcion de cierre en: {self.pais}')
                errores.append(f"No hay error en la funcion de cierre en: {self.pais}")
            else:
                total = len(result[0])
                for count, row in enumerate(result[0], start=1):
                    iter = total - count
                    print(f"-------------#Documentos Faltantes: {iter}---------------------------")
                    query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{row[2]}',{row[3]},'{row[4]}'"
                    try:
                        self.db.connect()
                        query_result = self.db.execute_query(query, False)
                        documentos_actualizados.append(row[3])
                        if query_result is not None:
                            errores.append(f"Consulta vacía en iteración {count}")
                    except Exception as e:
                        error_message = f"Error al ejecutar consulta en iteración {count}: {str(e)}"
                        errores.append(error_message)
                    finally:
                        self.db.disconnect()

        else:
            query = f"EXEC [dbo].[SP_VALIDADOR_PROYECTO_MERGE_{self.pais}]'{ord}',{docnum},'{serie}', '{CardCode}'"
            query_validador = f"Select * from DatosProyectos_PipeDrive Where DocNum = {docnum} AND ORD ='{ord}' AND CardCode = '{CardCode}'"
            self.db.connect()
            query_validador_result = self.db.execute_query(query_validador)
            if query_validador_result:
                try:
                    query_result = self.db.execute_query(query, False)
                    if query_result is not None:
                        errores.append("Consulta vacía")
                    documentos_actualizados.append(docnum)
                except Exception as e:
                    error_message = f"Error al ejecutar consulta: {str(e)}"
                    errores.append(error_message)
                finally:
                    self.db.disconnect()
            else:
                error_message = f"El numero de documento: {docnum}, no pertenece a la tabla ORD{ord}"
                errores.append(error_message)

        print('######################Finalizando Proceso##########################################')
        return documentos_actualizados, errores

    def obtener_cotizaciones(self, sector, validador):
        errores = []
        result = []
        query = f"EXEC [dbo].[SP_SECTOR]'{self.pais}', '{sector}', '{validador}'"
        try:
            self.db.connect()
            result = self.db.execute_query(query)

        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def obtener_cotizaciones_abiertas(self, SlpName):
        errores = []
        result = []
        query = f"Select SlpName, CardCode, CardName, COUNT(*) AS #Cotizaciones from DatosProyectos_PipeDrive Where DocStatus = 'O' AND Pais = '{self.pais}' AND SlpName = '{SlpName}' Group By SlpName, CardCode, CardName Order By #Cotizaciones desc"
        try:
            self.db.connect()
            result = self.db.execute_query(query)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def cotizaciones_del_dia(self, fecha=None):
        errores = []
        result = []
        query = f"EXEC [dbo].[SP_Cotizaciones_Dia_{self.pais}]'{fecha}'"
        #query = f"EXEC [dbo].[SP_Cotizaciones_Dia_{self.pais}]"
        print(query)
        try:
            self.db.connect()
            result = self.db.execute_query(query)
        except Exception as e:
            error_message = f"Error al ejecutar cotizaciones_del_dia el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def ultima_version(self, docnum, ORD, cardcode):
        query = f"EXEC [dbo].[SP_COTIZACIONES_BUSQUEDA_{self.pais}_PY] {docnum}, '{ORD}', '{cardcode}'"
        errores = []
        result = []
        try:
            self.db.connect()
            result = self.db.execute_query(query)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def familia_padre_de_la_cotizacion(self, DocNum, DocEntry):
        errores = []
        try:
            # Intenta conectarse a la base de datos y ejecutar la consulta
            self.db.connect()
            query = f"EXEC [dbo].[SP_DetalleProducto_{self.pais}] {DocNum}, {DocEntry}"
            valores = self.db.execute_query(query)
            # Procesa los resultados de la consulta
            result = {}
            currency_mapping = {'SV': 'USD', 'GT': 'GTQ', 'HN': 'HNL'}
            currency = currency_mapping.get(self.pais, 'USD')
            for row in valores:
                clave_familia = familias_padres.get(row[1])
                if clave_familia is not None:
                    result.update({f"{clave_familia}": float(row[0]), f"{clave_familia}_currency": currency})
                else:
                    print(f"Clave {row[1]} no encontrada en familias_padres.")

            return result
        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la conexión a la base de datos o la ejecución de la consulta
            errores.append({'DocNum': DocNum, 'msg_error': str(e)})
            # Decide cómo quieres manejar este error; podrías retornar None, una lista vacía, o re-lanzar la excepción
            return None
        finally:
            # Código que se ejecutará independientemente de si se produjo una excepción o no
            # Por ejemplo, cerrar la conexión a la base de datos si está abierta
            if self.db.connect():
                self.db.disconnect()
                print("La conexión a la base de datos se ha cerrado.")

    def datos_de_la_cotizacion(self, DocNum, DocEntry):
        result = {}
        errores = []
        data = {}
        try:
            id_fields_deals = [12527, 12546, 12521, 12523, 12522, 12524, 12531, 12529, 12534, 12475]
            values = get_all_option_for_fields_in_deals(id_fields_deals)
            print(values.get('12475'))
            # Intenta conectarse a la base de datos y ejecutar la consulta
            self.db.connect()
            query = f"EXEC [dbo].[SP_COTIZACIONES_{self.pais}_PYTHON]  {DocNum}, {DocEntry}"
            print(query)
            valores = self.db.execute_query(query)[0]
            self.obtener_y_actualizar_datos_pais({'Vendedor_Asignado': valores[0]}, data)
            def actualizar_data1(valores, values):
                # Casos especiales donde se necesita un "stage_id"
                casos_especiales = ["Presupuesto", "Recotización", "Cierre por cambio de cotizacion"]
                # Configura "data1" según el motivo de pérdida
                if valores[8] in casos_especiales:
                    data1 = {
                        "status": "lost",
                        "lost_reason": f"{valores[8]}",
                        "stage_id": 21
                    }
                elif valores[8] == "Venta":
                    validador = self.consulta_factura(DocNum, DocEntry)
                    if validador == 'Sin Factura':
                        data1 = {
                            "status": "lost",
                            "lost_reason": "Cotización mal cerrada en pos"
                        }
                    else:
                        data1 = {
                            "status": "won"
                        }
                        data1.update(validador)
                elif valores[8] == "Venta Parcial":
                    validador = self.consulta_factura(DocNum, DocEntry)
                    if validador == 'Sin Factura':
                        data1 = {
                            "status": "lost",
                            "lost_reason": "Cotización mal cerrada en pos"
                        }
                    else:
                        data1 = {
                            "status": "won"
                        }
                        data1.update(validador)
                else:
                    # Configuración general para los casos de pérdida
                    data1 = {
                        "status": "lost",
                        "lost_reason": f"{valores[8]}"
                    }
                return data1

            cliente = self.datos_cliente_vw_table_pipedrive(valores[18])
            datosClientes = {
                "Status": cliente.get('Status'),
                "POS != Pipedrive": cliente.get('Diferencia de datos entre POS y pipeDrive'),
                "POS != VW_POS": cliente.get('Diferencia de datos entre POS y VW_POS')
            }
            datos_coti={
                f"{datos_cotizacion.get('vendedor_asignado')}": values.get('12521').get(f'{valores[0]}'),
                f"{datos_cotizacion.get('vendedor_cot')}": values.get('12522').get(f'{valores[1]}'),
                f"{datos_cotizacion.get('Sector_Vendedor')}": values.get('12523').get(f'{valores[2]}'),
                f"{datos_cotizacion.get('Pais')}": values.get('12524').get(f'{valores[3]}'),
                f"{datos_cotizacion.get('obtener_estado_cotizacion')}": values.get('12527').get(f'{valores[4]}'),
                f"{datos_cotizacion.get('DocNum')}": valores[5],
                f"{datos_cotizacion.get('Serie')}": valores[6],
                f"{datos_cotizacion.get('T_Sector_Cliente')}": values.get('12529').get(f'{valores[9]}'),
                f"{datos_cotizacion.get('expected_close_date')}": valores[10].strftime('%Y-%m-%d'),
                f"{datos_cotizacion.get('label')}": valores[11],
                f"{datos_cotizacion.get('Valor')}": float(valores[12]),
                f"{datos_cotizacion.get('Título')}": valores[13],
                f"{datos_cotizacion.get('Organizacion')}": valores[14],
                f"{datos_cotizacion.get('DocDate')}": valores[15].strftime('%Y-%m-%d'),
                f"{datos_cotizacion.get('DocDate1')}": valores[15].strftime('%Y-%m-%d'),
                f"{datos_cotizacion.get('Autorizado')}": values.get('12534').get(f'{valores[16]}'),
                f"{datos_cotizacion.get('obtener_tipo_cotizacion')}": values.get('12546').get(f'{valores[17]}'),
                f"{datos_cotizacion.get('CardName')}": valores[18]
            }
            currency = currency_mapping.get(self.pais, 'USD')
            datos_coti.update({"currency": currency})
            familias_padres = self.familia_padre_de_la_cotizacion(DocNum, DocEntry)
            if valores[4] == 'Closed' or valores[4] == 'Process':
                datos_coti.update(
                    {
                        f"{datos_cotizacion.get('Comentario_POS')}": valores[7],
                        f"{datos_cotizacion.get('Descripcion_Pos')}": values.get('12531').get(f'{valores[8]}'),
                    }
                )
                dato_cierre = actualizar_data1(valores, values)
                data.update(dato_cierre)

            data.update(datos_coti)
            data.update(familias_padres)
            return data

        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la conexión a la base de datos o la ejecución de la consulta
            errores.append({'DocNum': DocNum, 'msg_error': str(e)})
            # Decide cómo quieres manejar este error; podrías retornar None, una lista vacía, o re-lanzar la excepción
            return errores
        finally:
            # Código que se ejecutará independientemente de si se produjo una excepción o no
            # Por ejemplo, cerrar la conexión a la base de datos si está abierta
            if self.db.connect():
                self.db.disconnect()
                print("La conexión a la base de datos se ha cerrado.")

    def marcar_de_la_cotizacion(self, DocNum, DocEntry):
        result = []
        errores = []
        salida = []
        try:
            self.db.connect()
            query = f"Select distinct FirmName from [dbo].[VW_D_PRO_SV] Where DocNum = {DocNum} AND DocEntry = {DocEntry}"
            valores = self.db.execute_query(query)
            for row in valores:
                salida.append(row)
            # Procesa los resultados de la consulta
            result = ", ".join([elemento[0] for elemento in salida])
            return result

        except Exception as e:
            # Maneja cualquier excepción que ocurra durante la conexión a la base de datos o la ejecución de la consulta
            errores.append({'DocNum': DocNum, 'msg_error': str(e)})
            # Decide cómo quieres manejar este error; podrías retornar None, una lista vacía, o re-lanzar la excepción
            return errores
        finally:
            # Código que se ejecutará independientemente de si se produjo una excepción o no
            # Por ejemplo, cerrar la conexión a la base de datos si está abierta
            if self.db.connect():
                self.db.disconnect()
                print("La conexión a la base de datos se ha cerrado.")

    def cotizaciones_por_sector(self, sector, validador):
        errores = []
        result = []
        query = f"Select DocNum, DocEntry from DatosProyectos_PipeDrive Where Pais = '{self.pais}' AND Validador = '{validador}' AND U_JEFE = '{sector}'"
        try:
            self.db.connect()
            result = self.db.execute_query(query)

        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
            errores.append(error_message)
        finally:
            self.db.disconnect()
        return result, errores

    def obtener_datos_pos(self, codigoCliente):
        """
            Función para obtener los datos del cliente desde la tabla 'DatosClientes' (POS).

            Entradas:
            - codigoCliente: Código del cliente que se quiere buscar en la tabla 'DatosClientes'.

            Salidas:
            - datos_POS: Diccionario con los datos del cliente desde la tabla 'DatosClientes'.
            - id_pipedrive: ID del cliente en Pipedrive (si existe).
            - id_registro: ID del registro en la tabla 'DatosClientes'.
            """
        # Construir la consulta SQL para obtener los datos del cliente desde la tabla 'DatosClientes'
        query = f"SELECT * FROM DatosClientes WHERE CardCode = '{codigoCliente}' AND Pais = '{self.pais}'"

        # Conectar a la base de datos
        self.db.connect()
        try:
            # Ejecutar la consulta y obtener el primer registro (asumiendo que solo hay un resultado)
            result = self.db.execute_query(query)[0]

            # Crear un diccionario que contenga los datos relevantes del cliente extraídos de la tabla 'DatosClientes'
            datos_POS = {
                'CardCode': result[1],  # Código del cliente
                'CardName': result[2],  # Nombre del cliente
                'address': result[3],  # Dirección del cliente
                'Municipio': result[5],  # Municipio del cliente
                'Departamento': result[6],  # Departamento del cliente
                'Pais': result[14],  # País del cliente
                'Sector': result[11],  # Sector del cliente
                'Coordenadas': result[13],  # Coordenadas del cliente
                'Vendedor_Asignado': result[15]  # Vendedor asignado al cliente
            }

            # Obtener el ID de Pipedrive y el ID del registro para futuras referencias
            id_pipedrive = result[8]  # ID del cliente en Pipedrive
            id_registro = result[0]  # ID del registro en la tabla 'DatosClientes'

            # Devolver los datos del cliente y los identificadores
            return datos_POS, id_pipedrive, id_registro

        except Exception as e:
            # En caso de error, devolver un mensaje con la descripción del problema
            return f"Error al obtener datos de POS: {str(e)}"

        finally:
            # Desconectar de la base de datos, independientemente de si hubo un error o no
            self.db.disconnect()

    def obtener_datos_vw(self, codigoCliente):
        """
            Función para obtener los datos del cliente desde la vista 'VW_DATOS_CLIENTES' (VW_POS).

            Entradas:
            - codigoCliente: Código del cliente que se quiere buscar en la vista 'VW_DATOS_CLIENTES'.

            Salidas:
            - datos_vw_pos: Diccionario con los datos del cliente desde la vista 'VW_DATOS_CLIENTES'.
            """
        # Construir la consulta SQL para obtener los datos del cliente desde la vista 'VW_DATOS_CLIENTES'
        query2 = f"SELECT * FROM [dbo].[VW_DATOS_CLIENTES_{self.pais}] WHERE CardCode = '{codigoCliente}'"

        # Conectar a la base de datos
        self.db.connect()
        try:
            # Ejecutar la consulta y obtener el primer registro (asumiendo que solo hay un resultado)
            result2 = self.db.execute_query(query2)[0]

            # Crear un diccionario que contenga los datos relevantes del cliente extraídos de la vista
            datos_vw_pos = {
                'CardCode': result2[0],  # Código del cliente
                'CardName': result2[1],  # Nombre del cliente
                'address': result2[2],  # Dirección del cliente
                'Municipio': result2[4],  # Municipio del cliente
                'Departamento': result2[5],  # Departamento del cliente
                'Pais': result2[13],  # País del cliente
                'Sector': result2[10],  # Sector del cliente
                'Coordenadas': result2[12],  # Coordenadas del cliente
                'Vendedor_Asignado': result2[14]  # Vendedor asignado al cliente
            }

            # Devolver los datos obtenidos desde la vista
            return datos_vw_pos

        except Exception as e:
            # En caso de error, devolver un mensaje con la descripción del problema
            return f"Error al obtener datos de VW: {str(e)}"

        finally:
            # Desconectar de la base de datos, independientemente de si hubo un error o no
            self.db.disconnect()

    def obtener_datos_pipedrive(self, id_pipedrive, lista):
        """
            Función para obtener los datos del cliente desde Pipedrive si el cliente existe.

            Entradas:
            - id_pipedrive: ID del cliente en Pipedrive.
            - lista: Diccionario de opciones para la conversión de valores desde Pipedrive.

            Salidas:
            - datos_pipe: Diccionario con los datos del cliente desde Pipedrive.
            """
        try:
            # Obtener los datos de la organización desde Pipedrive utilizando el ID de Pipedrive
            result_pipe = self.pipe.get_organization_id(id_pipedrive).get('data')

            # Crear un diccionario que contenga los datos relevantes del cliente extraídos de Pipedrive
            datos_pipe = {
                'CardCode': result_pipe.get('bd4aa325c2375edc367c1d510faf509422f71a5b'),
                # Código del cliente en Pipedrive
                'CardName': result_pipe.get('name'),  # Nombre del cliente en Pipedrive
                'address': result_pipe.get('address'),  # Dirección del cliente en Pipedrive
                'Municipio': dictionary_invert(lista.get('4025'),
                                               result_pipe.get('99daf5439284d6a809aee36c4d52a53c9826300b')),
                # Municipio del cliente en Pipedrive
                'Departamento': dictionary_invert(lista.get('4024'),
                                                  result_pipe.get('deca3dd694894b2ca93df56db39f66468cb3885d')),
                # Departamento del cliente en Pipedrive
                'Sector': dictionary_invert(lista.get('4023'),
                                            result_pipe.get('8b8121d03ef920b724ffa68b0f6177fdf281ad3f')),
                # Sector del cliente en Pipedrive
                'Coordenadas': result_pipe.get('3ed19788ef9c8ebeaf0f24f58394f67ac784684c'),
                # Coordenadas del cliente en Pipedrive
                'Vendedor_Asignado': dictionary_invert(lista.get('4028'),
                                                       result_pipe.get('fd0f15b9338615a55ca56a3cada567919ec33306')),
                # Vendedor asignado al cliente en Pipedrive
                'Pais': dictionary_invert(lista.get('4026'),
                                          result_pipe.get('2d4edef00aec72dcc0fd1a240f7897fb0eb34465'))
                # País del cliente en Pipedrive
            }

            # Devolver los datos obtenidos desde Pipedrive
            return datos_pipe

        except Exception as e:
            # En caso de error, devolver un mensaje con la descripción del problema
            return f"Error al obtener datos de Pipedrive: {str(e)}"

    def datos_cliente_vw_table_pipedrive(self, codigoCliente):
        """
            Función principal que coordina la obtención y comparación de datos entre POS, VW_POS, y Pipedrive.

            Entradas:
            - codigoCliente: Código del cliente que se quiere validar y obtener datos.

            Salidas:
            - output: Diccionario con el estado del cliente y diferencias entre los datos de POS, VW_POS y Pipedrive (si aplica).
            """
        try:
                # Construir la consulta SQL para validar la existencia del cliente en la tabla
                queryv = f"DECLARE @resultado NVARCHAR(10); EXEC [PipeDrive].[dbo].[sp_ValidadorCliente_{self.pais}] '{codigoCliente}', @resultado OUTPUT; SELECT @resultado AS Resultado;"
                # Conectar a la base de datos y ejecutar la consulta de validación
                self.db.connect()
                validador = self.db.execute_query(queryv)[0][0]

                # Verificar si el cliente existe en la tabla
                if validador == 'Existe':
                    # Obtener datos del cliente desde la tabla 'DatosClientes' (POS)
                    datos_POS, id_pipedrive, id_registro = self.obtener_datos_pos(codigoCliente)

                    # Obtener datos del cliente desde la vista 'VW_DATOS_CLIENTES' (VW_POS)
                    datos_vw_pos = self.obtener_datos_vw(codigoCliente)

                    # Obtener la lista de opciones para la conversión de valores desde una fuente externa
                    lista = get_all_option_for_fields_in_get_all_organization([4025, 4024, 4023, 4028, 4026])

                    # Verificar si el cliente tiene un ID en Pipedrive
                    if id_pipedrive is None:
                        # Si el cliente no existe en Pipedrive, pero sí en la tabla
                        return {
                            'Status': 'No existe en pipedrive, pero si en la tabla',
                            'Diferencia de datos entre POS y VW_POS': datos_vw_pos != datos_POS,
                            # Comparar datos entre POS y VW_POS
                            'datos_POS': datos_POS,  # Datos del cliente desde POS
                            'datos_vw_pos': datos_vw_pos,  # Datos del cliente desde VW_POS
                            'id_registro': id_registro,  # ID del registro en la tabla
                            'lista': lista  # Lista de opciones para la conversión de valores
                        }
                    else:
                        # Si el cliente existe en Pipedrive, obtener los datos desde Pipedrive
                        datos_pipe = self.obtener_datos_pipedrive(id_pipedrive, lista)

                        # Devolver un resumen de las diferencias entre los datos en diferentes fuentes (POS, VW_POS, Pipedrive)
                        return {
                            'Status': 'Si existe en pipedrive y tambien en la tabla',
                            'Diferencia de datos entre POS y pipeDrive': datos_POS != datos_pipe,
                            # Comparar datos entre POS y Pipedrive
                            'Diferencia de datos entre POS y VW_POS': datos_vw_pos != datos_POS,
                            # Comparar datos entre POS y VW_POS
                            'datos_POS': datos_POS,  # Datos del cliente desde POS
                            'datos_vw_pos': datos_vw_pos,  # Datos del cliente desde VW_POS
                            'datos_pipe': datos_pipe,  # Datos del cliente desde Pipedrive
                            'lista': lista,  # Lista de opciones para la conversión de valores
                            'id_pipedrive': id_pipedrive,  # ID del cliente en Pipedrive
                            'id_registro': id_registro  # ID del registro en la tabla
                        }
                else:
                    # Si el cliente no existe en la tabla, devolver un mensaje indicando que no se encontró
                    return {
                        'Status': 'No Existe Cliente en la tabla',
                        'Codigo Del Cliente': codigoCliente,  # Código del cliente
                        'Pais': self.pais  # País del cliente
                    }

        except Exception as e:
            # Manejo de errores generales durante el proceso y devolución de un mensaje con el error
            return {f"El cliente: {codigoCliente} tiene el siguiente error: ": str(e)}

        finally:
            # Desconectar de la base de datos al finalizar la operación
            self.db.disconnect()

    def clientes_por_sector_validador(self, Validador):
        self.db.connect()
        query = f"Select CardCode from DatosClientes Where Pais = '{self.pais}' AND Validador = '{Validador}'"
        result = self.db.execute_query(query)
        return result, len(result)

    def consulta_factura(self, docnum, docentry):
        # Conectar a la base de datos
        self.db.connect()

        # Consulta para obtener información de la factura
        query = (f"SELECT DocNum, Serie, ORD, DetailSum, id_deal, CancelComments, CancelReason, CDESCRIPCION, SlpName "
                 f"FROM DatosProyectos_PipeDrive WHERE DocNum = {docnum} AND DocEntry = {docentry} AND Pais = '{self.pais}'")
        row = self.db.execute_query(query)[0]

        # Construir el número de orden y el tipo de referencia
        order_number = row[1] + str(row[0])
        ref_type = row[2]

        # Ejecutar el procedimiento almacenado para consultar la factura
        query1 = f"EXEC sp_consulta_factura_{self.pais} {order_number}, {ref_type}"
        resultado = self.db.execute_query(query1)[0][0]
        if resultado == 'Sin Factura':
            return resultado
        else:
            valor_facturado = float(resultado)
            valor_cotizacion = float(row[3])

            # Establecer la moneda según el país, asumiendo USD por defecto
            currency = currency_mapping.get(self.pais, 'USD')
            porcentaje = round(valor_facturado * 100 / valor_cotizacion, 2)
            # Crear y devolver el resultado solo si los valores coinciden
            if valor_facturado == valor_cotizacion:
                return {"currency": currency, "value": valor_facturado, 'e98fda1c30bf99bce1876a34e6caa56c540a4e32': porcentaje}
            else:
                return {"currency": currency, "value": valor_facturado, 'e98fda1c30bf99bce1876a34e6caa56c540a4e32': porcentaje}

    def validador_vendedor_asignado(self, SlpCode):
        try:
            self.db.connect()
            query = f"SELECT PipedriveID FROM [PipeDrive].[dbo].[VendedoresConCredenciales] WHERE SlpCode = {SlpCode}"
            row = self.db.execute_query(query)
            if row:
                return True, row[0][0]
            else:
                return False
        except Exception as e:
            print(f"Error al validar el vendedor: {e}")
            return False
        finally:
            self.db.disconnect()

    def validador_vendedor_cotizado(self, UserCode):
        try:
            self.db.connect()
            query = f"SELECT PipedriveID FROM [PipeDrive].[dbo].[VendedoresConCredenciales] WHERE UserCode = '{UserCode}'"
            row = self.db.execute_query(query)
            if row:
                return True, row[0][0]
            else:
                return False
        except Exception as e:
            print(f"Error al validar el vendedor: {e}")
            return False
        finally:
            self.db.disconnect()

    def vendedor_cartera(self, cardcode):
        self.db.connect()
        query = f"Select CardCode from DatosClientes Where Pais = '{self.pais}' AND Validador = '{cardcode}'"
        self.db.execute_query(query)

    def obtener_y_actualizar_datos_pais(self, valores, datos):
        """
        Función que obtiene y actualiza los datos basados en el país del vendedor asignado.

        Args:
            valores (dict): Diccionario con valores relevantes como el 'Vendedor_Asignado'.
            datos (dict): Diccionario que será actualizado con los datos obtenidos.
        """
        match self.pais:
            case "SV":
                query = (f"SELECT SlpName, U_Jefe AS SECTOR FROM [dbo].[vw_RepresentantesVentas_{self.pais}] "
                         f"WHERE SlpName = '{valores.get('Vendedor_Asignado')}'")
                result = self.db.execute_query(query)[0]
                id_dueño = self.obtener_id_vendedor(result[0], result[1])
                datos.update(id_dueño)
            case _:
                query = (f"SELECT SlpName FROM [dbo].[vw_RepresentantesVentas_{self.pais}] "
                         f"WHERE SlpName = '{valores.get('Vendedor_Asignado')}'")
                result = self.db.execute_query(query)[0]
                id_dueño = self.obtener_id_vendedor(result[0], self.pais)
                datos.update(id_dueño)

    def cliente_con_keys_pipedrive(self, valores):
        """
        Esta función procesa los valores de un cliente y mapea las claves correspondientes a los campos de Pipedrive.

        Entrada:
        - valores: Un diccionario que contiene los valores asociados a cada campo del cliente.

        Salida:
        - datos: Un diccionario que contiene los datos mapeados con las claves correspondientes a los campos de Pipedrive.
        """

        # Inicializa el diccionario de datos y el diccionario de valores que no existen en Pipedrive
        datos = {}
        valoresNoExisteCampo = {}
        self.db.connect()
        self.obtener_y_actualizar_datos_pais(valores, datos)

        # Obtiene todas las opciones para los campos específicos en Pipedrive
        lista = get_all_option_for_fields_in_get_all_organization([4025, 4024, 4023, 4028, 4026])
        # Itera sobre cada valor en el diccionario `valores`
        for row in valores:
            valor = valores.get(f'{row}')  # Obtiene el valor asociado a la clave `row`
            keys = datos_cliente.get(f'{row}')  # Obtiene la clave correspondiente del cliente
            datos.update({
                'label': 1
            })
            # Utiliza `match-case` para identificar el campo correspondiente
            match row:
                case "Sector":
                    id_selecto_pipedrive  = lista.get('4023').get(f'{valor}')  # Obtiene el ID del sector en Pipedrive
                    if id_selecto_pipedrive  is None:  # Si el valor no existe en Pipedrive
                        manejar_no_existencia_campo('4023', valor, valoresNoExisteCampo, 'cliente_con_keys_pipedrive')
                    else:  # Si el valor existe, actualiza el diccionario `datos`
                        datos.update({
                            f'{keys}': id_selecto_pipedrive 
                        })


                case "Departamento":
                    id_selecto_pipedrive  = lista.get('4024').get(
                        f'{valor}')  # Obtiene el ID del departamento en Pipedrive
                    if id_selecto_pipedrive  is None:  # Si el valor no existe en Pipedrive
                        manejar_no_existencia_campo('4024', valor, valoresNoExisteCampo, 'cliente_con_keys_pipedrive')
                    else:  # Si el valor existe, actualiza el diccionario `datos`
                        datos.update({
                            f'{keys}': id_selecto_pipedrive 
                        })


                case "Municipio":
                    id_selecto_pipedrive  = lista.get('4025').get(f'{valor}')  # Obtiene el ID del municipio en Pipedrive
                    if id_selecto_pipedrive  is None:  # Si el valor no existe en Pipedrive
                        manejar_no_existencia_campo('4025', valor, valoresNoExisteCampo, 'cliente_con_keys_pipedrive')
                    else:  # Si el valor existe, actualiza el diccionario `datos`
                        datos.update({
                            f'{keys}': id_selecto_pipedrive 
                        })


                case "Vendedor_Asignado":
                    id_selecto_pipedrive  = lista.get('4028').get(
                        f'{valor}')
                    # Obtiene el ID del vendedor asignado en Pipedrive
                    if id_selecto_pipedrive  is None:  # Si el valor no existe en Pipedrive
                        manejar_no_existencia_campo('4028', valor, valoresNoExisteCampo, 'cliente_con_keys_pipedrive')
                    else:  # Si el valor existe, actualiza el diccionario `datos`
                        datos.update({
                            f'{keys}': id_selecto_pipedrive 
                        })


                case "Pais":
                    id_selecto_pipedrive  = lista.get('4026').get(f'{valor}')  # Obtiene el ID del país en Pipedrive
                    if id_selecto_pipedrive  is None:  # Si el valor no existe en Pipedrive
                        manejar_no_existencia_campo('4026', valor, valoresNoExisteCampo, 'cliente_con_keys_pipedrive')
                    else:  # Si el valor existe, actualiza el diccionario `datos`
                        datos.update({
                            f'{keys}': id_selecto_pipedrive 
                        })


                case _:  # Caso por defecto para cualquier otro campo
                    datos.update({
                        f'{keys}': f'{valor}'  # Actualiza el diccionario `datos` con el valor tal cual
                    })

        # Retorna el diccionario `datos` actualizado
        return datos

    def obtener_id_vendedor(self, nombre, seccion=None):
        """
        Obtiene el ID del vendedor asociado con un nombre y, opcionalmente, una sección específica.

        Parámetros:
        - nombre (str): El nombre del vendedor cuyo ID se desea obtener.
        - section (str, opcional): La sección en el archivo de configuración donde se buscará el vendedor.
          Si no se especifica, se considerará que puede buscarse en cualquier sección relevante para el país.

        Retorno:
        - dict: Un diccionario con la clave 'owner_id' y el valor correspondiente al ID del vendedor.
        - str: Mensaje de error si la sección especificada no se encuentra en el archivo de configuración.

        """

        data = {}
        # Crear un objeto ConfigParser para leer el archivo de configuración
        config = configparser.ConfigParser()
        # Leer el archivo de configuración Sectores_SV.ini (dependiendo del país)
        config.read(f'Sectores_{self.pais}.ini')

        # Verificar si existe la sección especificada
        if seccion in config:
            # Buscar el ID del vendedor en la sección específica
            vendedores = config[seccion]
            if nombre in vendedores:
                # Si el nombre del vendedor existe en la sección, se retorna su ID
                data.update({
                    'owner_id': vendedores[nombre]
                })
                return data
            else:
                # Si el nombre no se encuentra, se retorna el ID del jefe de sector correspondiente según el país
                match self.pais:
                    case "SV":
                        data.update({
                            'owner_id': id_jefes_sector_sv.get(f"{seccion}")
                        })
                        return data
                    case "GT":
                        data.update({
                            'owner_id': id_jefes_sector_gt.get(f"{seccion}")
                        })
                        return data
                    case "HN":
                        data.update({
                            'owner_id': id_jefes_sector_hn.get(f"{seccion}")
                        })
                        return data
        else:
            # Si la sección especificada no existe, se retorna un mensaje de error
            return f"La sección '{seccion}' no se encontró en el archivo."