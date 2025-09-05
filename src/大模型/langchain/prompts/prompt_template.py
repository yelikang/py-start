from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# 直接构建提示模板
# prompt = PromptTemplate(
#     input_variables=["input"],
#     template="你是一个历史人物介绍专家,\n,请介绍{input}",
# )


# 使用from_template格式化生成提示模板 
prompt = PromptTemplate.from_template("你是一个历史人物介绍专家,\n,请介绍{input}")

print(prompt)
print('-'*20)
print(prompt.format(input="张飞"))

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"  # 需要替换为实际可用的模型名
)

# 调用方式1: 提示词 + llm
# chain = prompt | llm
# response = chain.invoke({"input":'张飞'})
# print(response.content)

# 调用方式2: prompt先格式化为具体的提示词、再使用llm
text = prompt.format(input="张飞")
response = llm.invoke(text)
print(response.content)
