from flask_socketio import SocketIO, join_room
from flask import session

socketio = SocketIO()


@socketio.on("connect", namespace="/dashboard")
def handle_dashboard_connection():
    restaurant_id = session.get("user_id")
    join_room(restaurant_id)


def init_app(app):
    socketio.init_app(app)
