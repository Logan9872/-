import pandas as pd

# Load the performance data for men and women
df_men_performance = pd.read_csv('/数据/筛选后的数据/men_performance.csv')
df_women_performance = pd.read_csv('/数据/筛选后的数据/women_performance.csv')

# Corrected conversion function to handle numeric values as well
def convert_to_seconds(time_value, column):
    # If the value is NaN, return None
    if pd.isna(time_value):
        return None
    # If the value is already a numeric type, we assume it's already in seconds
    if isinstance(time_value, (int, float)):
        return time_value
    try:
        # If the value is a string, attempt to convert based on the expected format
        parts = time_value.split(':')
        if column == '5K':  # Format is "MM:SS"
            mins, secs = map(int, parts)
            return mins * 60 + secs
        elif column in ['10K', '10M', 'HM']:  # Format is "MM:SS:milli"
            mins, secs = parts[0], parts[1]
            secs, millis = map(int, secs.split('.'))
            return mins * 60 + secs + millis / 1000.0
        elif column == 'Mar':  # Format is "HH:MM:SS"
            hrs, mins, secs = map(int, parts)
            return hrs * 3600 + mins * 60 + secs
    except Exception as e:
        # If there's an error, return None to avoid data corruption
        print(f"Error converting {time_value}: {e}")
        return None

# Define the columns and their respective formats
column_formats = {
    '5K': 'MM:SS',
    '10K': 'MM:SS:milli',
    '10M': 'MM:SS:milli',
    'HM': 'MM:SS:milli',
    'Mar': 'HH:MM:SS'
}

# Apply the conversion function to each relevant column in the dataframes
for column, time_format in column_formats.items():
    df_men_performance[column] = df_men_performance[column].apply(lambda x: convert_to_seconds(x, column))
    df_women_performance[column] = df_women_performance[column].apply(lambda x: convert_to_seconds(x, column))

# Save the converted data
df_men_performance.to_csv('D:/Users/11619/PycharmProjects/跑步记录爬取/数据/筛选后的数据/men_performance_seconds.csv', index=False)
df_women_performance.to_csv('D:/Users/11619/PycharmProjects/跑步记录爬取/数据/筛选后的数据/women_performance_seconds.csv', index=False)
