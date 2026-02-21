import streamlit as st
from utils.common import set_page_style
from floating_ai import render_floating_ai

set_page_style()

st.title("故障监测")
st.success("系统状态：正常运行。构网型算法正在提供惯量支撑。")
st.json({
    "实时健康分": 98,
    "最近故障预警": "无",
    "直流电压波动": "0.02%",
    "谐波畸变率": "1.2%"
})

render_floating_ai()