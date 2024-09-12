from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# Variable global para almacenar el estado
ultimo_estado = None

def ejecutar_proceso_cotizaciones():
    global ultimo_estado
    print("Simulación de proceso de cotizaciones ejecutado.")
    # Simula un resultado exitoso o fallido
    resultado = True  # Cambia a True o False para simular el comportamiento
    if resultado:
        ultimo_estado = 'success'
        print("Proceso exitoso.")
    else:
        ultimo_estado = 'error'
        print("Ocurrió un error en el proceso.")
    return resultado

@app.route('/')
def ver_estado():
    # Mostrar la última página de éxito o error según el último estado
    if ultimo_estado == 'success':
        return render_template('success.html')
    elif ultimo_estado == 'error':
        return render_template('error.html')
    else:
        return "No hay un resultado de ejecución aún."

# Función que será ejecutada cada minuto por el scheduler para pruebas
def tarea_diaria():
    ejecutar_proceso_cotizaciones()

# Configurar APScheduler para ejecutar cada minuto (solo para prueba)
scheduler = BackgroundScheduler()
scheduler.add_job(func=tarea_diaria, trigger="interval", minutes=30, id='tarea_diaria')

# Iniciar el scheduler
scheduler.start()

# Cerrar el scheduler cuando la aplicación termine
atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
