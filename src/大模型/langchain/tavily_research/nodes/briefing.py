from langchain_core.prompts import ChatPromptTemplate
from entity.domain.state import ResearchCompanyState
import asyncio
from typing import Dict, Any
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

category_prompts = {
    "financial": """
        为 {industry} 行业公司 {company} 撰写一份聚焦且全面的财务简报
        关键要求:
        1. 使用以下标题和项目符号组织结构：
        ### 融资与投资
        * 标注总融资金额及日期
        * 列出每一轮融资及其日期
        * 列出具名投资方
        ### 收入模式
        * 讨论产品/服务的定价

        2. 尽可能包含具体数字
        3. 仅使用项目符号，不要写段落
        4. 切勿出现“未找到信息”或“无可用数据”的表述
        5. 切勿重复同一轮融资；若同一月份出现多次融资记录，一律视为同一轮融资
        6. 切勿给出融资金额范围；请根据提供的信息作出最佳判断，给出确切金额
        7. 只提供简报内容，不要添加任何解释或评论 

    """,
    "industry": """
        为 的 {industry} 行业公司 {company} 撰写一份聚焦且全面的行业简报
        关键要求:
        1. 使用以下“完全一致”的标题与项目符号组织结构：
        ### 市场概览
        * 给出 {company} 的精准市场细分
        * 列出市场规模并标注年份
        * 列出增长率并标注年份范围
        ## 直接竞争
        * 列出具名的直接竞争对手
        * 列出具体的竞品
        * 列出市场地位/份额等信息
        ## 竞争优势
        * 列出独特的技术特性
        * 列出已被证明的优势
        ## 市场挑战
        * 列出经验证的具体挑战

        2. 每个项目符号必须是一个完整的、独立的新闻事件
        3. 不要写段落，只使用项目符号
        4. 切勿出现“未找到信息”或“无可用数据”的表述
        5. 只提供简报内容，不要添加任何解释或评论 
    """,
}


# 生成简报节点
class BriefingNode:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="sk-20ac359475264bd8b170bf90c230d0c7",
            model="deepseek-v3.2",  # 需要替换为实际可用的模型名
        )

    async def run(self, state: ResearchCompanyState):
        """根据研究数据，生成研究简报"""
        context = {
            "company": state["company_name"],
            "industry": state["industry"],
        }

        categories = {
            "financial_data": ("financial", "financial_briefing"),
            "industry_data": ("industry", "industry_briefing"),
        }

      
        briefing_tasks = []
        for data_field, (category, briefing_key) in categories.items():
            curated_data = state.get(f"curated_{data_field}", {})
            if curated_data:
                briefing_tasks.append(
                    {
                        "category": category,
                        "briefing_key": briefing_key,
                        "data_field": data_field,
                        "curated_data": curated_data,
                    }
                )


        # 每个类别的简报
        briefings = {}
        if briefing_tasks:
            # 异步信号量：控制2个
            briefing_semaphore = asyncio.Semaphore(2)

            async def process_briefing(task: Dict[str, Any]):
                async with briefing_semaphore:
                    result = {"content": ""}

                    content = await self._generate_category_briefing(
                        category=task["category"],
                        docs=task["curated_data"],
                        context=context,
                    )
                    result["content"] = content
                    # 记录每个类别的简报
                    briefings[task["category"]] = result
            await asyncio.gather(*[process_briefing(task) for task in briefing_tasks])
               
        # 整体简报
        state['briefings'] = briefings
        return state

    async def _generate_category_briefing(
        self, category: str, docs: Dict[str, Any], context: Dict[str, Any]
    ):
        """根据类别和文档，生成简报"""
        company = context.get("company", "")
        industry = context.get("industry", "")

        category_prompt = category_prompts.get(category, "")
        # 填充模板变量
        category_prompt = category_prompt.format(
            company=company,
            industry=industry,
        )

        if not category_prompt:
            return {"content": f"未找到{category}的简报模板"}

        formatted_docs = self._prepare_documents(docs)

        briefing_prompt = """
        {category_prompt}
        分析以下文档并提取关键信息，仅提供简报内容，不要给出任何解释或评论
        {documents}
        """

        formatted_briefing_prompt = ChatPromptTemplate.from_messages(
            [("user", briefing_prompt)]
        )

        chain = formatted_briefing_prompt | self.llm | StrOutputParser()

        content = chain.invoke(
            {
                "category_prompt": category_prompt,
                "documents": formatted_docs,
            }
        )

        return content

    def _prepare_documents(self, docs: Dict[str, Any]):
        """准备文档内容，合并所有文档的raw_content"""

        items = list(docs.items())

        # 文档最大长度
        max_doc_length = 1000

        doc_texts = []
        total_length = 0
        for _, doc in items:
            title = doc.get("title", "")
            content = doc.get("raw_content", "") or doc.get("content", "")

            if len(content) > max_doc_length:
                content = content[:max_doc_length] + "...[内容已被截断]"

            doc_entry = f"标题:{title}\n\n 内容:{content}"
            if total_length + len(doc_entry) < 120000:
                doc_texts.append(doc_entry)
                total_length += len(doc_entry)

        # 添加doc分割符
        separator = "\n" + "-" * 40 + "\n"

        return f"{separator}{separator.join(doc_texts)}{separator}"
