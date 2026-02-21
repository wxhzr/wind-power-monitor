import streamlit as st
import requests

def set_page_style():
    """全局 CSS 样式注入"""
    st.markdown("""
    <style>
        /* 统一导航栏对齐 */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important; margin: 0px !important; padding: 0px 10px !important;
            text-align: left !important; border: 1px solid #e0e0e0; border-radius: 8px; height: 45px;
        }
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            border: 1px solid #e0e0e0; border-radius: 8px; padding: 5px 10px !important; background-color: transparent !important;
        }
        /* 卡片样式 */
        .kpi-card {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 20px;
            border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.4); margin-bottom: 15px;
        }
        .kpi-title { font-size: 14px; opacity: 0.8; margin-bottom: 8px; }
        .kpi-value { font-size: 28px; font-weight: bold; }
        /* 手册右侧目录样式 */
        .toc-box {
            position: sticky; top: 2rem; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #1e3a8a;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_china_map():
    """加载中国地图 GeoJSON，带有缓存机制"""
    url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return None