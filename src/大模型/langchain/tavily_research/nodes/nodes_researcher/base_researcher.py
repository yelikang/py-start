from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from loguru import logger
from tavily import AsyncTavilyClient
import asyncio

class BaseResearcher:
    def __init__(self):
        self.tavily_client = AsyncTavilyClient(
            api_key="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"
        )
        self.llm = ChatOpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="sk-20ac359475264bd8b170bf90c230d0c7",
            model="deepseek-v3.2",  # 需要替换为实际可用的模型名
        )

    async def generate_queries(self, state: Dict, prompt: str):
        """生成查询"""
        company_name = state.get("company_name", "")
        industry = state.get("industry", "")
        current_year = datetime.now().year
        current_day = datetime.now().strftime("%B %d, %Y"),

        query_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "你正在搜索{industry}行业的{company_name}公司"),
                (
                    "user",
                    """
                        任务:
                        {task_prompt}
                        时间限制:
                        {year}，截止{date}
                        指南:
                        1. 仅关注{company_name}特定信息
                        2. 查询要非常简洁且直击要点
                        3. 提供恰好4条搜索查询(每行一条)，且不要使用连字符或破折号
                        4. 不要对行业作任何假设-仅使用提供的行业信息
                    """,
                ),
            ]
        )

        chain = query_prompt | self.llm

        current_query = ''
        async for chunk in chain.astream({
            "industry": industry,
            "company_name": company_name,
            "task_prompt": prompt,
            "year": current_year,
            "date": current_day,
        }):
            current_query += chunk.content
        
        queries = current_query.splitlines()
        return queries

    async def search_documents(self, queries: list[str]):
        """搜索文档"""
        
        # 搜索参数
        search_params = {
            "search_depth":"basic",
            # 不要包含原始内容(html内容)
            "include_raw_content": False,
            "max_results": 5,
            # "topic": "news",
            "country": "china"
        }
        # 并发执行多个query
        search_tasks = [self.tavily_client.search(query, **search_params) for query in queries]
        # 等待所有任务完成
        try:
            results = await asyncio.gather(*search_tasks)
        except Exception as e:
            logger.error(f"Error during parallel search execution: {e}")
            return
        new_documents = {}
        # 按位置，循环匹配query、result；获取搜索结果
        for query, result in zip(queries, results):
            # 循环每个result的results结果
            for item in result.get('results', []):
                # 网页标题
                title = item.get('title', '')
                # 网页地址
                url = item.get('url', '')
                # 搜索结果的简短描述
                content = item.get('content', '')
                # 评分
                score = item.get('score', 0.0)

                # 构建新的文档
                new_documents[url] = {
                    'query': query,
                    'title': title,
                    'url': url,
                    'content': content,
                    'score': score,
                    "source": "web_search",
                }

        return new_documents