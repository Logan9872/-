import os
import pandas as pd

def extract_athlete_id(file_name):
    # 从文件名提取 athleteid
    prefix = "athleteid="
    start = file_name.find(prefix)
    if start != -1:
        start += len(prefix)
        end = file_name.find('.', start)
        return file_name[start:end]
    return None

def process_csv_files(folder_path):
    # 初始化汇总DataFrame，确保 'athleteid' 列存在
    summary_df = pd.DataFrame(columns=['athleteid'])

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # 提取athleteid
            athlete_id = extract_athlete_id(file_name)
            if athlete_id:
                file_path = os.path.join(folder_path, file_name)
                # 读取CSV文件
                df = pd.read_csv(file_path)
                # 确保有 "Event" 和 "PB" 列
                if "Event" in df.columns and "PB" in df.columns:
                    for index, row in df.iterrows():
                        event = row['Event']
                        pb = row['PB']
                        if event not in summary_df.columns:
                            summary_df[event] = pd.NA
                        # 检查athleteid是否已存在于summary_df中
                        if not summary_df['athleteid'].str.contains(athlete_id).any():
                            # 向summary_df中添加新行
                            new_row = {'athleteid': athlete_id, event: pb}
                            summary_df = pd.concat([summary_df, pd.DataFrame([new_row])], ignore_index=True)
                        else:
                            summary_df.loc[summary_df['athleteid'] == athlete_id, event] = pb

    return summary_df

# 示例用的文件夹路径，需要替换成实际路径
folder_path = './10K排行榜跑者数据'
summary_df = process_csv_files(folder_path)

# 保存汇总DataFrame到CSV
summary_df.to_csv('./summary.csv', index=False)
