import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import io

# 设置控制台输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

class WeChatArticleSummarizer:
    def __init__(self):
        pass
        
    def fetch_article(self, url):
        """获取文章内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取文章标题和正文
            title = soup.find('h1', class_='rich_media_title').get_text(strip=True)
            content = soup.find('div', class_='rich_media_content').get_text(strip=True)
            
            return {
                'title': title,
                'content': content,
                'url': url
            }
        except Exception as e:
            print(f"获取文章时出错: {str(e)}")
            return None

    def extract_summary(self, text, max_sentences=3):
        """生成文章摘要
        使用简单的基于句子重要性的方法提取摘要
        """
        try:
            # 分句
            sentences = text.split('。')
            sentences = [s.strip() + '。' for s in sentences if s.strip()]
            
            if not sentences:
                return ""
            
            # 如果句子数量小于等于要求的摘要句子数，直接返回全文
            if len(sentences) <= max_sentences:
                return ''.join(sentences)
            
            # 选择前几句作为摘要
            # 通常文章的前几句包含了主要信息
            summary = ''.join(sentences[:max_sentences])
            
            return summary
        except Exception as e:
            print(f"生成摘要时出错: {str(e)}")
            return None

    def save_summary(self, article_data, summary):
        """保存文章摘要到文件"""
        try:
            # 创建输出目录
            output_dir = "article_summaries"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/summary_{timestamp}.json"

            # 准备保存的数据
            data = {
                'title': article_data['title'],
                'url': article_data['url'],
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            }

            # 保存到文件
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"摘要已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"保存摘要时出错: {str(e)}")
            return None

    def process_article(self, url):
        """处理单篇文章的完整流程"""
        # 1. 获取文章
        article_data = self.fetch_article(url)
        if not article_data:
            return None

        # 2. 生成摘要
        summary = self.extract_summary(article_data['content'])
        if not summary:
            return None

        # 3. 保存摘要
        return self.save_summary(article_data, summary)

def main():
    print("微信公众号文章摘要生成器")
    print("-" * 30)
    
    # 这里可以输入微信文章的URL
    # article_url = input("请输入微信公众号文章URL: ")
    article_url = "https://mp.weixin.qq.com/s/C_0j0vBUp9lpEdfhoJ1LYA"
    
    summarizer = WeChatArticleSummarizer()
    result = summarizer.process_article(article_url)
    
    if result:
        print("文章处理完成！")
    else:
        print("文章处理失败，请检查URL是否正确或网络连接是否正常。")

if __name__ == "__main__":
    main()
