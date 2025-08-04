from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

def query_ollama(prompt):
    model = Ollama(model="qwen2.5:1.5b", base_url="http://localhost:11434")

    response = model.stream(prompt)
    for chunk in response:
        print(chunk, end="", flush=True)

def query_ollama_with_chat(prompt):
    model = ChatOllama(model="qwen2.5:1.5b", base_url="http://localhost:11434")

    response = model.stream(prompt)
    for chunk in response:
        additional_kwargs = chunk.additional_kwargs
        response_metadata = chunk.response_metadata

        print(chunk.content, end="", flush=True)

if __name__ == "__main__":
    # prompt = "如果小明有5个梨，然后吃掉2个，再买5个，分给朋友3个，他还有多少个梨？请一步一进行推理并得出结论"
    prompt = "你是谁"
    query_ollama_with_chat(prompt)