import numpy as np
import mpmath as mt
from scipy.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np
from scipy.optimize import least_squares
# Load the CSV file
# csv_path = 'D:/Users/11619/PycharmProjects/跑步记录爬取/数据/筛选后的数据/men_performance_seconds1.csv'  # 请根据实际文件路径进行修改
csv_path = 'D:/Users/11619/PycharmProjects/跑步记录爬取/数据/筛选后的数据/women_performance_seconds1.csv'  # 请根据实际文件路径进行修改
data_csv = pd.read_csv(csv_path)

# 自定义非线性模型函数，定义时间预测函数等...
def time_fct(params, dist):
    # vm（最大速度）: 模型中的一个参数，代表运动员可以达到的最大速度。
    # tc（临界时间）: 运动员能以最大速度vm跑的时间长度。
    # gl（长距离耐力系数）: 当距离大于某个临界值（由vm和tc共同决定）时，描述运动员长距离耐力的参数。
    # gs（短距离耐力系数）: 当距离小于临界值时，描述运动员短距离耐力的参数
    vm, gl, tc, gs = params
    dc = vm * tc
    time_pred = np.zeros_like(dist, dtype=np.float64)
    for i, d in enumerate(dist):
        if d > dc:
            time_pred[i] = - (d / (gl * vm)) / mt.lambertw(-(d * np.exp(-1 / gl)) / (dc * gl), k=-1).real
        else:
            time_pred[i] = -(d / (gs * vm)) / mt.lambertw(-(d * np.exp(-1 / gs)) / (dc * gs), k=-1).real
    return time_pred

# 定义参数搜索范围
param_bounds = ((2, 7), (0.05, 0.135), (300, 420), (0.08, 0.2))

# 定义一个函数来执行非线性最小二乘拟合

def nls_fit(dist, times, param_bounds, num_starts=10):
    best_result = None
    # 定义残差函数
    def residuals(params, dist, times):
        return times - time_fct(params, dist)
    for _ in range(num_starts):
        params0 = [np.random.uniform(low, high) for low, high in param_bounds]
        # 使用least_squares
        result = least_squares(residuals, params0, bounds=np.transpose(param_bounds), args=(dist, times))
        # 检查并更新最佳结果
        if best_result is None or result.cost < best_result.cost:
            best_result = result

    return best_result.x

# def nls_fit(dist, times, param_bounds, num_starts=10):
#     best_result = None
#     for _ in range(num_starts):
#         params0 = [np.random.uniform(low, high) for low, high in param_bounds]
#         result = minimize(lambda params: np.sum((times - time_fct(params, dist)) ** 2),
#                           params0, bounds=param_bounds, method='L-BFGS-B')
#         if best_result is None or result.fun < best_result.fun:
#             best_result = result
#     return best_result.x

# 准备绘图
plt.figure(figsize=(10, 6))

# 为每个运动员绘制数据点和拟合曲线
colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
athlete_ids = data_csv['athleteid'].unique()
for athlete_id in athlete_ids:
    athlete_data = data_csv[data_csv['athleteid'] == athlete_id]
    dists = []
    times = []
    for dist_col in ['5000', '10000', '16093', '21097', '42195']:
        if not np.isnan(athlete_data.iloc[0][dist_col]):
            dists.append(int(dist_col))
            times.append(athlete_data.iloc[0][dist_col])
    if dists:
        dists = np.array(dists)
        times = np.array(times)
        best_params = nls_fit(dists, times, param_bounds)
        predicted_times = time_fct(best_params, dists)
        color = next(colors)
        plt.scatter(dists, times,  color=color, alpha=0.5)
        plt.plot(dists, predicted_times, color=color, alpha=0.75)

plt.xlabel('Distance (meters)')
plt.ylabel('Time (seconds)')
plt.title('Actual vs Predicted Time for Each Athlete')
plt.legend()
plt.grid(True)
plt.show()
