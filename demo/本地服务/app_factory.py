from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    init_app(app)
    return app


def init_app(app):
    from controller import user_controller, role_controller

    controllers = [user_controller, role_controller]

    for controller in controllers:
        controller.init_app(app)
