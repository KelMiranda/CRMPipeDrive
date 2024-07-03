from flask import Flask, render_template, request, redirect, url_for,jsonify
from processes.ingresoDeCotizaciones import IngresoDeCotizaciones
from processes.deals import save_json
from processes.deals import DealTable
from pipedrive.users_pipedrive import GetIdUser
from processes.organizations import OrganizationTable
from processes.cotizaciones import Cotizaciones
from database.sql_server_connection import SQLServerDatabase
from processes.proceso_cliente import Cliente
from processes.deals import get_all_deals
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    dato_dia = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', date=dato_dia)


@app.route('/consulta-cotizacion')
def cotizacion():
    return render_template('consultaCoti.html')


@app.route('/cotizaciones', methods=['GET', 'POST'])
def cotizaciones():
    if request.is_json:
        data = request.get_json()
        DocNum = data.get('numero1')
        DocEntry = data.get('numero2')
        pais = data.get('pais')
        print(pais)
        # Aquí puedes procesar los valores como necesites, por ejemplo, guardarlos en una base de datos
        data_cotizacion = Cotizaciones(pais).datos_de_la_cotizacion(DocNum, DocEntry)

        # Devuelve la respuesta en formato JSON
        return jsonify(data_cotizacion)

    return jsonify({"error": "Invalid request"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
