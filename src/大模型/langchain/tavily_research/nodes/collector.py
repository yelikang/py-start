from entity.domain.state import ResearchCompanyState
from urllib.parse import urljoin, urlparse

# 汇总研究数据


class CollectorNode:
    def run(self, state: ResearchCompanyState):
        """收集所有节点的结果"""

        data_types = {"financial_data": "financial", "industry_data": "industry"}

        # 根据页面url去重
        for data_field, doc_type in data_types.items():
            data = state.get(data_field, {})
            if not data:
                continue
            unique_docs = {}
            for url, doc in data.items():
                try:
                    parsed = urlparse(url)
                    if not parsed.scheme:
                        # 如果没有协议，添加默认协议
                        url = urljoin("https://", url)
                    # 移除查询参数和片段
                    clean_url = parsed._replace(query="", fragment="").geturl()
                    if clean_url not in unique_docs:
                        doc["url"] = clean_url
                        doc["doc_type"] = doc_type
                        unique_docs[clean_url] = doc
                except Exception as e:
                    print(f"Error processing {url}: {e}")
                    continue

            docs = list(unique_docs.values())
            evaluated_docs = self.evaluate_documents(docs)
            # 将evaluated_docs数组，转换为以url为键的字典；同时可以去重
            relevant_docs = {doc["url"]: doc for doc in evaluated_docs}
            # 排序，relevant_docs中的url可能被后面的文档覆盖，所以需要重新排序
            sorted_items = sorted(
                relevant_docs.items(),
                key = lambda item: item[1]['evaluation']['overall_score'],
                reverse=True,
            )

            if len(sorted_items) > 30:
                sorted_items = sorted_items[:30]
            relevant_docs = dict(sorted_items)

            # 记录每种数据类型的docs
            state[f'curated_{data_field}'] = relevant_docs

        return state

    def evaluate_documents(self, docs):
        """基于tavily评分,评估文档"""
        evaluated_docs = []
        for doc in docs:
            try:
                tavily_score = float(doc.get("score", 0))

                # 是否公司网站
                is_company_website = doc.get("source") == "company_website"

                # 评分限制(0.4)
                limit_score = 0.4
                if tavily_score >= limit_score or is_company_website:
                    # 如果搜索的文档评分大于0.4，或者是官方网站

                    evaluated_doc = {
                        **doc,
                        "evaluation": {
                            "overall_score": tavily_score,
                            "query": doc.get("query", ""),
                        },
                    }
                    evaluated_docs.append(evaluated_doc)

            except Exception as e:
                # 如果没有评分，默认不评估
                continue

        # 按评分排序
        evaluated_docs.sort(
            key=lambda x: x["evaluation"]["overall_score"], reverse=True
        )
        return evaluated_docs
