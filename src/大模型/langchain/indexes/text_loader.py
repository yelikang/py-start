import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def split_text():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_path, 'demo.txt')
    # 文档加载
    loader = TextLoader(filepath, 'utf-8')
    documents = loader.load()

    # 文档切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap=20
    )
    docs = text_splitter.split_documents(documents)
    print(docs)

    # 向量化
    # embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    # vectors = Chroma.from_documents(
    #     documents = docs,
    #     embedding = embeddings,
    #     persist_directory = './chrom_db'
    # )
    

if __name__ == '__main__':
    split_text()