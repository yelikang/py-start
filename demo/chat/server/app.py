from flask import Flask
from app.api.chat import chat_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# 为整个应用设置前缀
base_url = "/api"

modules = [
    chat_bp
]

for module in modules:
    app.register_blueprint(module, url_prefix= f"{base_url}/{module.name}")

@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
