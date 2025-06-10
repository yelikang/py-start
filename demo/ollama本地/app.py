import requests
import json

def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": True  # 启用流式输出
    }
    
    # 使用stream=True参数来获取流式响应
    response = requests.post(url, json=data, stream=True)
    
    # 处理流式响应
    for line in response.iter_lines():
        if line:
            # 解析JSON响应
            json_response = json.loads(line)
            # 获取响应文本
            response_text = json_response.get("response", "")
            # 打印响应文本，不换行
            print(response_text, end="", flush=True)
            
            # 如果响应结束，打印换行
            if json_response.get("done", False):
                print()

if __name__ == "__main__":
    prompt = "你是谁"
    query_ollama(prompt)