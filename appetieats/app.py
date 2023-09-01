from flask import Flask
from appetieats.ext import sesssion

from appetieats.ext import database
from appetieats.routes.main import main_bp
from appetieats.routes.menu import menu_bp
from appetieats.routes.auth import auth_bp
from appetieats.routes.admin.admin import admin_bp
from appetieats.routes.admin.settings import settings_bp
from appetieats.ext import commands
from appetieats.ext import configuration
from appetieats.ext import error
from appetieats.routes import restapi

app = Flask(__name__)

commands.init_app(app)
sesssion.init_app(app)
configuration.init_app(app)
database.init_app(app)
error.init_app(app)
restapi.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(menu_bp)
