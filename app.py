import time
import socket
import logging
import atexit
import dns.resolver
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone

from pipedrive.pipedrive_api_conecction import PipedriveAPI
from database.sql_server_connection import SQLServerDatabase
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from telegram.apitelegram import TelegramBot

# ----------- CONFIGURACIÓN FLASK + SOCKETIO -------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# ----------- LOGGING ------------------------------------------
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ----------- CONEXIÓN A BASE DE DATOS -------------------------
db = SQLServerDatabase("SERVER", "DATABASE", "USERNAME_", "PASSWORD")
db.connect()

# ----------- UTILIDAD DE LOG ----------------------------------
def enviar_log(mensaje):
    timestamp = datetime.now().strftime('%H:%M:%S')
    mensaje_final = f"[{timestamp}] {mensaje}"
    print("🔥 EMITIENDO LOG:", mensaje_final)
    socketio.emit('log_event', {'mensaje': mensaje_final})

@socketio.on('connect')
def handle_connect():
    print("🧲 Cliente conectado vía WebSocket")
    enviar_log("🧲 Cliente WebSocket conectado.")

# ----------- FUNCIONES DE NEGOCIO -----------------------------
def ejecutar_procedimiento(id_usuario, fecha):
    try:
        query = f"EXEC RegistrarConexion @UserId = {id_usuario}, @LastLogin = '{fecha}'"
        db.execute_query(query, return_results=False)
        enviar_log(f"🗂 Procedimiento ejecutado para usuario {id_usuario}")
    except Exception as e:
        enviar_log(f"❌ Error en procedimiento para usuario {id_usuario}: {e}")
        logging.error(str(e))

def procesar_usuarios():
    try:
        usuarios = PipedriveAPI('Token').get_all_user()
        if not usuarios:
            enviar_log("⚠️ No se encontraron usuarios para procesar.")
            return []

        data = usuarios.get("data", [])
        utc = timezone('UTC')
        local_tz = timezone('America/El_Salvador')
        now_local = datetime.now(local_tz)
        historico = []

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
                usuario['days_since_last_login'] = (now_local - local_time).days
            else:
                usuario['days_since_last_login'] = None

        return sorted(data, key=lambda x: x.get('last_login') or '', reverse=True), historico
    except Exception as e:
        enviar_log(f"❌ Error al procesar usuarios: {e}")
        logging.error(str(e))
        return []

def procesando_usuario_base():
    try:
        enviar_log("📋 Iniciando procesamiento de usuarios...")
        datos = procesar_usuarios()
        for usuario in datos[1]:
            ejecutar_procedimiento(usuario['id_usuarios'], usuario['fecha'])
        enviar_log("✅ Procesamiento finalizado.")
        db.log_error('procesando_usuario_base', "procesado", "proceso con exito")
    except Exception as e:
        enviar_log(f"❌ Error general: {e}")
        logging.error(str(e))

def procesando_usuario_base_socketio():
    with app.app_context():
        procesando_usuario_base()

def procesar_cotizaciones_por_pais():
    paises = ['SV', 'GT', 'HN']
    resultados = []
    enviar_log("🧪 Iniciando procesamiento por país...")

    for row in paises:
        try:
            enviar_log(f"🟢 Procesando {row}")
            ct = IngresoDeCotizaciones(f'{row}')
            clientes_dias = ct.proceso_clientes_dias(1)
            cotizaciones_actualizadas = ct.cotizaciones_actualizadas()
            cotizaciones_dia = ct.proceso_cotizaciones_dia(1)
            cotizaciones_pipedrive = ct.proceso_cotizaciones_pipedrive()

            enviar_log(f"✅ {row} completado.")
            resultados.append({
                'pais': row,
                'clientes_dias': clientes_dias,
                'cotizaciones_actualizadas': cotizaciones_actualizadas,
                'cotizaciones_dia': cotizaciones_dia,
                'cotizaciones_pipedrive': cotizaciones_pipedrive,
            })
        except Exception as e:
            enviar_log(f"❌ Error con {row}: {e}")
            resultados.append({'pais': row, 'error': str(e)})

    bot = TelegramBot(None)
    bot.send_message(1947314689)
    enviar_log("✅ Todos los procesos completados.")
    return resultados

def procesar_cotizaciones_por_pais_socketio():
    with app.app_context():
        procesar_cotizaciones_por_pais()

# ----------- SCHEDULER ----------------------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(func=procesando_usuario_base_socketio, trigger="interval", minutes=10)
scheduler.start()

# ----------- RUTAS FLASK --------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/procesar-cotizaciones')
def procesar_cotizaciones():
    try:
        enviar_log("📡 Iniciando procesamiento en segundo plano...")
        socketio.start_background_task(procesar_cotizaciones_por_pais_socketio)
        return jsonify({'status': 'iniciado'})
    except Exception as e:
        enviar_log(f"❌ Error al iniciar proceso: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/hora-servidor')
def hora_servidor():
    return jsonify({'hora_servidor': datetime.now().strftime('%H:%M:%S')})

@app.route('/usuarios')
def get_users():
    try:
        usuarios = procesar_usuarios()
        return jsonify(usuarios[0])
    except Exception as e:
        enviar_log(f"❌ Error al obtener usuarios: {e}")
        return jsonify({"error": "No se pudieron obtener los usuarios."}), 500

@app.route('/usuarios-page')
def usuarios_page():
    return render_template('usuarios.html')

@app.route('/probar-log')
def probar_log():
    try:
        enviar_log("🧪 Iniciando prueba de resolución DNS...")
        ip = dns.resolver.resolve("api.pipedrive.com")[0].to_text()
        enviar_log(f"📡 IP Resuelta: {ip}")
        return jsonify({"status": "ok", "ip": ip})
    except Exception as e:
        mensaje_error = f"❌ Error resolviendo DNS: {e}"
        enviar_log(mensaje_error)
        print(mensaje_error)
        return jsonify({"error": str(e)}), 500

# ----------- SHUTDOWN LIMPIO ----------------------------------
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: db.disconnect())
