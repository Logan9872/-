import numpy as np
import mpmath as mt
from scipy.optimize import minimize, curve_fit
import pandas as pd
import matplotlib.pyplot as plt
# 读取数据

# [输入格式：（距离，时间），距离单位：米，时间格式：hh：mm：ss]
history_data = [
    {'dist': 1000, 'time': '2:12.82'}, {'dist': 1500, 'time': '3:29.46'},
    {'dist': 1609.34, 'time': '3:46.32'}, {'dist': 3000, 'time': '7:29.45'},
    {'dist': 5000, 'time': '12:58.39'}, {'dist': 10000, 'time': '27:08.23'}
]


# 将时间字符串转换为秒
def time_to_seconds(time_str):
    minutes, seconds = map(float, time_str.split(':'))
    return minutes * 60 + seconds


# 将数据转换为DataFrame
data = pd.DataFrame(history_data)
data['time_sec'] = data['time'].apply(time_to_seconds)


# 自定义非线性模型函数
# 定义时间预测函数
def time_fct(params, dist):
    # params: [vm,，gl, gs，tc]
    # dist: 距离数组
    vm, gl, tc, gs= params
    # 假设的常量时间
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


# 定义参数搜索范围
# (vm_lower, vm_upper), (gl_lower, gl_upper),(tc_lower, tc_upper) (gs_lower, gs_upper)
# vm交叉速度，gl长距离耐力指数，gs短距离耐力指数，tc交叉时间
param_bounds = ((2, 7), (0.05, 0.135), (300, 420), (0.08, 0.2))

# 定义一个函数来执行非线性最小二乘拟合，并考虑多个起始点
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

# 打印拟合后的图像
predictions = time_fct(best_params, data['dist'])
plt.figure(figsize=(10, 6))  # 设置图像大小
plt.scatter(data['dist'], data['time_sec'], label='Actual Time', color='blue')
plt.plot(data['dist'], predictions, 'r-', label='Predicted Time', linewidth=2)
plt.xlabel('Distance (meters)')
plt.ylabel('Time (seconds)')
plt.title('Actual vs Predicted Time')
plt.legend()
plt.grid(True)
plt.show()
