from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个历史人物介绍专家"),
    ("user", "请介绍,{input}")
])

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"  # 需要替换为实际可用的模型名
)

# 构建输出解析器
# output_parser = StrOutputParser()
# 使用json解析器，需告诉模型输出的是json格式；并且没有content属性
output_parser = JsonOutputParser()

chain = prompt | llm | output_parser

response = chain.invoke({"input":'张飞,回答使用answer字段,使用json格式进行回复'})
print(response)