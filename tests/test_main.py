from appetieats.models import Users
from appetieats.ext.commands import hello_commands


def test_home(client):
    response = client.get("/")
    assert b'<session id="home" class="home">' in response.data


def test_menu_order(client):
    response = client.post(
        "/login/customer",
        data={"username": "wanteat", "password": "wanteat"})

    response2 = client.post("/python-pizza", data={
        "cart-data": '[{"id": 1, "quantity": 2, "restaurant_id": 1}]'
    })

    response3 = client.get("/customer")
    print(response3)

    assert b'target URL: <a href="/customer">' in response.data
    assert b'target URL: <a href="/python-pizza#cart">' in response2.data
    assert b'Orders' in response3.data


def test_menu(client):
    response = client.get("/python-pizza")
    assert b'<h1 class="mb-0"> Python Pizza </h1>' in response.data


def test_menu_data(client):
    response = client.get("/python-pizza/data")
    assert b'products:' in response.data


def test_login(client):
    response = client.get("/login")
    assert b'<a href="/login/customer">' in response.data


def test_customer_register_login(client, app):
    response = client.post(
        "/register/customer",
        data={
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
        assert Users.query.count() == 3
        assert Users.query.filter(Users.id == 3).first().username == "testing"
        assert Users.query.filter(Users.id == 3).first().role == "customer"
        assert b'target URL: <a href="/customer">' in response.data


def test_commands():
    assert hello_commands() == "hello commands"


def test_error_404(client):
    response = client.get('/invalid-route')
    assert response.status_code == 404
    assert b"<h1>Error 404 &#128560;</h1>" in response.data


def test_error_403(client):
    response = client.get('/admin/dashboard')
    assert response.status_code == 403
    assert b"<h1>Error 403 &#128560;</h1>" in response.data
