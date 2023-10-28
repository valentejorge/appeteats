"""Module to configure the webhooks"""
from flask_socketio import SocketIO, join_room
from flask import session

socketio = SocketIO()


@socketio.on("connect", namespace="/dashboard")
def handle_dashboard_connection():
    """set a restaurant room"""
    restaurant_id = session.get("user_id")
    join_room(restaurant_id)


def init_app(app):
    """init socketio"""
    socketio.init_app(app)
