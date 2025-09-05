from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"  # 需要替换为实际可用的模型名
)

response = llm.invoke('你好,你的模型版本是什么?')
print(response.content)