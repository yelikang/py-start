from openai import OpenAI
import os

api_key = os.getenv("api_key")
base_url = os.getenv("base_url")

print("api_key", api_key)


def generate(query):
    client = OpenAI(api_key=api_key, base_url=base_url)

    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "user", "content": query},
            ],
            stream=True,
        )
        # 流式返回
        # full_content = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                # full_content += content
                print('content', content)
                yield content

        # answer = completion.choices[0].message
    except Exception as e:
        print(e)
        return f"API调用异常: {e}"

    # return answer.content
