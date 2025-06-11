from flask import Blueprint, jsonify, request, Response
import json

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/list", methods=["GET"])
def list():
    chatId = request.args.get("chatId")
    print("chatId", chatId)
    return jsonify({"code": 200, "message": f"chat lists: {chatId}"})


@chat_bp.route("/ask", methods=["POST"])
def ask():
    data = request.json
    print(data)
    from app.ai.aigc.llm import generate

    def generate_stream():
        for chunk in generate(data.get("query")):
            yield f"data: {json.dumps({'type': 'stream', 'content': chunk})}\n\n"
        yield f"data: {json.dumps({'type': 'end'})}\n\n"

    # 流式接口返回
    return Response(generate_stream(), mimetype="text/event-stream")
