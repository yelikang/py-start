from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    base_url="http://10.5.14.242:8001/v1",
    api_key="dummy-key",
    model_name="DeepSeek-V3-Fast"
)

# 步骤1：问题拆解
decompose_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个问题拆解专家。将复杂问题拆解成3-5个子问题，每个子问题应该是独立可解决的。"),
    ("user", "请将以下问题拆解成子问题：{question}")
])

# 步骤2：子问题解答
solve_subproblem_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业分析师。请详细解答以下子问题，提供具体的分析和推理过程。"),
    ("user", "子问题：{subproblem}\n\n原始问题背景：{original_question}")
])

# 步骤3：整合结论
integrate_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个整合专家。基于所有子问题的解答，整合出最终的完整答案。"),
    ("user", "原始问题：{original_question}\n\n各子问题的解答：\n{sub_answers}\n\n请整合出完整的最终答案：")
])

output_parser = StrOutputParser()

def multi_step_reasoning(question):
    """多步推理深度思考"""
    print("=" * 60)
    print("深度思考结果 - 多步推理法")
    print("=" * 60)
    
    # 步骤1：拆解问题
    print("\n🔍 步骤1：问题拆解")
    print("-" * 30)
    decompose_chain = decompose_prompt | llm | output_parser
    subproblems = decompose_chain.invoke({"question": question})
    print(subproblems)
    
    # 解析子问题（简单按行分割，实际项目中可能需要更复杂的解析）
    subproblem_lines = [line.strip() for line in subproblems.split('\n') if line.strip() and ('.' in line or '?' in line)]
    
    # 步骤2：解答子问题
    print("\n🧠 步骤2：子问题分析")
    print("-" * 30)
    solve_chain = solve_subproblem_prompt | llm | output_parser
    sub_answers = []
    
    for i, subproblem in enumerate(subproblem_lines[:5], 1):  # 限制最多5个子问题
        print(f"\n子问题 {i}: {subproblem}")
        answer = solve_chain.invoke({
            "subproblem": subproblem,
            "original_question": question
        })
        sub_answers.append(f"子问题 {i}: {subproblem}\n解答: {answer}")
        print(f"解答: {answer[:200]}..." if len(answer) > 200 else f"解答: {answer}")
    
    # 步骤3：整合答案
    print("\n🎯 步骤3：整合最终答案")
    print("-" * 30)
    integrate_chain = integrate_prompt | llm | output_parser
    final_answer = integrate_chain.invoke({
        "original_question": question,
        "sub_answers": "\n\n".join(sub_answers)
    })
    print(final_answer)
    
    return {
        "subproblems": subproblem_lines,
        "sub_answers": sub_answers,
        "final_answer": final_answer
    }

# 改进的多步推理（带验证）
def enhanced_multi_step_reasoning(question):
    """增强版多步推理，包含自我验证"""
    print("=" * 60)
    print("深度思考结果 - 增强版多步推理法")
    print("=" * 60)
    
    # 执行基础多步推理
    result = multi_step_reasoning(question)
    
    # 步骤4：自我验证
    print("\n✅ 步骤4：答案验证")
    print("-" * 30)
    
    verify_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个答案验证专家。请检查以下答案是否逻辑一致、完整准确，并提出可能的改进建议。"),
        ("user", "问题：{question}\n\n答案：{answer}\n\n请验证并评估这个答案：")
    ])
    
    verify_chain = verify_prompt | llm | output_parser
    verification = verify_chain.invoke({
        "question": question,
        "answer": result["final_answer"]
    })
    print(verification)
    
    result["verification"] = verification
    return result

if __name__ == '__main__':
    # 测试多步推理
    question = "如何设计一个可持续发展的智慧城市系统？"
    enhanced_multi_step_reasoning(question)