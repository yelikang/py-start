import os
from openai import OpenAI


# 位置参数，参数位置必须相同
# client = OpenAI(api_key, base_url)


# 关键字参数，参数位置可以不同；增加代码的可读性
client = OpenAI(
    api_key="sk-20ac359475264bd8b170bf90c230d0c7",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="deepseek-r1-distill-qwen-1.5b",
    messages=[
        {"role": "user", "content": "你是谁"},
        {"role": "assistant", "content": "我是 Roy"},
        {"role": "user", "content": "你的工作是什么？"},
        {"role": "assistant", "content": " 我是一个AI助手；请问你的名字是？"},
        {"role": "user", "content": "我叫阿三，是一名软件工程师；你记住了么?"},
    ],
)

print(completion.choices[0].message.content)

# 根目录下运行
# py -m  src.大模型.deepseek-r1
