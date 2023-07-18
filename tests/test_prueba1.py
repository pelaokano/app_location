"""
Esta prueba permite verificar si la vista inicial muestra el template index.html.
Tambien verifica que la vista index.html que es devuelta por flask contenga el 
tag h1 lo siguiente <h1>Seguimiento Ubicación</h1>.
"""


def test_vista_index(client, captured_templates):
    response = client.get("/")
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"
    assert response.text.find("<h1>Seguimiento Ubicación</h1>") >= 0
