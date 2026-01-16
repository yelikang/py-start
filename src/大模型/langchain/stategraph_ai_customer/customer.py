# 智能客服工作流（使用 langgraph StateGraph demo展示）


from typing import TypedDict, List, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from datetime import datetime

# ========== 1. 定义状态结构 ==========
class CustomerServiceState(TypedDict):
    """客服系统的状态定义"""
    # Annotated 用于指定状态更新规则
    conversation_history: Annotated[List[str], operator.add]  # 对话历史（累加）
    customer_query: str                                      # 客户当前查询
    intent: str                                              # 识别出的意图
    needs_escalation: bool                                   # 是否需要转人工
    resolution: str                                          # 解决方案
    agent_notes: List[str]                                   # 客服备注
    step_count: int                                          # 已执行的步骤数
    timestamp: str                                           # 时间戳

# ========== 2. 创建 StateGraph 实例 ==========
workflow = StateGraph(CustomerServiceState)
print("✅ 创建 StateGraph 实例")

# ========== 3. 定义各个节点函数 ==========
def preprocess_node(state: CustomerServiceState) -> dict:
    """预处理节点：初始化状态"""
    print(f"🔵 执行预处理节点 (step {state.get('step_count', 0) + 1})")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "step_count": state.get("step_count", 0) + 1,
        "conversation_history": [f"客户查询: {state['customer_query']}"],
        "agent_notes": ["开始处理客户请求"],
    }

def intent_classification_node(state: CustomerServiceState) -> dict:
    """意图分类节点"""
    print(f"🔵 执行意图分类节点 (step {state['step_count'] + 1})")
    
    query = state["customer_query"].lower()
    
    # 简单的意图识别逻辑
    if "退款" in query or "退钱" in query:
        intent = "refund"
    elif "投诉" in query or "不满意" in query:
        intent = "complaint"
    elif "咨询" in query or "问" in query:
        intent = "inquiry"
    else:
        intent = "general"
    
    return {
        "intent": intent,
        "step_count": state["step_count"] + 1,
        "conversation_history": [f"识别意图: {intent}"],
        "agent_notes": [f"意图分类为: {intent}"]
    }

def refund_handler_node(state: CustomerServiceState) -> dict:
    """退款处理节点"""
    print(f"🔵 执行退款处理节点 (step {state['step_count'] + 1})")
    
    return {
        "resolution": "退款申请已受理，将在3-5个工作日内处理完成",
        "needs_escalation": False,
        "step_count": state["step_count"] + 1,
        "conversation_history": ["处理退款请求"],
        "agent_notes": ["执行标准退款流程"]
    }

def complaint_handler_node(state: CustomerServiceState) -> dict:
    """投诉处理节点"""
    print(f"🔵 执行投诉处理节点 (step {state['step_count'] + 1})")
    
    # 复杂投诉需要人工介入
    if "严重" in state["customer_query"] or "多次" in state["customer_query"]:
        needs_escalation = True
        resolution = "投诉升级处理中"
    else:
        needs_escalation = False
        resolution = "投诉已记录，24小时内回复"
    
    return {
        "resolution": resolution,
        "needs_escalation": needs_escalation,
        "step_count": state["step_count"] + 1,
        "conversation_history": ["处理投诉请求"],
        "agent_notes": [f"投诉处理: {'需人工介入' if needs_escalation else '自动处理'}"]
    }

def human_agent_node(state: CustomerServiceState) -> dict:
    """人工客服节点"""
    print(f"🔵 执行人工客服节点 (step {state['step_count'] + 1})")
    
    return {
        "resolution": "人工客服已接入，正在为您处理",
        "step_count": state["step_count"] + 1,
        "conversation_history": ["转接人工客服"],
        "agent_notes": ["人工客服接手处理"]
    }

def finalize_node(state: CustomerServiceState) -> dict:
    """最终处理节点"""
    print(f"🔵 执行最终处理节点 (step {state['step_count'] + 1})")
    
    summary = f"处理完成。结果: {state['resolution']}。步骤数: {state['step_count']}"
    
    return {
        "conversation_history": [summary],
        "agent_notes": ["流程结束"],
        "step_count": state["step_count"] + 1
    }

# ========== 4. 添加节点到图中 ==========
print("📌 添加节点到 StateGraph...")
workflow.add_node("preprocess", preprocess_node)
workflow.add_node("classify_intent", intent_classification_node)
workflow.add_node("handle_refund", refund_handler_node)
workflow.add_node("handle_complaint", complaint_handler_node)
workflow.add_node("human_agent", human_agent_node)
workflow.add_node("finalize", finalize_node)

