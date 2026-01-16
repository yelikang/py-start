from typing import TypedDict, Any

class CompanyState(TypedDict, total=False):
    """公司状态"""
    company_name: str
    company_url: str
    industry: str


class ResearchCompanyState(CompanyState):
    """搜索-公司状态"""
    # 站点刮取的内容(grounding节点从官网crawl的)
    site_scrape: dict[str, Any]
    # 财务数据：site_scrape + tavily.search内容
    financial_data: dict[str, Any]
    # 行业数据: site_scrape + tavily.search内容
    industry_data: dict[str, Any]
    # 挑选出的财务数据(按评分过滤、排序)
    curated_financial_data: dict[str, Any]
    # 挑选出的行业数据
    curated_industry_data: dict[str, Any]
    # 所有简报
    briefings: dict[str, Any]