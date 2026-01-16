from entity.domain.state import CompanyState, ResearchCompanyState
from tavily import AsyncTavilyClient
from loguru import logger


# 基础节点
class GroundingNode:
    def __init__(self):
        self.tavily_client = AsyncTavilyClient(
            api_key="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"
        )

    async def run(self, state: CompanyState) -> ResearchCompanyState:
        logger.info(f"开始爬取公司官网信息: {state['company_url']}")

        # 爬取公司官网信息
        crawl_content = await self.tavily_client.crawl(
            url=state["company_url"],
            instructions="请详细介绍一下公司的背景、产品、服务、客户案例、合作关系、未来发展计划等。",
            # 爬取最大深度
            max_depth=1,
            # 最大结果数
            limit=5,
        )
        results = crawl_content.get('results', [])

        site_scrape = {}
        for item in results:
            content = item.get('raw_content')
            url = item.get('url')
            site_scrape[url] = {
                'row_content': content,
                'source': 'company_website'
            }

        return {**state, "site_scrape": site_scrape}
