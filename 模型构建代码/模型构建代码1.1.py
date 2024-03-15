import numpy as np
import mpmath as mt
from scipy.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_path = 'D:/Users/11619/PycharmProjects/跑步记录爬取/数据/筛选后的数据/men_performance_seconds1.csv'  # 更新为上传后的路径
data_csv = pd.read_csv(csv_path)

# 修改convert_to_specified_format函数以处理所有运动员的数据
def convert_to_specified_format(df):
    formatted_data = []
    distances = {'5000': 5000, '10000': 10000, '16093': 16093, '21097': 21097, '42195': 42195}
    for _, row in df.iterrows():
        athlete_id = row['athleteid']
        for dist_column, meters in distances.items():
            if not pd.isnull(row[dist_column]):
                time_sec = str(int(row[dist_column]))
                formatted_data.append({"id": int(athlete_id), "dist": meters, "time": time_sec})
    return formatted_data

history_data_converted = convert_to_specified_format(data_csv)

# 将数据转换为DataFrame
data = pd.DataFrame(history_data_converted)
data['time_sec'] = data['time'].astype(int)  # 转换时间为秒

# 以下函数和优化过程保持不变

# 自定义非线性模型函数，定义时间预测函数等...
def time_fct(params, dist):
    vm, gl, tc, gs = params
    dc = vm * tc
    time_pred = np.zeros_like(dist)
    for i, d in enumerate(dist):
        if d > dc:
            time_pred[i] = - (d / (gl * vm)) / mt.lambertw(-(d * np.exp(-1 / gl)) / (dc * gl), -1)
        else:
            time_pred[i] = -(d / (gs * vm)) / mt.lambertw(-(d * np.exp(-1 / gs)) / (dc * gs), -1)
    return time_pred

# 定义非线性最小二乘优化的目标函数
def objective(params, data):
    # params: [vm, gl, gs, tc]
    # data: 包含dist和time_sec的DataFrame
    predictions = time_fct(params, data['dist'])
    return np.sum((data['time_sec'] - predictions) ** 2)

# 定义参数搜索范围和nls_multstart函数
# 这些定义不需要修改
param_bounds = ((2, 7), (0.05, 0.135), (300, 420), (0.08, 0.2))

def nls_multstart(data, objective, param_bounds, num_starts=10):
    best_result = None
    best_params = None
    for _ in range(num_starts):
        # 随机选择起始点
        params0 = [np.random.uniform(low, high) for low, high in param_bounds]
        # 执行非线性最小二乘拟合
        result = minimize(objective, params0, args=(data,), bounds=param_bounds, method='L-BFGS-B')
        # 检查是否找到了更好的解
        if best_result is None or result.fun < best_result.fun:
            best_result = result
            best_params = result.x
    return best_params

# 使用最佳参数进行预测
best_params = nls_multstart(data, objective, param_bounds)
print("Best fit parameters:")
print("vm =", round(best_params[0] * 60, 2))
print("100gl =", round(best_params[1] * 100, 2))
print("tc =", round(best_params[2]/60, 2))
print("100gs =", round(best_params[3] * 100, 2))

# 生成一个基于所有独特距离的预测
unique_distances = np.sort(data['dist'].unique())
predictions_for_unique_distances = time_fct(best_params, unique_distances)

# 打印拟合后的图像
plt.figure(figsize=(10, 6))  # 设置图像大小
plt.scatter(data['dist'], data['time_sec'], label='Actual Time', color='blue')
plt.plot(unique_distances, predictions_for_unique_distances, 'r-', label='Predicted Time', linewidth=2)
plt.xlabel('Distance (meters)')
plt.ylabel('Time (seconds)')
plt.title('Actual vs Predicted Time')
plt.legend()
plt.grid(True)
plt.show()
