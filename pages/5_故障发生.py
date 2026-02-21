import streamlit as st
import numpy as np
import plotly.graph_objs as go
from utils.common import set_page_style
from floating_ai import render_floating_ai

set_page_style()

st.title("故障触发模拟")
col_l, col_r = st.columns([1, 2])

with col_l:
    st.write("### 故障控制面板")
    f_type = st.selectbox("选择故障类型", ["无故障", "三相短路", "直流侧断路", "风速突降"])
    if st.button("立即触发表后故障"):
        st.error(f"检测到 {f_type}！系统进入低电压穿越模式。")

with col_r:
    t_f = np.linspace(0, 5, 100)
    v_f = np.ones(100)
    v_f[20:40] = 0.4  # 跌落
    v_f[40:70] = 0.4 + 0.6*(t_f[40:70]-0.4) # 恢复
    fig_f = go.Figure(go.Scatter(x=t_f, y=v_f, name="电压恢复曲线", line=dict(color='red')))
    fig_f.update_layout(title="故障恢复能力分析", xaxis_title="时间", yaxis_title="标幺值电压")
    st.plotly_chart(fig_f, use_container_width=True)

render_floating_ai()