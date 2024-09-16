import random
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from processes.ingresoDeCotizaciones import log_error

# Cargar las variables desde el archivo .env
load_dotenv()


class TelegramBot:
    def __init__(self, token=None):
        # Si no se pasa el token como parámetro, se cargará desde el archivo .env
        if token is None:
            token = os.getenv('TELEGRAM_BOT_TOKEN')

        if token is None:
            raise ValueError("No se ha proporcionado un token de Telegram.")

        self.token = token
        self.api_url = f"https://api.telegram.org/bot{self.token}"

        # Diccionario de mensajes
        self.mensajes_exito = {
            1: "El proceso ha finalizado con éxito.",
            2: "Todo ha salido como se esperaba, proceso completado.",
            3: "¡Éxito! El proceso se ha ejecutado correctamente.",
            4: "Proceso terminado sin inconvenientes.",
            5: "La operación se completó exitosamente.",
            6: "El proceso fue ejecutado con éxito.",
            7: "¡Todo listo! Proceso completado.",
            8: "El sistema ha procesado la tarea con éxito.",
            9: "El proceso finalizó sin errores.",
            10: "¡Misión cumplida! El proceso ha sido un éxito.",
            11: "Se ha completado correctamente el proceso.",
            12: "Proceso finalizado sin ningún contratiempo.",
            13: "Todo salió bien, el proceso ha concluido.",
            14: "El proceso se realizó correctamente.",
            15: "Se completó el proceso con éxito.",
            16: "La operación se llevó a cabo sin problemas.",
            17: "El sistema ha completado el proceso exitosamente.",
            18: "Todo ha salido bien, proceso finalizado.",
            19: "¡Proceso exitoso! Todo ha terminado sin problemas.",
            20: "Proceso concluido satisfactoriamente.",
            21: "El proceso ha sido completado con éxito.",
            22: "Se ha llevado a cabo el proceso sin dificultades.",
            23: "Proceso exitoso, todo está en orden.",
            24: "El sistema ha terminado el proceso sin errores.",
            25: "¡Éxito total! El proceso ha finalizado correctamente.",
            26: "El proceso se completó sin ningún inconveniente.",
            27: "Todo ha salido de acuerdo al plan, proceso exitoso.",
            28: "El proceso ha sido realizado con éxito.",
            29: "¡Proceso completado con éxito y sin errores!",
            30: "La tarea ha finalizado exitosamente."
        }

        # Lista para llevar registro de los mensajes enviados
        self.mensajes_enviados = []

    def obtener_mensaje_unico(self):
        """
        Obtiene un mensaje de éxito que no se haya enviado aún. Si todos los mensajes han sido
        enviados, se restablece la lista.
        """
        # Si ya se han enviado todos los mensajes, restablecer la lista
        if len(self.mensajes_enviados) == len(self.mensajes_exito):
            self.mensajes_enviados = []

        # Obtener un mensaje que no haya sido enviado
        mensaje = None
        while not mensaje:
            key = random.randint(1, len(self.mensajes_exito))
            if key not in self.mensajes_enviados:
                mensaje = self.mensajes_exito[key]
                self.mensajes_enviados.append(key)

        return mensaje

    def send_message(self, chat_id):
        """
        Envía un mensaje único de éxito a un chat específico de Telegram, incluyendo la hora del envío.

        :param chat_id: El ID del chat (puede ser un chat individual o un grupo)
        """
        mensaje = self.obtener_mensaje_unico()

        # Obtener la hora actual
        hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Agregar la hora al mensaje
        mensaje_con_hora = f"{mensaje}\n\nHora de envío: {hora_actual}"

        # URL de la API de Telegram
        url = f"{self.api_url}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': mensaje_con_hora
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Levanta una excepción si la respuesta no es 200 OK
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Error al enviar mensaje: {e}"
            log_error(error_message)
            return None
