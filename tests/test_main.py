from appetieats.models import Users


def test_home(client):
    response = client.get("/")
    assert b'<session id="home" class="home">' in response.data


def test_login(client):
    response = client.get("/login")
    assert b'<a href="/login/customer">' in response.data


def test_customer_register(client, app):
    response = client.post("/register/customer", data={
        "first-name": "test",
        "last-name": "ing",
        "phone": "888-321-321",
        "address": "3 st, 12",
        "zip-code": "987654",
        "reference": "near of a st",
        "username": "testing",
        "password": "123",
        "confirm": "123",
        "agree": True
    })

    with app.app_context():
        assert Users.query.count() == 1
        assert Users.query.filter(Users.id == 1).first().username == "testing"
        assert Users.query.filter(Users.id == 1).first().role == "customer"
        assert b'target URL: <a href="/customer">' in response.data
