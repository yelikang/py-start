import re

def split_large_text_by_length(text :str, length_limit :int) -> list[str]:
    """
    先按标点符号拆分，保留句子完整性，再将大文本按指定长度进行拆分。
    :param text: 输入的大文本字符串
    :param length_limit: 每个拆分段落的最大长度
    :return: 拆分后的段落列表
    """

    # 使用正则表达式将文本按句子划分
    # 保留中文和英文的句末标点符号（包括：。！？.!?）
    sentences = re.findall(r'[^。！？]+[。！？]', text)
    
    chunks = []
    current_chunk = ''
    
    for sentence in sentences:
        # 如果加上这个句子后长度仍 <= 目标长度，则加进去
        if len(current_chunk) + len(sentence) <= length_limit:
            current_chunk += sentence
        else:
            # 超过长度，先保存当前段落，再开始新段落
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    # 加入最后一段
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

    
if __name__ == '__main__':
    text ='你好呀！这是什么？这是一个文本,用来解释agent的内容。'
    chunks = split_large_text_by_length(text, 10)
    print(chunks)