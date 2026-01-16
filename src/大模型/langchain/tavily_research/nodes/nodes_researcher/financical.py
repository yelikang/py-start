from entity.domain.state import ResearchCompanyState
from .base_researcher import BaseResearcher


prompt = """
为{industry}行业中的{company}公司，生成财务分析相关的查询语句，例如:
- 融资与历史估值
- 财务报表与关键指标
- 收入与利润来源
"""

# 财务数据分析节点
class FinancialNode(BaseResearcher):
    def __init__(self):
        super().__init__()
    async def run(self, state: ResearchCompanyState) -> ResearchCompanyState:
        # 使用llm生成4条查询
        # 根据query，通过tavily search，获取财务数据
        querys = await self.generate_queries(state, prompt)
        # 并行搜索query的内容
        new_documents = await self.search_documents(querys)

        # 获取并拷贝site_scrape中的数据
        financial_data = dict(state.get('site_scrape',{}))

        financial_data.update(new_documents)
        
        return {
            'financial_data': financial_data
        }