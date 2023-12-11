import pytest

from appetieats.app import create_app
from appetieats.ext.commands import restart_db
from appetieats.ext.database import db


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")

    with app.app_context():
        restart_db()

        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
