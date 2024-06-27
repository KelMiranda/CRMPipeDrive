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

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/deals', methods=['GET'])
def get_deals():
    # Aquí puedes agregar la lógica para generar o recuperar tus datos
    result = get_all_deals()
    return jsonify(result)
@app.route('/coti')
def home_coti():
    return render_template('coti.html')

@app.route('/cotizaciones', methods=['POST'])
def cotizaciones():
    paises = request.form.getlist('paises')
    results = {}

    for row in paises:
        ct = IngresoDeCotizaciones(row)
        result = ct.cotizaciones_diarias(1)
        result_act = ct.cotizaciones_actualizadas()
        save_json(result, f'Cotizaciones_diarias_{row}')
        save_json(result_act, f'Cotizaciones_actualizadas_{row}')
        results[row] = {
            'cotizaciones_diarias': result,
            'cotizaciones_actualizadas': result_act
        }

    return render_template('result.html', results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
