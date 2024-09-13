from telegram import Bot
import os
from dotenv import load_dotenv
import requests


load_dotenv()
# Tu token del bot y chat ID
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = 1947314689

# Crear instancia del bot
bot = Bot(token=bot_token)

def enviar_mensaje_telegram(mensaje):
    bot.send_message(chat_id=chat_id, text=mensaje)
    print("Mensaje enviado a Telegram.")

# Llama a la función para enviar una notificación
enviar_mensaje_telegram("Este es un mensaje de prueba desde Python a Telegram.")
