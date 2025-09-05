from langchain_community.document_loaders import WebBaseLoader
import bs4

loader = WebBaseLoader(
    web_path='https://baijiahao.baidu.com/s?id=1842285798559978318', 
    # bs_kwargs=dict(parse_only=bs4.SoupStrainer(id="RichContent-inner"))
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(attrs={"class": "_18p7x"}))
    )
docs = loader.load()
print(docs)
