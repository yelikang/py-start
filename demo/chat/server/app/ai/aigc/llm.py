from openai import OpenAI
import os

api_key = os.getenv("api_key")
base_url = os.getenv("base_url")

print("api_key", api_key)


def generate(query, history):
    client = OpenAI(api_key=api_key, base_url=base_url)
    system_prompt = "你是一个专业的前端性能优化助手，擅长分析和优化前端性能问题；当用户问到你是谁的时候，请如实回答。"

    enchance_query = f"""
        # 如果用户问到前端性能优化相关问题，请基于以下维度进行性能分析:
        1. 加载性能
        2. 运行性能
        # 用户问题: {query}
    """

    history.append({"role": "user", "content": enchance_query})
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": system_prompt},
            ]
            + history,
            stream=True,
        )
        # 流式返回
        # full_content = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                # full_content += content
                # print('content', content)
                yield content

        # answer = completion.choices[0].message
    except Exception as e:
        print(e)
        return f"API调用异常: {e}"

    # return answer.content
