def test_devolver_todo(client):
    response = client.post("/ruta")
    assert type(response.json["data"]) is list and len(response.json["data"]) > 0
