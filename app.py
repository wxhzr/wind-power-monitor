import streamlit as st
from floating_ai import render_floating_ai
from utils.common import set_page_style

# 1. 页面配置
st.set_page_config(
    page_title="深远海风电构网型监测平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 全局 CSS 优化
set_page_style()

# 3. 页面内容
st.title("深远海风电构网型控制监测平台")
st.info("欢迎。本项目旨在研究深远海风电在弱网环境下的构网型控制策略稳定性。")
st.image("https://via.placeholder.com/1000x300.png?text=Platform+Overview", width="stretch")

# 4. 渲染悬浮 AI
render_floating_ai()