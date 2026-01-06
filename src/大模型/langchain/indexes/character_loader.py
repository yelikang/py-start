import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter


# 字符切割：使用单一分隔符进行分割；只能指定一个分隔符，多个分隔符可以使用RecursiveCharacterTextSplitter
def split_text():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_path, 'demo.txt')
    # 文档加载
    loader = TextLoader(filepath, 'utf-8')
    documents = loader.load()

    # 文档切分
    text_splitter = CharacterTextSplitter(
        separator = "\n",  # 分隔符，默认\n\n
        chunk_size = 5,
        chunk_overlap=0
    )
    docs = text_splitter.split_documents(documents)
    print(docs)


if __name__ == '__main__':
    split_text()