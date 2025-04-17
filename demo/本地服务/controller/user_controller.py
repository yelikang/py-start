from flask import Flask, Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/list')
def userList():
    return 'userList'
def init_app(app: Flask):
    app.register_blueprint(bp)
    print('user_controller.py')