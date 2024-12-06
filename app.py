import time
from time import sleep

from flask import Flask, render_template, jsonify
from datetime import datetime
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from pytz import timezone
from database.sql_server_connection import SQLServerDatabase
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# Configuración de la base de datos
db = SQLServerDatabase("SERVER", "DATABASE", "USERNAME_", "PASSWORD")
db.connect()

# Función para ejecutar el procedimiento almacenado
def ejecutar_procedimiento(id_usuario, fecha):
    time.sleep(0.5)  # Simula un pequeño retraso
    try:
        query = f"EXEC RegistrarConexion @UserId = {id_usuario}, @LastLogin = '{fecha}'"
        db.execute_query(query, return_results=False)
        print(f"Procedimiento almacenado ejecutado para usuario {id_usuario}.")
    except Exception as e:
        print(f"Error al ejecutar el procedimiento almacenado: {e}")
    finally:
        if not db.is_connected():
            db.connect()

# Lógica centralizada para procesar usuarios
def procesar_usuarios():
    """
    Consulta usuarios desde Pipedrive, procesa sus datos, y ejecuta el procedimiento almacenado.
    """
    print("Procesando usuarios...")
    usuarios = PipedriveAPI('Token').get_all_user()

    if not usuarios:
        print("No se encontraron usuarios para procesar.")
        return []

    data = usuarios.get("data", [])
    utc = timezone('UTC')
    local_tz = timezone('America/El_Salvador')
    now_local = datetime.now(local_tz)

    for usuario in data:
        time.sleep(1)
        last_login = usuario.get('last_login')
        if last_login:
            # Convertir la hora de UTC a la hora local
            utc_time = utc.localize(datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S'))
            local_time = utc_time.astimezone(local_tz)
            last_login_local = local_time.strftime('%Y-%m-%d %H:%M:%S')
            usuario['last_login'] = last_login_local

            # Ejecutar procedimiento almacenado
            ejecutar_procedimiento(usuario.get('id'), last_login_local)

            # Calcular los días desde la última conexión
            days_since_last_login = (now_local - local_time).days
            usuario['days_since_last_login'] = days_since_last_login
        else:
            usuario['days_since_last_login'] = None

    # Ordenar por última conexión
    sorted_data = sorted(data, key=lambda x: x.get('last_login', ''), reverse=True)
    return sorted_data

# Programador de tareas con APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=procesar_usuarios, trigger="interval", minutes=10)
scheduler.start()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hora-servidor')
def hora_servidor():
    # Retorna la hora actual del servidor en formato JSON
    return jsonify({'hora_servidor': datetime.now().strftime('%H:%M:%S')})

@app.route('/usuarios', methods=['GET'])
def get_users():
    """
    Endpoint que devuelve los usuarios procesados en formato JSON.
    """
    try:
        usuarios = procesar_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        print(f"Error al procesar usuarios: {e}")
        return jsonify({"error": "No se pudieron obtener los usuarios."}), 500

@app.route('/usuarios-page')
def usuarios_page():
    """
    Renderiza la página que contiene la tabla de usuarios con AJAX.
    """
    return render_template('usuarios.html')

# Asegura el apagado limpio del programador al cerrar la app
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: db.disconnect())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
