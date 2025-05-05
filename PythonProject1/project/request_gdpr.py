import requests
from bs4 import BeautifulSoup


def html_to_text(html):
    # 创建 BeautifulSoup 对象，使用 lxml 解析器
    soup = BeautifulSoup(html, 'lxml')
    # 提取所有文本
    text = soup.get_text()
    # 分割文本为段落
    paragraphs = text.split('\n')
    # 过滤掉空段落
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs


def save_paragraphs_to_file(paragraphs, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for paragraph in paragraphs:
            file.write(paragraph + '\n')


def main():
    # 替换为你要访问的接口 URL
    url = 'http://www.innovation4.cn/library/FileData/33586?page=1'
    try:
        # 发送请求获取响应
        response = requests.get(url)
        # 检查响应状态码
        response.raise_for_status()
        response.encoding = 'utf-8'
        # 获取 HTML 内容
        html_content = response.text
        # 将 HTML 解析为段落文本
        print(html_content)

        paragraphs = html_to_text(html_content)
        print(paragraphs)

        # 保存段落文本到文件
        save_paragraphs_to_file(paragraphs, 'output.txt')
        print("文本已成功保存到 output.txt")
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")


if __name__ == "__main__":
    main()
