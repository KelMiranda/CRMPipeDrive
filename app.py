from flask import Flask, render_template, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from telegram.apitelegram import TelegramBot

app = Flask(__name__)

# Variable global para almacenar la fecha de última ejecución
ultima_ejecucion = None

def ejecutar_proceso_cotizaciones():
    global ultima_ejecucion
    pais = ['SV', 'GT', 'HN']
    for row in pais:
        try:
            ct = IngresoDeCotizaciones(f'{row}')
            print(ct.proceso_clientes_dias(1))
            print(ct.cotizaciones_actualizadas())
            print(ct.proceso_cotizaciones_dia(1))
            print(ct.proceso_cotizaciones_pipedrive())
        except Exception as e:
            print(f'Ocurrió un error con el país {row}: {e}')
    bot = TelegramBot(None)
    bot.send_message(1947314689)

    # Actualizar la fecha y hora de la última ejecución
    ultima_ejecucion = datetime.now()

# Ruta principal de la landing page
@app.route('/')
def index():
    global ultima_ejecucion
    fecha_ejecucion = ultima_ejecucion.strftime('%Y-%m-%d %H:%M:%S') if ultima_ejecucion else "No ejecutada aún"
    return render_template('index.html', fecha_ejecucion=fecha_ejecucion)

# Ruta para ejecutar la función manualmente desde el botón
@app.route('/ejecutar')
def ejecutar():
    ejecutar_proceso_cotizaciones()
    return redirect(url_for('index'))

# Función que será ejecutada automáticamente a las 3:00 AM
def tarea_diaria():
    ejecutar_proceso_cotizaciones()

# Configurar APScheduler para ejecutar diariamente
scheduler = BackgroundScheduler()
scheduler.add_job(func=tarea_diaria, trigger="cron", hour=3, minute=0, id='tarea_diaria')
scheduler.start()

# Cerrar el scheduler cuando la aplicación termine
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
