import asyncio
from flask import Flask, render_template, redirect, url_for, request, flash, session
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from telegram.apitelegram import TelegramBot

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Necesario para usar flash messages

# Simulamos un usuario registrado
USUARIO_CORRECTO = 'admin@grupopelsa.com'
PASSWORD_CORRECTA = 'Soy$pectr02024'
# Variable global para almacenar la fecha de última ejecución
ultima_ejecucion = None

# Cambiar esta función a asincrónica
async def ejecutar_proceso_cotizaciones():
    global ultima_ejecucion
    pais = ['SV', 'GT', 'HN']
    for row in pais:
        try:
            print(f"#############################Inicio de los proceso para {row}###################################")
            ct = IngresoDeCotizaciones(f'{row}')
            print(ct.proceso_clientes_dias(1))
            print(f"#####################Finalizando proceso clientes dias para {row}###############################")
            print(ct.cotizaciones_actualizadas())
            print(f"#####################Finalizando cotizaciones actualizadas para {row}###########################")
            print(ct.proceso_cotizaciones_dia(1))
            print(f"#####################Finalizando proceso cotizaciones dias para {row}###########################")
            print(ct.proceso_cotizaciones_pipedrive())
            print(f"#####################Finalizando proceso cotizaciones pipedrive para {row}######################")
            print(f"##############################Finalizando proceso para {row}####################################")
        except Exception as e:
            print(f'Ocurrió un error con el país {row}: {e}')

    # Usar asyncio.sleep en lugar de time.sleep para no bloquear el proceso
    await asyncio.sleep(3)
    print(f"#####################Enviando Notificacion Telegram######################")
    bot = TelegramBot(None)
    bot.send_message(1947314689)

    # Actualizar la fecha y hora de la última ejecución
    ultima_ejecucion = datetime.now()

# Si quieres llamar a esta función en un contexto síncrono (como una vista Flask)
def ejecutar_proceso_cotizaciones_sync():
    asyncio.run(ejecutar_proceso_cotizaciones())

# Ruta principal de la landing page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global ultima_ejecucion
    fecha_ejecucion = ultima_ejecucion.strftime('%Y-%m-%d %H:%M:%S') if ultima_ejecucion else "No ejecutada aún"
    return render_template('index.html', fecha_ejecucion=fecha_ejecucion)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Verificar credenciales
        if email == USUARIO_CORRECTO and password == PASSWORD_CORRECTA:
            session['logged_in'] = True  # Marcar la sesión como iniciada
            return redirect(url_for('index'))
        else:
            # Enviar mensaje de error con flash
            flash('Correo o contraseña incorrecta', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('login'))

# Cambiar esta vista para que sea síncrona y llame a la función asincrónica
@app.route('/ejecutar')
def ejecutar():
    ejecutar_proceso_cotizaciones_sync()
    return redirect(url_for('index'))

# Configuración de tareas programadas
def tarea_diaria():
    ejecutar_proceso_cotizaciones_sync()

scheduler = BackgroundScheduler()
scheduler.add_job(func=tarea_diaria, trigger="cron", hour=3, minute=0, id='tarea_diaria')
scheduler.start()

# Cerrar el scheduler cuando la aplicación termine
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# No necesitas este bloque ya que gunicorn se encargará de ejecutar el servidor
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=False)
