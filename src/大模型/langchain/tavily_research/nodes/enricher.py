from entity.domain.state import ResearchCompanyState
import asyncio
from tavily import AsyncTavilyClient

# 增强、丰富文档内容（填充raw_content内容-html内容）
class EnricherNode:
    def __init__(self):
        self.tavily_client = AsyncTavilyClient(
            api_key="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"
        )

    async def run(self, state: ResearchCompanyState):
        data_types = {"financial_data": "financial", "industry_data": "industry"}

        enrichment_tasks = []
        for data_field, doc_type in data_types.items():
            curated_docs = state.get(f"curated_{data_field}", {})

            # 需要获取raw_content的文档(raw_content为空的；官网raw_content不为空)
            docs_needing_content = {
                url: doc
                for url, doc in curated_docs.items()
                if not doc.get("raw_content")
            }

            enrichment_tasks.append(
                {
                    "field": data_field,
                    "curated_docs": curated_docs,
                    "docs": docs_needing_content,
                }
            )

        if enrichment_tasks:
            async def process_category(task):
                raw_contents = await self.fetch_raw_content(list(task["docs"].keys()))
                
                for url, content in raw_contents.items():
                    if content: # 爬取失败时，content可能为空
                        # 更新文档的raw_content
                        task["docs"][url]["raw_content"] = content


            # 并发处理（更新doc中的raw_content）
            await asyncio.gather(
                *[process_category(task) for task in enrichment_tasks]
            )

        return state

    async def fetch_raw_content(self, urls):
        """异步获取文档的raw_content"""
        raw_contents = {}

        # 创建批次(防止同时请求太多)
        batch_number = 20
        batches = [
            urls[i : i + batch_number] for i in range(0, len(urls), batch_number)
        ]

        # 异步信号量：同时处理的批次数量，不超过3个；没批20，最大请求为 3批 * 20 = 60个
        semaphore = asyncio.Semaphore(3)

        async def process_batch(batch_urls: list[str]):
            async with semaphore:
                tasks = [self.fetch_url_content(url) for url in batch_urls]
                results = await asyncio.gather(*tasks)

                batch_contents = {}
                for result in results:
                    batch_contents.update(result)
                return batch_contents
        
        batch_results = await asyncio.gather(*[process_batch(batch) for batch in batches])

        for batch_result in batch_results:
            raw_contents.update(batch_result)
        
        return raw_contents


    async def fetch_url_content(self, url):
        """异步获取单个文档的raw_content"""
        try:
            result = await self.tavily_client.extract(url)
            if result and result.get("results"):
                content = result.get("results")[0].get("raw_content", "")
                return {url: content}
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return {url: ""}
        return {url: ""}
