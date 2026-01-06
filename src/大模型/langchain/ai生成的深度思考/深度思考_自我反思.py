from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"
)

# 初始回答生成
initial_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业顾问。请针对用户问题提供详细的初始答案。"),
    ("user", "{question}")
])

# 自我反思提示
reflection_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个严格的评判者。请对以下答案进行深入反思，检查：

1. 逻辑一致性：推理过程是否合理
2. 信息完整性：是否遗漏重要信息
3. 准确性：事实是否正确
4. 实用性：建议是否可行
5. 创新性：是否有更好的思路

请用JSON格式回复，包含：
- strengths: 答案的优点（数组）
- weaknesses: 答案的不足（数组）
- missing_aspects: 遗漏的重要方面（数组）
- improvement_suggestions: 具体改进建议（数组）
- confidence_score: 对答案的信心分数（1-10）"""),
    ("user", "问题：{question}\n\n答案：{answer}\n\n请进行深入反思：")
])

# 改进答案生成
improved_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "基于反思结果，请提供一个更完善的改进答案。"),
    ("user", """原问题：{question}

初始答案：{initial_answer}

反思结果：{reflection}

请基于反思提供改进后的答案：""")
])

# 最终验证
final_verification_prompt = ChatPromptTemplate.from_messages([
    ("system", "请对最终改进的答案进行质量评估，给出1-10分的评分并说明理由。"),
    ("user", "问题：{question}\n\n改进答案：{improved_answer}\n\n请评估：")
])

output_parser = JsonOutputParser()
str_parser = JsonOutputParser()

def self_reflection_thinking(question, max_iterations=2):
    """自我反思深度思考"""
    print("=" * 60)
    print("深度思考结果 - 自我反思法")
    print("=" * 60)
    
    # 步骤1：生成初始答案
    print("\n💭 步骤1：生成初始答案")
    print("-" * 40)
    initial_chain = initial_answer_prompt | llm
    initial_response = initial_chain.invoke({"question": question})
    initial_answer = initial_response.content
    print(initial_answer)
    
    current_answer = initial_answer
    
    for iteration in range(max_iterations):
        print(f"\n🔍 步骤{iteration+2}：自我反思 (第{iteration+1}轮)")
        print("-" * 40)
        
        # 反思当前答案
        reflection_chain = reflection_prompt | llm | output_parser
        try:
            reflection = reflection_chain.invoke({
                "question": question,
                "answer": current_answer
            })
            
            print("✅ 优点:")
            for strength in reflection.get("strengths", []):
                print(f"  • {strength}")
            
            print("\n❌ 不足:")
            for weakness in reflection.get("weaknesses", []):
                print(f"  • {weakness}")
            
            print("\n🔍 遗漏方面:")
            for missing in reflection.get("missing_aspects", []):
                print(f"  • {missing}")
            
            print("\n💡 改进建议:")
            for suggestion in reflection.get("improvement_suggestions", []):
                print(f"  • {suggestion}")
            
            confidence = reflection.get("confidence_score", 0)
            print(f"\n📊 信心分数: {confidence}/10")
            
            # 如果信心分数足够高，停止迭代
            if confidence >= 8:
                print(f"\n✨ 信心分数达到{confidence}，停止迭代")
                break
                
        except Exception as e:
            print(f"反思解析失败: {e}")
            reflection = {"improvement_suggestions": ["继续完善答案的逻辑性和完整性"]}
        
        # 生成改进答案
        print(f"\n🔧 步骤{iteration+3}：生成改进答案")
        print("-" * 40)
        improve_chain = improved_answer_prompt | llm
        improved_response = improve_chain.invoke({
            "question": question,
            "initial_answer": initial_answer,
            "reflection": str(reflection)
        })
        current_answer = improved_response.content
        print(current_answer)
    
    # 最终验证
    print(f"\n⭐ 最终步骤：质量验证")
    print("-" * 40)
    verify_chain = final_verification_prompt | llm
    verification = verify_chain.invoke({
        "question": question,
        "improved_answer": current_answer
    })
    print(verification.content)
    
    return {
        "initial_answer": initial_answer,
        "final_answer": current_answer,
        "verification": verification.content
    }

# 简化版自我反思
def simple_self_reflection(question):
    """简化版自我反思"""
    print("=" * 50)
    print("简化版自我反思")
    print("=" * 50)
    
    # 生成答案
    chain = initial_answer_prompt | llm
    response = chain.invoke({"question": question})
    answer = response.content
    
    print("\n📝 初始答案:")
    print(answer)
    
    # 自我质疑
    critique_prompt = ChatPromptTemplate.from_messages([
        ("system", "请对以下答案提出3个批判性问题，帮助改进答案质量。"),
        ("user", "问题：{question}\n答案：{answer}")
    ])
    
    critique_chain = critique_prompt | llm
    critique = critique_chain.invoke({"question": question, "answer": answer})
    
    print("\n❓ 批判性问题:")
    print(critique.content)
    
    # 基于批判改进答案
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "基于这些批判性问题，请提供一个更好的答案。"),
        ("user", "原问题：{question}\n原答案：{answer}\n批判问题：{critique}")
    ])
    
    final_chain = final_prompt | llm
    final_response = final_chain.invoke({
        "question": question,
        "answer": answer,
        "critique": critique.content
    })
    
    print("\n✨ 改进后答案:")
    print(final_response.content)
    
    return final_response.content

if __name__ == '__main__':
    # 测试自我反思
    question = "如何平衡工作与生活？"
    
    print("测试完整版自我反思：")
    self_reflection_thinking(question)
    
    print("\n" + "="*80 + "\n")
    
    print("测试简化版自我反思：")
    simple_self_reflection(question)