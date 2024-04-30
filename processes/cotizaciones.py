from database.sql_server_connection import SQLServerDatabase
from time import sleep, time
from processes.deals import get_all_option_for_fields_in_deals
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from processes.organizations import get_all_option_for_fields_in_get_all_organization
from processes.deals import dictionary_invert

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


def notificar_errores(errores):
    # Aquí puedes implementar la lógica para enviar notificaciones con la lista de errores
    print("Enviando notificación de errores:", errores)


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
            errores.append(error_message)

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

    def cotizaciones_del_dia(self, fecha):
        errores = []
        result = []
        query = f"EXEC [dbo].[SP_Cotizaciones_Dia_{self.pais}]'{fecha}'"
        print(query)
        try:
            self.db.connect()
            result = self.db.execute_query(query)
        except Exception as e:
            error_message = f"Error al ejecutar la consulta el error es: {str(e)}"
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
            for row in valores:
                clave_familia = familias_padres.get(row[1])
                if clave_familia is not None:
                    result.update({f"{clave_familia}": float(row[0])})
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
        try:
            id_fields_deals = [12527, 12546, 12521, 12523, 12522, 12524, 12531, 12529, 12534]
            values = get_all_option_for_fields_in_deals(id_fields_deals)
            # Intenta conectarse a la base de datos y ejecutar la consulta
            self.db.connect()
            query = f"EXEC [dbo].[SP_COTIZACIONES_{self.pais}_PYTHON]  {DocNum}, {DocEntry}"
            valores = self.db.execute_query(query)[0]

            def actualizar_data1(valores, values):
                # Casos especiales donde se necesita un "stage_id"
                casos_especiales = ["Presupuesto", "Recotización", "Cierre por cambio de cotizacion"]

                # Configura "data1" según el motivo de pérdida
                if valores[8] in casos_especiales:
                    data1 = {
                        "status": "lost",
                        "lost_reason": values.get('12531').get(valores[8]),
                        "stage_id": 21
                    }
                elif valores[8] == "Venta":
                    # Si no hay que actualizar nada para "Venta", simplemente pasar
                    pass
                else:
                    # Configuración general para los casos de pérdida
                    data1 = {
                        "status": "lost",
                        "lost_reason": values.get('12531').get(valores[8])
                    }
                return data1
            result.update({
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
            })

            if valores[4] == 'Closed':
                result.update(actualizar_data1(valores, values))
                result.update(
                    {
                        f"{datos_cotizacion.get('Comentario_POS')}": valores[7],
                        f"{datos_cotizacion.get('Descripcion_Pos')}": values.get('12531').get(f'{valores[8]}'),
                    }
                )
            # Procesa los resultados de la consulta
            return result, {'id_deal': valores[19]}
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

    def datos_cliente(self, codigoCliente):
        try:
            queryv = f"EXEC [PipeDrive].[dbo].[sp_ValidadorCliente_{self.pais}] '{codigoCliente}'"
            self.db.connect()
            validador = self.db.execute_query(queryv)[0][0]
            if validador == 'Existe':
                query = f"Select * from DatosClientes Where CardCode = '{codigoCliente}' AND Pais = '{self.pais}'"
                query2 = f"Select * from [dbo].[VW_DATOS_CLIENTES_{self.pais}] Where CardCode = '{codigoCliente}'"
                result = self.db.execute_query(query)[0]
                id_pipedrive = result[8]
                id_registro = result[0]
                result2 = self.db.execute_query(query2)[0]
                lista = get_all_option_for_fields_in_get_all_organization([4025, 4024, 4023, 4028, 4026])
                datos_POS = {
                    'CardCode': result[1],
                    'CardName': result[2],
                    'address': result[3],
                    'Municipio': result[5],
                    'Departamento': result[6],
                    'Pais': result[14],
                    'Sector': result[11],
                    'Coordenadas': result[13],
                    'Vendedor_Asignado': result[15]
                }
                datos_vw_pos = {
                    'CardCode': result2[0],
                    'CardName': result2[1],
                    'address': result2[2],
                    'Municipio': result2[4],
                    'Departamento': result2[5],
                    'Pais': result2[13],
                    'Sector': result2[10],
                    'Coordenadas': result2[12],
                    'Vendedor_Asignado': result2[14]
                }

                if id_pipedrive is None:
                    output = {
                        'Status': 'No existe en pipedrive, pero si en la tabla',
                        'Diferencia de datos entre POS y VW_POS': datos_vw_pos != datos_POS,
                        'datos_POS': datos_POS,
                        'datos_vw_pos': datos_vw_pos,
                        'id_registro': id_registro,
                        'lista': lista
                    }
                else:
                    result_pipe = self.pipe.get_organization_id(result[8]).get('data')
                    datos_pipe = {
                        'CardCode': result_pipe.get('bd4aa325c2375edc367c1d510faf509422f71a5b'),
                        'CardName': result_pipe.get('name'),
                        'address': result_pipe.get('address'),
                        'Municipio': dictionary_invert(lista.get('4025'),
                                                       result_pipe.get('99daf5439284d6a809aee36c4d52a53c9826300b')),
                        'Departamento': dictionary_invert(lista.get('4024'),
                                                          result_pipe.get('deca3dd694894b2ca93df56db39f66468cb3885d')),
                        'Sector': dictionary_invert(lista.get('4023'),
                                                    result_pipe.get('8b8121d03ef920b724ffa68b0f6177fdf281ad3f')),
                        'Coordenadas': result_pipe.get('3ed19788ef9c8ebeaf0f24f58394f67ac784684c'),
                        'Vendedor_Asignado': dictionary_invert(lista.get('4028'),
                                                               result_pipe.get(
                                                                   'fd0f15b9338615a55ca56a3cada567919ec33306')),
                        'Pais': dictionary_invert(lista.get('4026'),
                                                  result_pipe.get('2d4edef00aec72dcc0fd1a240f7897fb0eb34465'))
                    }
                    output = {
                        'Status': 'Si existe en pipedrive y tambien en la tabla',
                        'Diferencia de datos entre POS y pipeDrive': datos_POS != datos_pipe,
                        'Diferencia de datos entre POS y VW_POS': datos_vw_pos != datos_POS,
                        'datos_POS': datos_POS,
                        'datos_vw_pos': datos_vw_pos,
                        'datos_pipe': datos_pipe,
                        'lista': lista,
                        'id_pipedrive': result[8]
                    }
                return output
            else:
                output = {
                    'Status': 'No Existe Cliente en la tabla',
                    'Codigo Del Cliente': codigoCliente,
                    'Pais': self.pais,
                }
                return output
        except Exception as e:
            error = {f"El cliente: {codigoCliente} tiene el siguiente error: ": {e}}
            return error
        finally:
            self.db.disconnect()

    def clientes_por_sector_validador(self, Validador):
        self.db.connect()
        query = f"Select CardCode from DatosClientes Where Pais = '{self.pais}' AND Validador = '{Validador}'"
        result = self.db.execute_query(query)
        return result, len(result)