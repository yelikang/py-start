from flask import Blueprint

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/list", methods=["GET"])
def list():
    return "chat list"
