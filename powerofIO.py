import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# 发送HTTP请求
response = requests.get('https://www.thepowerof10.info/athletes/profile.aspx?athleteid=16663')
# 解析HTML源代码
soup = BeautifulSoup(response.text, 'html.parser')

# 找到特定的div
div1 = soup.find('div', {'id': 'cphBody_pnlAthleteDetails'})
div2 = soup.find('div', {'id': 'cphBody_pnlBestPerformances'})


print("--------------------------div1--------------------------")
tables1 = div1.find_all('table')
# 遍历所有的表格
with open('./跑步数据/AthleteDetails1.csv', 'w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    for table in tables1:
        # 检查cellspacing和cellpadding属性
        if table.get('cellspacing') == '0' and table.get('cellpadding') == '2':
            # 这是我们要找的表格
            # print(table)
            for row in table.find_all('tr'):
            # 在每行中，获取所有列的数据
                columns = row.find_all('td')
                data = [column.get_text() for column in columns]
                print(data)
                writer.writerow(data)


# # print("--------------------------div2--------------------------")
# # # 在这个div中找到具有特定class的表格
table2 = div2.find('table', {'class': 'alternatingrowspanel'})
with open('./跑步数据/BestPerformances1.csv', 'w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    # 遍历表格中的所有行
    for row in table2.find_all('tr'):
        # 在每行中，获取所有列的数据
        columns = row.find_all('td')
        data = [column.get_text() for column in columns]
        print(data)
        writer.writerow(data)


