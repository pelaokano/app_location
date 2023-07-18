import pytest
from main import app as flask_app
from main import coordenadas
from flask import template_rendered


@pytest.fixture()
def app():
    app = flask_app

    app.config.update(
        {
            "TESTING": True,
        }
    )

    with app.app_context():
        coordenadas.agregar([41.374790372054065, 2.125009758191433])
        coordenadas.agregar([41.37492944021627, 2.125303342489873])
        coordenadas.agregar([41.37508778479142, 2.125628120120022])

    yield app

    coordenadas.limpiar()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
