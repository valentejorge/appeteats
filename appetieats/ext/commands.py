from appetieats.ext.database import db
from appetieats.models import Users, RestaurantsData
from werkzeug.security import generate_password_hash


def create_db():
    """create sql database"""
    db.create_all()


def drop_db():
    """drop sql database"""
    db.drop_all()


def populate_users():
    """populate db users with default accounts"""
    data = [
            Users(
                id=1,
                username="dev",
                hash=generate_password_hash("dev"),
                role="restaurant"
            ),
            RestaurantsData(
                id=1,
                name="Python Pizza",
                address="123 Snake St, Pythonville, PY 31415",
                phone="555-PY-314",
                color="#4B8BBE",
                url="python-pizza",
                user_id=1
            )
            # TODO: add products
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Users.query.all()


def hello_commands():
    """says hello"""
    print("hello commands")


def restart_db():
    """restart database"""
    drop_db()
    create_db()
    populate_users()


def init_app(app):
    """add multiple commands in a bulk"""
    for command in [create_db,
                    drop_db,
                    populate_users,
                    hello_commands,
                    restart_db]:
        app.cli.add_command(app.cli.command()(command))
    return app
