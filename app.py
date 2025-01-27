import time
import logging
from flask import Flask, render_template, jsonify
from datetime import datetime
from pipedrive.pipedrive_api_conecction import PipedriveAPI
from pytz import timezone
from database.sql_server_connection import SQLServerDatabase
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de la base de datos
db = SQLServerDatabase("SERVER", "DATABASE", "USERNAME_", "PASSWORD")
db.connect()

def ejecutar_procedimiento(id_usuario, fecha):
    """Ejecuta un procedimiento almacenado en la base de datos."""
    try:
        query = f"EXEC RegistrarConexion @UserId = {id_usuario}, @LastLogin = '{fecha}'"
        db.execute_query(query, return_results=False)
        print(f"Procedimiento almacenado ejecutado para usuario {id_usuario}.")
    except Exception as e:
        logging.error(f"Error al ejecutar el procedimiento almacenado: {e}")
        db.reconnect()

def procesar_usuarios():
    """Consulta usuarios desde Pipedrive, procesa sus datos y ejecuta el procedimiento almacenado."""
    try:
        usuarios = PipedriveAPI('Token').get_all_user()

        if not usuarios:
            logging.info("No se encontraron usuarios para procesar.")
            return []

        data = usuarios.get("data", [])
        utc = timezone('UTC')
        local_tz = timezone('America/El_Salvador')
        now_local = datetime.now(local_tz)
        historico =[]
        for usuario in data:
            last_login = usuario.get('last_login')
            if last_login:
                utc_time = utc.localize(datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S'))
                local_time = utc_time.astimezone(local_tz)
                last_login_local = local_time.strftime('%Y-%m-%d %H:%M:%S')
                usuario['last_login'] = last_login_local
                historico.append({
                    'id_usuarios': usuario.get('id'),
                    'fecha': last_login_local,
                })
                #ejecutar_procedimiento(usuario.get('id'), last_login_local)
                days_since_last_login = (now_local - local_time).days
                usuario['days_since_last_login'] = days_since_last_login
            else:
                usuario['days_since_last_login'] = None
        sorted_data = sorted(data, key=lambda x: x.get('last_login') or '', reverse=True)
        return sorted_data, historico
    except Exception as e:
        logging.error(f"Error al procesar usuarios: {e}")
        return []

def procesando_usuario_base():
    try:
        print("#############Iniciando Procesando usuarios...##############")
        datos = procesar_usuarios()
        for usuario in datos[1]:
            print(usuario)
            ejecutar_procedimiento(usuario['id_usuarios'], usuario['fecha'])  # Clave corregida
        print("#############Finalizando Procesando usuarios...##############")
    except Exception as e:
        logging.error(f"Error al procesar usuarios: {e}")


scheduler = BackgroundScheduler()
scheduler.add_job(func=procesando_usuario_base, trigger="interval", minutes=10)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hora-servidor')
def hora_servidor():
    return jsonify({'hora_servidor': datetime.now().strftime('%H:%M:%S')})

@app.route('/usuarios', methods=['GET'])
def get_users():
    try:
        usuarios = procesar_usuarios()
        return jsonify(usuarios[0])
    except Exception as e:
        logging.error(f"Error al procesar usuarios: {e}")
        return jsonify({"error": "No se pudieron obtener los usuarios."}), 500

@app.route('/usuarios-page')
def usuarios_page():
    return render_template('usuarios.html')

atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: db.disconnect())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
