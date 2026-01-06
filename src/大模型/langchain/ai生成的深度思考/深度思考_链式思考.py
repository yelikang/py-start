from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 链式思考提示词模板
cot_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个深度思考专家。对于用户的问题，请按照以下步骤进行深度思考：

1. 问题分析：首先分析问题的关键要素和背景
2. 思考过程：展示你的逐步推理过程，包括可能的不同角度
3. 关键因素：识别影响答案的关键因素
4. 结论推导：基于以上分析得出最终结论

请用JSON格式回复，包含以下字段：
- analysis: 问题分析
- thinking_process: 思考过程（数组，每个元素是一个思考步骤）  
- key_factors: 关键因素（数组）
- conclusion: 最终结论"""),
    ("user", "请对以下问题进行深度思考：{question}")
])

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"
)

output_parser = JsonOutputParser()
chain = cot_prompt | llm | output_parser

def deep_think_cot(question):
    """使用链式思考进行深度思考"""
    response = chain.invoke({"question": question})
    
    print("=" * 50)
    print("深度思考结果 - 链式思考法")
    print("=" * 50)
    
    print("\n📊 问题分析:")
    print(response.get("analysis", ""))
    
    print("\n🧠 思考过程:")
    for i, step in enumerate(response.get("thinking_process", []), 1):
        print(f"{i}. {step}")
    
    print("\n🔑 关键因素:")
    for factor in response.get("key_factors", []):
        print(f"• {factor}")
    
    print("\n💡 最终结论:")
    print(response.get("conclusion", ""))
    
    return response

if __name__ == '__main__':
    # 测试深度思考
    question = "人工智能对未来教育的影响"
    deep_think_cot(question)