import streamlit as st
import pandas as pd
import numpy as np
from utils.common import set_page_style
from floating_ai import render_floating_ai

set_page_style()

st.title("文件管理与分析")

st.subheader("历史仿真性能摘要")
c1, c2, c3 = st.columns(3)
c1.metric("平均电压跌落深度", "12.4%", "-2.1%")
c2.metric("频率恢复耗时", "0.42 s", "-0.05 s")
c3.metric("VSG阻尼比评估", "0.707", "优")

uploaded_file = st.file_uploader("上传仿真数据 (.csv, .xlsx)", type=["csv", "xlsx"])

df = pd.DataFrame(np.random.randn(5, 5), columns=['时间', '有功', '无功', '电压', '频率'])
st.subheader("数据预览")
st.dataframe(df, use_container_width=True)

st.download_button("下载完整仿真实验报告", data="PDF内容占位", file_name="Simulation_Report.pdf")

render_floating_ai()