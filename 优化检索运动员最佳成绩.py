import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# 读取athlete_links.csv中的URLs
urls_df = pd.read_csv('D:/Users/11619/PycharmProjects/跑步记录爬取/排行榜中的运动员主页/10K_athlete_links1.csv')
urls = urls_df.iloc[:, 0].tolist()

for url in urls:
    # 从URL中提取athleteid作为文件名
    athlete_id = url.split('athleteid=')[-1]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到特定的divs
    div1 = soup.find('div', {'id': 'cphBody_pnlAthleteDetails'})
    div2 = soup.find('div', {'id': 'cphBody_pnlBestPerformances'})

    base_dir1 = 'D:/Users/11619/PycharmProjects/跑步记录爬取/跑步数据/AthleteDetails/'
    base_dir2 = 'D:/Users/11619/PycharmProjects/跑步记录爬取/跑步数据/BestPerformances/'

    athlete_details_filename = f'{base_dir1}ID_{athlete_id}.csv'
    best_performances_filename = f'{base_dir2}ID_{athlete_id}.csv'

    # 处理第一个div
    if div1 and div1.find_all('table'):
        tables1 = div1.find_all('table')
        with open(athlete_details_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for table in tables1:
                if table.get('cellspacing') == '0' and table.get('cellpadding') == '2':
                    for row in table.find_all('tr'):
                        columns = row.find_all('td')
                        data = [column.get_text(strip=True) for column in columns]
                        writer.writerow(data)
    else:
        print(f"未找到指定的AthleteDetails表格: {url}")

    # 处理第二个div
    if div2 and div2.find('table', {'class': 'alternatingrowspanel'}):
        table2 = div2.find('table', {'class': 'alternatingrowspanel'})
        with open(best_performances_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in table2.find_all('tr'):
                columns = row.find_all('td')
                data = [column.get_text(strip=True) for column in columns]
                writer.writerow(data)
    else:
        print(f"未找到指定的BestPerformances表格: {url}")

print('所有CSV文件已成功创建。')
