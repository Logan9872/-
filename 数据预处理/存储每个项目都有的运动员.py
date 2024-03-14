

import pandas as pd

# Load the data
df = pd.read_csv('/数据/最佳成绩汇总/women_summary1.csv')

# Filter out rows where any of the specified columns have missing values
filtered_df = df.dropna(subset=['athleteid', '5K', '10K', '10M', 'HM', 'Mar'])

# Save the filtered data to a new CSV file
filtered_df.to_csv('D:/Users/11619/PycharmProjects/跑步记录爬取/数据/最佳成绩汇总/women_summary_c.csv', index=False)
