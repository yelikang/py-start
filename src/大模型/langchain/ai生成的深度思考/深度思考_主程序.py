"""
深度思考主程序 - 统一调度器
支持多种深度思考方法：
1. 链式思考 (Chain of Thought)
2. 多步推理 (Multi-step Reasoning) 
3. 自我反思 (Self-reflection)
"""

import sys
import os

# 导入各种深度思考方法
try:
    from 深度思考_链式思考 import deep_think_cot
    from 深度思考_多步推理 import multi_step_reasoning, enhanced_multi_step_reasoning
    from 深度思考_自我反思 import self_reflection_thinking, simple_self_reflection
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有深度思考模块都在同一目录下")
    sys.exit(1)

class DeepThinkingOrchestrator:
    """深度思考调度器"""
    
    def __init__(self):
        self.methods = {
            "1": {
                "name": "链式思考 (Chain of Thought)",
                "description": "逐步展示推理过程，适合逻辑分析问题",
                "function": deep_think_cot
            },
            "2": {
                "name": "多步推理 (Multi-step Reasoning)",
                "description": "将复杂问题拆解成子问题逐步解决",
                "function": multi_step_reasoning
            },
            "3": {
                "name": "增强多步推理 (Enhanced Multi-step)",
                "description": "多步推理 + 自我验证",
                "function": enhanced_multi_step_reasoning
            },
            "4": {
                "name": "自我反思 (Self-reflection)",
                "description": "生成答案后进行深度反思和改进",
                "function": self_reflection_thinking
            },
            "5": {
                "name": "简化自我反思 (Simple Self-reflection)",
                "description": "快速版本的自我反思",
                "function": simple_self_reflection
            }
        }
    
    def show_menu(self):
        """显示方法选择菜单"""
        print("🧠 深度思考系统")
        print("=" * 50)
        print("请选择深度思考方法：")
        print()
        
        for key, method in self.methods.items():
            print(f"{key}. {method['name']}")
            print(f"   {method['description']}")
            print()
        
        print("0. 退出程序")
        print("a. 运行所有方法对比")
        print("-" * 50)
    
    def get_user_choice(self):
        """获取用户选择"""
        while True:
            choice = input("请输入您的选择 (0-5 或 a): ").strip().lower()
            
            if choice == "0":
                return "exit"
            elif choice == "a":
                return "all"
            elif choice in self.methods:
                return choice
            else:
                print("❌ 无效选择，请重新输入")
    
    def get_question(self):
        """获取用户问题"""
        print("\n📝 请输入您想要深度思考的问题:")
        question = input().strip()
        
        if not question:
            print("❌ 问题不能为空")
            return self.get_question()
        
        return question
    
    def run_single_method(self, method_key, question):
        """运行单一方法"""
        method = self.methods[method_key]
        print(f"\n🚀 运行方法: {method['name']}")
        print("=" * 80)
        
        try:
            if method_key in ["4"]:  # 自我反思方法需要特殊参数
                result = method["function"](question, max_iterations=1)
            else:
                result = method["function"](question)
            return result
        except Exception as e:
            print(f"❌ 方法执行失败: {e}")
            return None
    
    def run_all_methods(self, question):
        """运行所有方法进行对比"""
        print(f"\n🔄 对比所有深度思考方法")
        print("=" * 80)
        results = {}
        
        # 运行各种方法
        for key, method in self.methods.items():
            print(f"\n{'='*20} {method['name']} {'='*20}")
            try:
                if key == "4":  # 自我反思方法
                    result = method["function"](question, max_iterations=1)
                else:
                    result = method["function"](question)
                results[key] = result
            except Exception as e:
                print(f"❌ {method['name']} 执行失败: {e}")
                results[key] = None
        
        # 显示对比总结
        print(f"\n{'='*20} 方法对比总结 {'='*20}")
        for key, method in self.methods.items():
            status = "✅ 成功" if results.get(key) else "❌ 失败"
            print(f"{method['name']}: {status}")
        
        return results
    
    def run(self):
        """主运行循环"""
        print("欢迎使用深度思考系统！")
        print("这个系统提供多种AI深度思考方法来帮助您分析复杂问题。")
        
        while True:
            self.show_menu()
            choice = self.get_user_choice()
            
            if choice == "exit":
                print("👋 感谢使用深度思考系统！")
                break
            
            question = self.get_question()
            
            if choice == "all":
                self.run_all_methods(question)
            else:
                self.run_single_method(choice, question)
            
            # 询问是否继续
            print("\n" + "="*80)
            continue_choice = input("是否继续使用？(y/n): ").strip().lower()
            if continue_choice not in ["y", "yes", "是", ""]:
                print("👋 感谢使用深度思考系统！")
                break

def main():
    """主函数"""
    orchestrator = DeepThinkingOrchestrator()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"检测到命令行问题: {question}")
        
        # 如果有命令行参数，运行所有方法
        orchestrator.run_all_methods(question)
    else:
        # 交互模式
        orchestrator.run()

if __name__ == "__main__":
    main()