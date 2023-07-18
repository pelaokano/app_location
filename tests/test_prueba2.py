"""
Esta prueba permite agregar una coordenada a la variable coordenadas del modelo
lo anterior mediante el envio de una petición post acompañada de un json con 
los valores de la longitud, latitud y dirección. Se verifica que la url responda
con un codigo 200 y con un json que contiene la palabra correcto
"""


def test_json_data(client):
    ubicaciones = {
        "longitud": "2.125009758191433",
        "latitud": "41.374790372054065",
        "direccion": "barcelo s/n",
    }

    response = client.post("/recibir", json=ubicaciones)
    assert response.status_code == 200 and response.json["respuesta"] == "correcto"
