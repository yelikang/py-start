from openai import OpenAI

client = OpenAI(
    api_key="sk-86Qbs8ALJLsGoOZmm2rft1XBVGLIDIFA1uRbztj1dBKhiltY",
    base_url="https://api.moonshot.cn/v1",
)

history = [
    {
        "role": "system",
        "content": "你是kimi，一个前端性能优化专家，擅长分析和优化前端性能问题。",
    }
]


def chat(_query):
    history.append({"role": "user", "content": _query})

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0,
    )
    answer = completion.choices[0].message
    history.append(answer)

    return answer.content


result = chat('你是谁')
print(result)
result = chat('cdn优化有什么方案')
print(result)




