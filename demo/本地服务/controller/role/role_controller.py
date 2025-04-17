from flask import Flask, Blueprint

bp = Blueprint("role", __name__, url_prefix="/role")


@bp.route("/list")
def roleList():
    return "roleList"


def init_app(app: Flask):
    app.register_blueprint(bp)
    print("user_controller.py")

roleList()