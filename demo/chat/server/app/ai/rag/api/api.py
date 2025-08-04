from langchain_ollama import ChatOllama
from datetime import datetime
import api_function

"""
tool格式
{
    "name": "get_ages",
    "description": "计算年龄",
    "parameters": {
        "type": "object",
        "properties": {
            "birth_year": {
                "type": "int",
                "description": "出生年份" "如：2006",
            }
        },
        "required": ["birth_year"],
    },
}
"""


api_list = [
    {
        "name": "get_city_weather",
        "description": "城市天气查询接口，会返回指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
            },
            "required": ["city"],
        },
        "meta": {
            "url": "/api/weather/city",
            "method": "get",
        },
    },
    {
        "name": "get_card_info",
        "description": "车辆信息查询接口，返回指定车辆的信息",
        "parameters": {
            "type": "object",
            "properties": {
                "cardNo": {"type": "string", "description": "车牌号"},
            },
            "required": ["cardNo"],
        },
        "meta": {
            "url": "/api/card/info",
            "method": "get",
        },
    },
]


# 构建function calling 模型
def create_fn_model(api_list):
    model = ChatOllama(model="qwen2.5:1.5b", base_url="http://localhost:11434")
    model = model.bind_tools(tools=api_list)
    return model

# 构建文本生成模型
def create_llm_model():
    model = ChatOllama(model="qwen2.5:1.5b", base_url="http://localhost:11434")
    return model


def query_ollama_with_chat(prompt):
    fn_model = create_fn_model(api_list)
    llm_model = create_llm_model()

    # 1. 获取function list
    selected_tool = []
    response = fn_model.stream(prompt)
    for chunk in response:
        for tool in chunk.tool_calls:
            selected_tool.append(tool)

    if len(selected_tool) > 0:
        tools_result = []
        for tool in selected_tool:
            hit_tool = getattr(api_function, tool["name"])
            if hit_tool:
                tools_result.append(hit_tool(tool["args"]))
        # 2. 基于function list，生成response
        combine_prompt = f"""
        你是一个AI助手，根据以下内容，返回用户需要的信息。
        以下是用户需要的信息：{tools_result}
        以下是用户的问题：{prompt}
        """
        response = llm_model.stream(combine_prompt)
        print_response(response)
    else:
        response = llm_model.stream(prompt)
        print_response(response)


def print_response(response):
    for chunk in response:
        print(chunk.content, end="", flush=True)


if __name__ == "__main__":
    query_ollama_with_chat("帮我查询长沙的天气")
    query_ollama_with_chat("帮我查询湘A:17W0W车主信息")


    # 不同的query，执行有时候function_calling不一定会返回，需要更具体的描述
    # query_ollama_with_chat("出生在2005年的人年龄多大了")
    # query_ollama_with_chat("帮我计算一下1992年出生的人今年多少岁")
