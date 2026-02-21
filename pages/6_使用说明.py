import streamlit as st
from utils.common import set_page_style
from floating_ai import render_floating_ai

set_page_style()

st.title("📚 技术原理与使用手册")

tab1, tab2 = st.tabs(["📖 操作指南", "⚡ 技术原理"])

with tab1:
    st.info("💡 请点击“技术原理”标签页查看您要求的 PMSG 和 VSG 详细介绍。")
    st.write("（此处可以保留原本的操作说明内容...）")

with tab2:
    st.markdown(r"""
    ### 1. 永磁直驱风力发电机 (PMSG)
    **PMSG (Permanent Magnet Synchronous Generator)** 是深远海风电的主流机型。
    ... (保留你原来的文本) ...
    """, unsafe_allow_html=True)

render_floating_ai()