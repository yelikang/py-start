import requests
from bs4 import BeautifulSoup

# beautifulsoup4 解析网页内容
# lxml 解析器

def get_html_content(_url: str):
    response = requests.get(_url)
    if response.status_code == 200:
        return response.text
    else:
        return ""


def parse_html_content(_html_content: str):
    soup = BeautifulSoup(_html_content, "lxml")
    return soup


if __name__ == "__main__":
    url = "https://baijiahao.baidu.com/s?id=1844496593701031655"
    html_content = get_html_content(url)
    soup = parse_html_content(html_content)

    # 文档标题
    header_title = soup.title.getText()
    # 从内容中获取标题内容(使用find、find_all)
    titles = soup.find_all('div', class_="sKHSJ")
    for title in titles:
        # 获取元素属性，可以获取data-xxx等属性
        clazzName = title.get('class')
        print(title.text.strip())

    # 使用select选择器，获取二级标题内容
    second_titles = soup.select('.bjh-p')
    for st in second_titles:
        st_text = st.find('span', class_='bjh-strong')
        if st_text:
            print(st_text.text.strip())


