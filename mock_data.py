import pandas as pd
import numpy as np

def get_steady_state_data():
    """
    模拟生成24小时的稳态运行数据 [cite: 19]
    包含：时间戳、风速、总功率、直流母线电压
    """
    # 模拟24小时，每小时一个点（演示时可以加速播放）
    times = pd.date_range("2024-01-01 00:00", "2024-01-01 23:59", freq="1H")
    
    # 随机生成数据，保持在合理范围内
    df = pd.DataFrame({
        "Time": times.strftime("%H:%M:%S"),
        # 风速：5-12m/s之间波动 [cite: 22]
        "Wind_Speed": np.round(np.random.uniform(5, 12, len(times)), 1),
        # 功率：2000-5000MW之间波动 [cite: 23]
        "Power_Total": np.random.randint(2000, 5000, len(times)),
        # 电压：500kV上下微小跳动 [cite: 24]
        "U_DC": np.round(np.random.normal(500, 2, len(times)), 2)
    })
    return df