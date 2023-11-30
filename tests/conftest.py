import pytest

from appetieats.app import create_app
from appetieats.ext.commands import restart_testing_db
from appetieats.ext.database import db


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")

    with app.app_context():
        db.create_all()
        restart_testing_db('fast')

        yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
