from flask import Blueprint, jsonify, request, Response
import json
import time
import sys
chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/list", methods=["GET"])
def list():
    chatId = request.args.get("chatId")
    print("chatId", chatId)
    return jsonify({"code": 200, "message": f"chat lists: {chatId}"})


@chat_bp.route("/ask", methods=["POST"])
def ask():
    data = request.json
    from app.ai.aigc.llm import generate

    def generate_stream():
        for chunk in generate(data.get("query"), data.get("history", [])):
            yield f"data: {json.dumps({'type': 'stream', 'content': chunk}, ensure_ascii=False)}\n\n"
            # time.sleep(1)
        yield f"data: {json.dumps({'type': 'end'}, ensure_ascii=False)}\n\n"

    # 流式接口返回
    # 设置响应头确保不缓冲
    response = Response(generate_stream(), mimetype="text/event-stream")
    return response


# @chat_bp.route("/ask", methods=["GET"])
# def ask():
#     print("ask", request.args)
#     query = request.args.get("query")
    
#     from app.ai.aigc.llm import generate
#     def generate_stream():
#         for chunk in generate(query):
#             yield f"data: {json.dumps({'type': 'stream', 'content': chunk}, ensure_ascii=False)}\n\n"
#         yield f"data: {json.dumps({'type': 'end'}, ensure_ascii=False)}\n\n"

#     # 流式接口返回
#     # 设置响应头确保不缓冲
#     response = Response(generate_stream(), mimetype="text/event-stream")
#     response.headers['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
#     response.headers['pragma'] = 'no-cache'
#     response.headers['X-Accel-Buffering'] = 'no'
#     response.headers['Expires'] = '0'
#     response.headers['Connection'] = 'keep-alive'
    
#     return response