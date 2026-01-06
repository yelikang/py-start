import jieba
import math
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import json


# 1. 句子分词: ep: 好莱坞电影推荐 -> [好莱坞, 电影, 推荐]
# 2. 句子得分

class BM25:
    """
    BM25算法实现类
    用于文档检索和相关性评分
    """
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        初始化BM25参数
        
        Args:
            k1: 控制词频饱和度的参数，通常取值1.2-2.0
            b: 控制文档长度归一化的参数，通常取值0.75
        """
        self.k1 = k1
        self.b = b
        self.documents = []  # 存储原始文档
        self.tokenized_docs = []  # 存储分词后的文档
        self.doc_freqs = defaultdict(int)  # 词汇在多少个文档中出现
        self.idf = {}  # 逆文档频率
        self.doc_len = []  # 每个文档的长度
        self.avgdl = 0  # 平均文档长度
        
    def tokenize(self, text: str) -> List[str]:
        """
        文本分词
        
        Args:
            text: 输入文本
            
        Returns:
            分词结果列表
        """
        # 使用jieba进行中文分词，去除长度小于2的词
        tokens = [word for word in jieba.cut(text) if len(word.strip()) >= 2]
        return tokens
    
    def fit(self, documents: List[str]):
        """
        训练BM25模型
        
        Args:
            documents: 文档列表
        """
        self.documents = documents
        self.tokenized_docs = []
        self.doc_freqs = defaultdict(int)
        
        # 1. 对所有文档进行分词
        for doc in documents:
            tokens = self.tokenize(doc)
            self.tokenized_docs.append(tokens)
            self.doc_len.append(len(tokens))
            
            # 统计词汇在多少个文档中出现
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] += 1
        
        # 2. 计算平均文档长度
        self.avgdl = sum(self.doc_len) / len(self.doc_len)
        
        # 3. 计算IDF值（逆文档频率）
        N = len(documents)  # 文档总数
        for token, freq in self.doc_freqs.items():
            # IDF = log((N - df + 0.5) / (df + 0.5))
            self.idf[token] = math.log((N - freq + 0.5) / (freq + 0.5))
    
    def get_score(self, query: str, doc_idx: int) -> float:
        """
        计算查询与指定文档的BM25得分
        
        Args:
            query: 查询字符串
            doc_idx: 文档索引
            
        Returns:
            BM25得分
        """
        query_tokens = self.tokenize(query)
        doc_tokens = self.tokenized_docs[doc_idx]
        doc_len = self.doc_len[doc_idx]
        
        # 统计文档中每个词的频率
        doc_token_counts = Counter(doc_tokens)
        
        score = 0.0
        for token in query_tokens:
            if token in doc_token_counts:
                # 词频
                tf = doc_token_counts[token]
                
                # IDF值
                idf = self.idf.get(token, 0)
                
                # BM25公式
                # score += IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl)))
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
                score += idf * (numerator / denominator)
        
        return score
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float, str]]:
        """
        搜索最相关的文档
        
        Args:
            query: 查询字符串
            top_k: 返回前k个结果
            
        Returns:
            [(文档索引, 得分, 文档内容), ...]
        """
        scores = []
        
        # 计算每个文档的得分
        for i in range(len(self.documents)):
            score = self.get_score(query, i)
            scores.append((i, score, self.documents[i]))
        
        # 按得分降序排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_k]
    
    def explain_score(self, query: str, doc_idx: int) -> Dict:
        """
        解释BM25得分的计算过程
        
        Args:
            query: 查询字符串
            doc_idx: 文档索引
            
        Returns:
            得分详细信息
        """
        query_tokens = self.tokenize(query)
        doc_tokens = self.tokenized_docs[doc_idx]
        doc_len = self.doc_len[doc_idx]
        doc_token_counts = Counter(doc_tokens)
        
        explanation = {
            "query": query,
            "query_tokens": query_tokens,
            "document": self.documents[doc_idx],
            "doc_length": doc_len,
            "avg_doc_length": self.avgdl,
            "token_scores": [],
            "total_score": 0.0
        }
        
        total_score = 0.0
        for token in query_tokens:
            token_info = {
                "token": token,
                "tf": doc_token_counts.get(token, 0),
                "df": self.doc_freqs.get(token, 0),
                "idf": self.idf.get(token, 0),
                "score": 0.0
            }
            
            if token in doc_token_counts:
                tf = doc_token_counts[token]
                idf = self.idf.get(token, 0)
                
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
                token_score = idf * (numerator / denominator)
                
                token_info["score"] = token_score
                total_score += token_score
            
            explanation["token_scores"].append(token_info)
        
        explanation["total_score"] = total_score
        return explanation


def demo():
    """
    BM25文档搜索演示
    """
    print("=== BM25文档搜索召回Demo ===\n")
    
    # 示例文档集合
    documents = [
        "好莱坞电影推荐系统可以根据用户喜好推荐电影",
        "机器学习算法在推荐系统中的应用非常广泛",
        "深度学习模型能够提高推荐系统的准确性",
        "电影推荐算法需要考虑用户的历史观看记录",
        "协同过滤是推荐系统中常用的技术方法",
        "内容基础推荐通过分析物品特征进行推荐",
        "好莱坞大片通常具有高制作成本和明星阵容",
        "人工智能技术正在改变电影制作和推荐方式",
        "用户画像分析有助于提升推荐系统效果",
        "电影评分预测是推荐系统的重要功能之一",
        "电影<美国队长>是好莱坞重量级热门的一部影片,具有很高的人气"
    ]
    
    # 初始化BM25模型
    bm25 = BM25(k1=1.5, b=0.75)
    
    print("正在训练BM25模型...")
    bm25.fit(documents)
    print(f"训练完成！共处理 {len(documents)} 个文档\n")
    
    # 测试查询
    test_queries = [
        "好莱坞电影推荐",
        # "机器学习推荐系统",
        # "深度学习算法",
        # "用户画像分析"
    ]
    
    for query in test_queries:
        print(f"查询: '{query}'")
        print("-" * 50)
        
        # 搜索相关文档
        results = bm25.search(query, top_k=3)
        
        for rank, (doc_idx, score, doc_content) in enumerate(results, 1):
            print(f"排名 {rank}: (得分: {score:.4f})")
            print(f"文档 {doc_idx}: {doc_content}")
            print()
        
        # 显示第一个结果的详细得分解释
        if results:
            best_doc_idx = results[0][0]
            explanation = bm25.explain_score(query, best_doc_idx)
            
            print("最佳匹配文档的得分详解:")
            print(f"查询词: {explanation['query_tokens']}")
            print(f"文档长度: {explanation['doc_length']}, 平均长度: {explanation['avg_doc_length']:.2f}")
            
            for token_info in explanation['token_scores']:
                if token_info['score'] > 0:
                    print(f"  词 '{token_info['token']}': TF={token_info['tf']}, "
                          f"DF={token_info['df']}, IDF={token_info['idf']:.4f}, "
                          f"得分={token_info['score']:.4f}")
            
            print(f"总得分: {explanation['total_score']:.4f}")
        
        print("=" * 60)
        print()


if __name__ == "__main__":
    # 运行演示
    demo()
    
    # # 交互式搜索
    # print("\n=== 交互式搜索 ===")
    # print("输入查询词进行搜索，输入 'quit' 退出")
    
    # # 使用演示数据初始化
    # documents = [
    #     "好莱坞电影推荐系统可以根据用户喜好推荐电影",
    #     "机器学习算法在推荐系统中的应用非常广泛", 
    #     "深度学习模型能够提高推荐系统的准确性",
    #     "电影推荐算法需要考虑用户的历史观看记录",
    #     "协同过滤是推荐系统中常用的技术方法",
    #     "内容基础推荐通过分析物品特征进行推荐",
    #     "好莱坞大片通常具有高制作成本和明星阵容",
    #     "人工智能技术正在改变电影制作和推荐方式",
    #     "用户画像分析有助于提升推荐系统效果",
    #     "电影评分预测是推荐系统的重要功能之一"
    # ]
    
    # bm25 = BM25()
    # bm25.fit(documents)
    
    # while True:
    #     query = input("\n请输入查询: ").strip()
    #     if query.lower() == 'quit':
    #         break
        
    #     if query:
    #         results = bm25.search(query, top_k=3)
    #         print(f"\n搜索结果 (查询: '{query}'):")
            
    #         if results:
    #             for rank, (doc_idx, score, doc_content) in enumerate(results, 1):
    #                 print(f"{rank}. (得分: {score:.4f}) {doc_content}")
    #         else:
    #             print("未找到相关文档")
    
    # print("感谢使用BM25搜索系统！")