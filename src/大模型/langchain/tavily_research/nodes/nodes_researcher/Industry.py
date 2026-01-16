from entity.domain.state import ResearchCompanyState
from .base_researcher import BaseResearcher


prompt = """
为{industry}行业中的{company}公司，生成行业分析相关的查询语句，例如:
- 市场定位
- 竞争对手
- {industry}行业趋势与挑战
- 市场规模与增长
"""

# 行业分析节点
class IndustryNode(BaseResearcher):
    def __init__(self):
        super().__init__()
    async def run(self, state: ResearchCompanyState) -> ResearchCompanyState:
        querys = await self.generate_queries(state, prompt)
        new_documents = await self.search_documents(querys)

        industry_data = dict(state.get('site_scrape',{}))

        industry_data.update(new_documents)
        
        return {
            'industry_data': industry_data
        }