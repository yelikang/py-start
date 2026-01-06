from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个历史人物介绍专家"),
    ("user", "请介绍,{input}")
])

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"  # 需要替换为实际可用的模型名
)
# 查看ChatPromoptTemplate实际转换成的内容
# print(prompt.format(input="张飞"))

chain = prompt | llm

response = chain.invoke({"input":'张飞'})
print(response.content)