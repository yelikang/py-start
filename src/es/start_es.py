from elasticsearch6 import Elasticsearch
from typing import List
from loguru import logger


class Es_client:
    def __init__(self, urls: List[str], username: str, password: str):
        self.client = Elasticsearch(
            urls,
            http_auth=(username, password),
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True,
        )
        logger.info("es client created")

    def list_indices(self):
        """
        获取所有索引
        """
        indices = self.client.cat.indices(format="json")
        logger.info(f"len: {len(indices)}")
        # for item in indices:
        #     print(f"索引: {item.get('index')}")

    def get_index_by_name(self, index_name: str):
        """
        获取指定索引的信息
        """
        info = self.client.indices.get(index_name)
        meta = info.get(index_name, {})
        aliases = meta.get("aliases", {})
        logger.info(f"{index_name}索引: 别名:{aliases}")

        rows = self.client.cat.indices(index_name, format="json")
        logger.info(f"{index_name}索引: 文档数:{rows[0].get('docs.count')}")

    def create_index(self, index_name: str, body: dict):
        """
        创建索引
        """
        # body={
        #     "settings": {
        #         "number_of_shards": 1,
        #         "number_of_replicas": 0,
        #     },
        #     "mappings": {
        #         "_doc": {
        #             "properties": {
        #                 "title": {"type": "text"},
        #                 "content": {"type": "text"},
        #             }
        #         }
        #     },
        #     "aliases": {
        #         "yk_test": {},
        #     }
        # },

        self.client.indices.create(index=index_name, body=body)
        logger.info(f"{index_name}索引创建成功")

    def delete_index(self, index_name: str):
        """
        删除索引
        """
        self.client.indices.delete(index=index_name)
        logger.info(f"{index_name}索引删除成功")

    def update_index(self, index_name: str, mapping_body: dict):
        """
        更新索引（好像不需要更新，操作document时，新增document字段，会自动更新；可以在创建索引时通过dynamic来控制默认行为）
        """
        self.client.indices.put_settings(index=index_name, body=mapping_body)
        logger.info(f"{index_name}索引更新成功")

    def search_index(self, index_name: str, keyword: dict):
        """
        搜索索引
        """
        res = self.client.search(index=index_name, body=keyword)
        logger.info(f"search {index_name} res: {res}")

    def insert_document(self, index_name: str, doc_id: str, document: dict):
        """
        插入文档/更新文档
        """
        response = self.client.index(
            index=index_name,
            doc_type="_doc",  # es6中必须指定doc_type为_doc，ES7中开始废弃
            id=doc_id,  # 这里如果不传，es会自动生成一个id；如果是已经存在的id，会覆盖原文档
            body=document,
        )

        logger.info(f"{index_name}索引文档插入成功")

    def delete_document(self, index_name: str, doc_id: str):
        """
        删除文档
        """
        self.client.delete(index=index_name, doc_type="_doc", id=doc_id)
        logger.info(f"{index_name}索引文档删除成功")
    
    def search_document(self, index_name: str, keyword: dict, size: int = 10):
        """
        搜索文档
        """
        res = self.client.search(index=index_name, body=keyword, size=size)

        result = {
            "total": res["hits"]["total"],
            "list": [item['_source'] for item in res["hits"]["hits"]]
        }
        logger.info(f"search {index_name} res: {result}")


if __name__ == "__main__":
    es_client = Es_client(
        urls=["http://10.5.23.193:9200/"],
        username="user",
        password="passwd",
    )
    # es_client.list_indices()
    # es_client.get_index_by_name('knowledge_base_content_v1749717498')

    # es_client.insert_document(
    #     index_name = "test_knowledge_yk",
    #     doc_id = None,
    #     document = {
    #         "title": "agent说明书",
    #         "content": "agent说明书内容",
    #         "age":20,
    #         "doc":{
    #             "type":"text",
    #             "value":"keyword测试",
    #             "fields":{
    #                 "keyword":{
    #                     "type":"keyword",
    #                     "ignore_above":256
    #                 }
    #             }
    #         }
    #     }
    # )

    # es_client.delete_document(
    #     index_name = 'test_knowledge_yk',
    #     doc_id = '3333'
    # )

    es_client.search_document(
        index_name = 'test_knowledge_yk',
        keyword = {
            "query": {
                # term: 不分词，按索引里的单个词项精确匹配；更像"等值过滤"；适合keyword、数值、日期、布尔、ID、邮箱、标签等
                # match：会用字段的分词器进行查询词分词；按相关性打分做全文检索；适合text字段的模糊/全文匹配
                # term:{"title.keyword":"agent说明书"}：需要字段按以下设置
                
                # "properties": {
                #     "name": {
                #         "type": "text",        # 会被分词
                #         "fields": {
                #             "keyword": {       # 不分词，完整存储
                #                 "type": "keyword",
                #                 "ignore_above": 256
                #             }
                #         }
                #     }
                # }


                # "term": {
                #     # 这里text类型的title字段，不会命中，应为索引可能被分成["agent", "说明书"]两个词项；所有搜索不到
                #     # "title.": "agent说明书"
                #     # 这里long类型的age字段，不会被索引，直接使用term能命中
                #     "age": 20
                # },
                # "term": {
                #     "doc.value.keyword": "keyword测试"
                # },
                # "match": {
                #     "title": "agent说明书"
                # }
            }
        }
    )


