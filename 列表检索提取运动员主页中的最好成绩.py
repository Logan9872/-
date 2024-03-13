import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd

# 从CSV文件中加载URL
athlete_links_df = pd.read_csv('/排行榜中的运动员主页/10K_athlete_links.csv')
urls = athlete_links_df.iloc[:, 0].tolist()

for url in urls:
    # 从URL中提取athleteid用作文件名
    athlete_id = url.split('athleteid=')[-1]
    filename = f"athleteid={athlete_id}.csv"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 根据类名查找表格
    table = soup.find('table', class_='alternatingrowspanel')
    if table:
        headers = [header.text for header in table.find('tr').find_all('td')]
        rows = table.find_all('tr')[1:]  # 跳过标题行

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # 写入标题
            for row in rows:
                cols = [ele.text.strip() for ele in row.find_all('td')]
                writer.writerow(cols)  # 写入行数据
        print(f'CSV文件 {filename} 已成功创建。')
    else:
        print(f"未找到表格 {url}")