# ========== 5. 定义边和路由逻辑 ==========
print("🔄 设置节点连接和路由...")

# 设置入口点
workflow.set_entry_point("preprocess")

# 添加边（固定顺序）
workflow.add_edge("preprocess", "classify_intent")

# 条件路由：根据意图选择处理路径
def route_by_intent(state: CustomerServiceState) -> str:
    """根据意图路由到不同节点"""
    intent = state["intent"]
    print(f"🔄 路由决策: intent={intent}")
    
    if intent == "refund":
        return "handle_refund"
    elif intent == "complaint":
        return "handle_complaint"
    else:
        return "finalize"  # 简单咨询直接结束

workflow.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {
        "handle_refund": "handle_refund",
        "handle_complaint": "handle_complaint",
        "finalize": "finalize"
    }
)

# 从退款处理到最终节点
workflow.add_edge("handle_refund", "finalize")

# 条件路由：投诉处理后判断是否需要人工介入
def check_escalation(state: CustomerServiceState) -> str:
    """检查是否需要人工介入"""
    if state.get("needs_escalation", False):
        print("🔄 路由决策: 需要人工介入")
        return "human_agent"
    else:
        print("🔄 路由决策: 不需要人工介入")
        return "finalize"

workflow.add_conditional_edges(
    "handle_complaint",
    check_escalation,
    {
        "human_agent": "human_agent",
        "finalize": "finalize"
    }
)

# 人工处理后到最终节点
workflow.add_edge("human_agent", "finalize")

# 最终节点到结束
workflow.add_edge("finalize", END)

# ========== 6. 编译工作流 ==========
print("🔧 编译工作流...")
app = workflow.compile()

# ========== 7. 可视化工作流 ==========
try:
    from IPython.display import Image, display
    # 生成流程图（需要graphviz）
    image_data = app.get_graph().draw_mermaid_png()
    display(Image(image_data))
except Exception as e:
    print(f"📊 工作流结构: {e}")
    print("preprocess → classify_intent → {handle_refund, handle_complaint, finalize}")
    print("handle_refund → finalize")
    print("handle_complaint → {human_agent, finalize}")
    print("human_agent → finalize → END")

# ========== 8. 执行工作流 ==========
print("\n" + "="*50)
print("🚀 开始执行工作流")
print("="*50)

# 测试用例1：退款请求
print("\n📋 测试用例1: 退款请求")
initial_state = {
    "customer_query": "我要申请退款",
    "conversation_history": [],
    "intent": "",
    "needs_escalation": False,
    "resolution": "",
    "agent_notes": [],
    "step_count": 0,
    "timestamp": ""
}

print(f"📥 初始状态: query='{initial_state['customer_query']}'")
result1 = app.invoke(initial_state)
print(f"📤 最终结果: {result1['resolution']}")
print(f"📈 执行步骤: {result1['step_count']}步")
print(f"📝 对话历史: {result1['conversation_history']}")

# 测试用例2：严重投诉
# print("\n" + "="*50)
# print("📋 测试用例2: 严重投诉请求")
# initial_state2 = {
#     "customer_query": "我要投诉，你们的产品有严重质量问题！",
#     "conversation_history": [],
#     "intent": "",
#     "needs_escalation": False,
#     "resolution": "",
#     "agent_notes": [],
#     "step_count": 0,
#     "timestamp": ""
# }

# print(f"📥 初始状态: query='{initial_state2['customer_query']}'")
# result2 = app.invoke(initial_state2)
# print(f"📤 最终结果: {result2['resolution']}")
# print(f"📈 执行步骤: {result2['step_count']}步")
# print(f"📝 对话历史: {result2['conversation_history']}")

# ========== 9. 查看完整执行链路 ==========
# print("\n" + "="*50)
# print("🔍 详细执行链路分析")
# print("="*50)

# def trace_execution(state_history):
#     """追踪执行链路"""
#     print("\n执行路径追踪:")
#     for i, (node, state) in enumerate(state_history):
#         print(f"步骤{i+1}: {node}")
#         print(f"  状态: intent={state.get('intent', '')}, "
#               f"step={state.get('step_count', 0)}, "
#               f"resolution={state.get('resolution', '未设置')}")

# # 获取执行历史（在真实环境中可以通过配置获取）
# print("\n用例1执行链路:")
# print("preprocess → classify_intent → handle_refund → finalize")
# print("\n用例2执行链路:")
# print("preprocess → classify_intent → handle_complaint → human_agent → finalize")