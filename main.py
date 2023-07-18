from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import requests
import time
from threading import Thread
from paquete_estructuras.estructuras import Cola

coordenadas = Cola()
salir = False

app = Flask(__name__)
socketio = SocketIO(app)


def consultar_temperatura():
    global coordenadas
    global salir

    while True:
        if not coordenadas.es_vacia():
            [latitud, longitud] = coordenadas.ultimo()
            url = f"http://api.weatherunlocked.com/api/current/{latitud},{longitud}"
            querystring = {
                "app_id": "88cdbe69",
                "app_key": "d0ff2caabd02ee46c7a0eae8d5276853",
            }
            payload = ""
            response = requests.request("GET", url, data=payload, params=querystring)
            data_filtrada = dict(
                filter(
                    lambda x: x[0] in ["temp_c", "wx_desc", "humid_pct", "windspd_kmh"],
                    dict(response.json()).items(),
                )
            )

            socketio.emit("envio_temperatura", data_filtrada)
        else:
            pass

        time.sleep(5)

        if salir:
            print("salir de hilo")
            break


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recibir", methods=["POST"])
def api_recibe():
    global coordenadas

    if request.method == "POST":
        data = request.get_json()
        coordenadas.agregar([data["latitud"], data["longitud"]])
        socketio.emit("envio_datos", data)

    responses = jsonify(respuesta="correcto")
    responses.status_code = 200

    return responses


@app.route("/ruta", methods=["GET", "POST"])
def api_ruta():
    global coordenadas

    if not coordenadas.es_vacia():
        list_aux = coordenadas.devolver_todo().copy()
    else:
        list_aux = [0]

    if request.method == "POST":
        responses = jsonify(data=list_aux)
        responses.status_code = 200
        return responses


@socketio.on("actualiza")
def actualiza(data):
    global coordenadas

    if data["data"] == "actualiza":
        coordenadas.limpiar()


if __name__ == "__main__":
    hilo1 = Thread(target=consultar_temperatura)
    hilo1.start()
    socketio.run(app, host="192.168.0.164", port=8000, debug=True)
    salir = True
