from langchain_core.prompts  import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def chat_with_ChatOpenAI():
    llm = ChatOpenAI(
        base_url="http://10.5.14.242:8001/v1",
        api_key="dummy-key",
        model="DeepSeek-V3-Fast"  # 需要替换为实际可用的模型名
    )

    template = ChatPromptTemplate.from_messages([
        ("system", '你是一个笑话生成器，请根据{txt}生成笑话；只生成一个'),
    ])
    # 模板连接到模型
    chain = template | llm
    # 同步调用
    result = chain.invoke({'txt': '小明'})
    print(result.content)
    # 异步/流式输出
    # import asyncio
    # async def generate_joke():
    #     async for token in chain.astream({'txt': '小明'}):
    #         print(token.content, end='', flush=True)

    # asyncio.run(generate_joke())


if __name__ == '__main__':
    chat_with_ChatOpenAI()
