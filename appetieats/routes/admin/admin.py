from flask import Blueprint, render_template

from appetieats.ext.helper.register_tools import login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin")
@login_required("restaurant")
def admin():
    return render_template("admin/admin.html")


@admin_bp.route("/admin/dashboard")
@login_required("restaurant")
def dashboard():
    return render_template("admin/dashboard.html")


@admin_bp.route("/admin/settings")
@login_required("restaurant")
def settings():
    return render_template("admin/settings.html")


def init_app(app):
    app.register_blueprint(admin_bp)
