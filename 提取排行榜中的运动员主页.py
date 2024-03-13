import csv
import requests
from bs4 import BeautifulSoup

# url = 'https://www.thepowerof10.info/rankings/rankinglist.aspx?event=Mar&agegroup=ALL&sex=M&year=2024'
url = 'https://www.thepowerof10.info/rankings/rankinglist.aspx?event=10K&agegroup=ALL&sex=M&year=2024'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

athlete_links = soup.find_all('a', href=True)
athleteid_links = [link['href'] for link in athlete_links if 'athleteid=' in link['href']]

# 将链接保存到CSV文件
with open('排行榜中的运动员主页/10K_athlete_links.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for link in athleteid_links:
        writer.writerow(['https://www.thepowerof10.info' + link])  # 如果链接是相对的，请添加基础URL

print('CSV文件已成功创建。')
