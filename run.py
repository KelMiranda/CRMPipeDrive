# ----------- PARCHEO PARA EVENTLET (ESTO VA PRIMERO) ----------
import eventlet
eventlet.monkey_patch()

# ----------- IMPORTAR DESPUÉS DE MONKEY_PATCH -----------------
from app import app, socketio

# ----------- INICIAR SERVIDOR ---------------------------------
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
