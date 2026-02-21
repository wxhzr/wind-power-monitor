import streamlit as st
import numpy as np
import plotly.graph_objs as go
from utils.common import set_page_style
from floating_ai import render_floating_ai

set_page_style()

st.title("深远海风电构网型控制监测平台 - 实时监测")

# --- 源端数据 ---
st.subheader("源端数据（风电场侧）")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="kpi-card"><div class="kpi-title">风速</div><div class="kpi-value">12.5 m/s</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="kpi-card"><div class="kpi-title">有功功率 P</div><div class="kpi-value">50 MW</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="kpi-card"><div class="kpi-title">无功功率 Q</div><div class="kpi-value">8 MVar</div></div>', unsafe_allow_html=True)

# --- 网端数据 ---
st.subheader("网端数据（柔性直流送出侧）")
col4, col5 = st.columns(2)
with col4:
    st.markdown('<div class="kpi-card"><div class="kpi-title">直流母线电压</div><div class="kpi-value">30.0 kV</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div class="kpi-card"><div class="kpi-title">并网点频率</div><div class="kpi-value">50.02 Hz</div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- 对比曲线 ---
st.subheader("控制策略对比分析")
t = np.arange(0, 10, 0.1)
y_gfm = 50 + 0.02 * np.exp(-t) * np.sin(2 * t)
y_gfl = 50 + 0.08 * np.exp(-0.3 * t) * np.sin(2 * t)

col_left, col_right = st.columns(2)
with col_left:
    fig1 = go.Figure(go.Scatter(x=t, y=y_gfm, name="构网型控制"))
    fig1.update_layout(title="构网型控制下频率响应", xaxis_title="时间(s)", yaxis_title="频率(Hz)", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)
with col_right:
    fig2 = go.Figure(go.Scatter(x=t, y=y_gfl, name="传统跟网型控制", line=dict(dash='dash', color='orange')))
    fig2.update_layout(title="传统控制下频率响应", xaxis_title="时间(s)", yaxis_title="频率(Hz)", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

render_floating_ai()