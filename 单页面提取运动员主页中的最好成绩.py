import requests
import csv
from bs4 import BeautifulSoup

# 页面的URL
url = 'https://www.thepowerof10.info/athletes/profile.aspx?athleteid=16663'

# 使用requests获取页面内容
response = requests.get(url)

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 接下来，你可以继续找到表格并提取数据
# 确保'class'名称'alternatingrowspanel'是正确的，并且在你获取的HTML内容中存在

# 找到表格
table = soup.find('table', class_='alternatingrowspanel')

# 提取表头
headers = [header.text for header in table.find('tr').find_all('td')]

# 提取表格行数据
rows = table.find_all('tr')[1:]  # 跳过表头

with open('table_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # 写入表头
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        writer.writerow(cols)  # 写入数据

print('CSV文件已成功创建。')


# ------------

