import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
def get_all_text_from_url(base_url):
    # 请求页面内容
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {base_url}")
        return None

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取页面上的所有文本内容
    text_content = soup.get_text()

    return text_content
def crawl_website(base_url):
    # 定义一个函数来递归地抓取所有链接
    def recursive_crawl(url):
        if url in visited_links:
            return
        visited_links.add(url)

        # 获取当前页面的所有文本内容
        text = get_all_text_from_url(url)
        if text:
            print(f"Text from {url}:")
            text = ' '.join(text.strip().split())
            data.append({'text':text})
        if len(data)%100==0:
            save()
        # 获取当前页面中的所有链接
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            # 将相对链接转换为绝对链接
            full_url = urljoin(base_url, href)
            if base_url in full_url:
                recursive_crawl(full_url)

    # 开始抓取
    recursive_crawl(base_url)
    return 
def save(file='tailaruiya.json'):
    with open(file,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False, indent=4)
