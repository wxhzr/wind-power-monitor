import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from openai import OpenAI
from floating_ai import render_floating_ai
import requests
import time
from streamlit_echarts import st_echarts, Map
import json

# --- 数据加载函数 ---
# 添加缓存装饰器，避免每次刷新都去下载地图，提高速度
# --- 数据加载函数 ---
@st.cache_data
def load_china_map():
    # 使用阿里云 DataV 的公开 GeoJSON 数据 (中国地图)
    url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return None
# --- 模拟数据生成函数 ---
def get_topology_data():
    # 模拟24小时数据
    times = pd.date_range("2024-01-01 00:00", "2024-01-01 23:59", freq="1H")
    df = pd.DataFrame({
        "Time": times.strftime("%H:%M:%S"),
        "Wind_Speed": np.round(np.random.uniform(5, 12, len(times)), 1),
        "Power_Total": np.random.randint(2000, 5000, len(times)),
        "U_DC": np.round(np.random.normal(500, 2, len(times)), 2)
    })
    return df

# ----------------------------
# 1. 页面配置
# ----------------------------
st.set_page_config(
    page_title="深远海风电构网型监测平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 2. 全局 CSS 优化
# ----------------------------
st.markdown("""
<style>
    /* 统一导航栏对齐 */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        margin: 0px !important;
        padding: 0px 10px !important;
        text-align: left !important;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        height: 45px;
    }
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 5px 10px !important;
        background-color: transparent !important;
    }
    /* 卡片样式 */
    .kpi-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }
    .kpi-title { font-size: 14px; opacity: 0.8; margin-bottom: 8px; }
    .kpi-value { font-size: 28px; font-weight: bold; }

    /* 手册右侧目录样式 */
    .toc-box {
        position: sticky;
        top: 2rem;
        padding: 15px;
        background-color: #f8f9fa;
        border-left: 4px solid #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 3. 侧边栏导航逻辑
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = "1. 平台首页"

st.sidebar.title("构网型风电平台")
st.sidebar.markdown("---")

# 主目录 1
if st.sidebar.button("1. 平台首页"):
    st.session_state.page = "1. 平台首页"

# 主目录 2：数据处理
with st.sidebar.expander("2. 数据处理", expanded=(st.session_state.page in ["实时监测", "拓扑结构", "文件管理"])):
    if st.button("实时监测", key="sub21"):
        st.session_state.page = "实时监测"
    if st.button("拓扑结构", key="sub22"):
        st.session_state.page = "拓扑结构"
    if st.button("文件管理", key="sub23"):
        st.session_state.page = "文件管理"

# 主目录 3：故障诊断
with st.sidebar.expander("3. 故障诊断", expanded=(st.session_state.page in ["故障检测", "故障发生"])):
    if st.button("故障检测", key="sub31"):
        st.session_state.page = "故障检测"
    if st.button("故障发生", key="sub32"):
        st.session_state.page = "故障发生"

# 主目录 4
if st.sidebar.button("4. 使用说明"):
    st.session_state.page = "4. 使用说明"


# ----------------------------
# 4. 页面分发
# ----------------------------
page = st.session_state.page

if page == "1. 平台首页":
    st.title("深远海风电构网型控制监测平台")
    st.info("欢迎。本项目旨在研究深远海风电在弱网环境下的构网型控制策略稳定性。")
    # 修改参数名为 use_container_width
    st.image("https://via.placeholder.com/1000x300.png?text=Platform+Overview", use_container_width=True)
# ============================
# 实时监测
# ============================
elif page == "实时监测":
    st.title("深远海风电构网型控制监测平台")

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
    # 模拟构网型平稳数据
    y_gfm = 50 + 0.02 * np.exp(-t) * np.sin(2 * t)
    # 模拟跟网型波动数据
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


# ============================
# 拓扑结构 (结合真实工程表格参数 + 修复悬浮卡片不显示)
# ============================
elif st.session_state.page == "拓扑结构":
    # --- [引入时间模块] 用于获取真实北京时间 ---
    from datetime import datetime, timezone, timedelta

    # --- [UI] 顶部状态栏 ---
    col_header_1, col_header_2 = st.columns([4, 1])
    with col_header_1:
        st.markdown("### 🌐 深远海风电柔直送出系统 - 实时监控中心")
    with col_header_2:
        st.markdown(
            """
            <div style='background-color:rgba(0, 255, 0, 0.1); border:1px solid #00ff00; border-radius:5px; padding:5px; text-align:center; color:#00ff00; font-weight:bold;'>
                ● 系统状态: 正常运行
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- [地图数据] 加载 ---
    map_data = load_china_map()
    if not map_data:
        st.error("地图数据加载失败，请检查网络连接。")
        st.stop()

    # --- [模拟数据] 基础波形生成 ---
    if 'sim_data' not in st.session_state:
        x = np.linspace(0, 4 * np.pi, 24) 
        wind_wave = 10 + 8 * np.sin(x)    
        power_wave = wind_wave * 200      
        
        st.session_state.sim_data = pd.DataFrame({
            "Wind_Speed": wind_wave, 
            "Power_Total": power_wave
        })
        st.session_state.play_index = 0 

    # --- [滑动窗口历史数据] 用于绘制两侧的动态曲线 ---
    if 'history_u' not in st.session_state:
        st.session_state.history_u = [500.0] * 20 
        st.session_state.history_p = [2000.0] * 20 

    # 默认开启自动播放
    if 'auto_play' not in st.session_state:
        st.session_state.auto_play = True 

    # --- [获取并更新实时数据] ---
    idx = st.session_state.play_index
    current_row = st.session_state.sim_data.iloc[idx]
    
    current_u = round(500.0 + np.random.uniform(-0.5, 0.5), 1) # 实时微扰电压
    current_p = current_row['Power_Total']
    current_wind = current_row['Wind_Speed']
    
    st.session_state.history_u.append(current_u)
    st.session_state.history_u.pop(0)
    st.session_state.history_p.append(current_p)
    st.session_state.history_p.pop(0)

    # ==========================================
    # 地图静态化配置 (⚠️更名为 v2 强制刷新缓存)
    # ==========================================
    if 'static_map_option_v2' not in st.session_state:
        geo_coord = {
            "阳江风电场群": [111.90, 21.50],
            "海上换流站(DRU)": [112.30, 21.35],
            "陆上登陆点": [112.80, 21.90],
            "多端口断路器(Hub)": [113.10, 22.60], 
            "大湾区负荷中心": [113.50, 23.10]
        }
        icon_wind = "path://M12,2L12,2c0.55,0,1,0.45,1,1v8.59l6.07-6.07c0.39-0.39,1.02-0.39,1.41,0l0,0c0.39,0.39,0.39,1.02,0,1.41L14.41,13 H23c0.55,0,1,0.45,1,1l0,0c0,0.55-0.45,1-1,1h-8.59l6.07,6.07c0.39,0.39,0.39,1.02,0,1.41l0,0c-0.39,0.39-1.02,0.39-1.41,0 L13,16.41V25c0,0.55-0.45,1-1,1l0,0c-0.55,0-1-0.45-1-1v-8.59l-6.07,6.07c-0.39,0.39-1.02,0.39-1.41,0l0,0 c-0.39-0.39-0.39-1.02,0-1.41L9.59,15H1c-0.55,0-1-0.45-1-1l0,0c0-0.55,0.45-1,1-1h8.59L3.52,6.93C3.13,6.54,3.13,5.91,3.52,5.52l0,0 c0.39-0.39,1.02-0.39,1.41,0L11,11.59V3C11,2.45,11.45,2,12,2z"
        icon_converter = "path://M3,3v18h18V3H3z M19,19H5V5h14V19z M12,7l-3,3h2v4H9l3,3l3-3h-2v-4h2L12,7z"
        icon_breaker = "path://M12 2L2 12l10 10 10-10L12 2zm0 16l-6-6 6-6 6 6-6 6z"
        icon_city = "path://M12,3L2,12h3v8h6v-6h2v6h6v-8h3L12,3z"

        # 生成纯净的 HTML 字符串
        def make_tooltip(title, params_dict):
            rows = ""
            for k, v in params_dict.items():
                rows += f"<div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;'><span style='color:#aaa;'>{k}</span><span style='color:#fff;font-weight:bold;'>{v}</span></div>"
            return f"<div style='width:220px;background:rgba(20,30,50,0.95);border:1px solid #00eaff;border-radius:8px;padding:12px;color:#fff;box-shadow:0 0 10px rgba(0,234,255,0.3);text-align:left;'><div style='color:#00eaff;font-size:14px;font-weight:bold;margin-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);padding-bottom:5px;'>{title}</div>{rows}</div>"

        # 精确映射真实参数
        tooltip_wind = make_tooltip("阳江风电场群", {"送端系统容量": "5000 MVA", "送端系统惯量": "4 s", "状态": "并网稳定运行"})
        tooltip_dru = make_tooltip("海上换流站(DRU)", {"额定电压": "±500 kV", "额定电流": "2000 A", "额定功率": "2000 MW", "子模块电容": "20833 μF", "子模块数量": "200"})
        tooltip_hub = make_tooltip("多端口断路器(Hub)", {"设备类型": "混合式断路器", "动作时间": "3 ms", "关键功能": "主动限流/故障隔离"})
        tooltip_load = make_tooltip("大湾区负荷中心", {"受端系统容量": "10000 MVA", "受端系统惯量": "3 s", "供电区域": "广州/深圳"})
        tooltip_cable = make_tooltip("柔直高压海缆", {"电压等级": "±500 kV", "线缆截面": "1×2500 mm²", "输送功率": "2215 MVA", "直流线路电阻": "2.0 Ω"})

        st.session_state.static_map_option_v2 = {
            "backgroundColor": '#0E1116',
            "tooltip": {
                "trigger": 'item',
                # 【关键修复】：取消全局 formatter，让各节点使用自身的独立 tooltip 渲染
                "padding": 0,
                "backgroundColor": "transparent",
                "borderColor": "transparent",
                "borderWidth": 0,
                "extraCssText": "box-shadow: none;"
            },
            "geo": {
                "map": "china",
                "center": [112.8, 22.0],
                "zoom": 7,
                "roam": True,
                "itemStyle": {"areaColor": '#1B2336', "borderColor": '#2a333d'},
                "emphasis": {"itemStyle": {"areaColor": '#2a333d'}}
            },
            "series": [
                {
                    "type": "lines",
                    "coordinateSystem": "geo",
                    "effect": {
                        "show": True, 
                        "period": 2.5,  
                        "trailLength": 0.6,    
                        "color": "#00ffcc", "symbol": "arrow", "symbolSize": 8
                    },
                    "lineStyle": {"color": "#a6c84c", "width": 0, "curveness": 0.1},
                    "zlevel": 2, 
                    "data": [
                        {"coords": [geo_coord["阳江风电场群"], geo_coord["海上换流站(DRU)"]]},
                        {"coords": [geo_coord["海上换流站(DRU)"], geo_coord["陆上登陆点"]]},
                        {"coords": [geo_coord["陆上登陆点"], geo_coord["多端口断路器(Hub)"]]},
                        {"coords": [geo_coord["多端口断路器(Hub)"], geo_coord["大湾区负荷中心"]]}
                    ]
                },
                {
                    "type": "lines",
                    "coordinateSystem": "geo",
                    "lineStyle": {"color": "#a6c84c", "width": 6, "opacity": 0.3, "curveness": 0.1},
                    "zlevel": 1,
                    "data": [
                        {
                            "coords": [geo_coord["阳江风电场群"], geo_coord["海上换流站(DRU)"]], 
                            "name": "柔直海缆", 
                            "tooltip": {"formatter": tooltip_cable} # 为海缆独立注入卡片
                        },
                        {
                            "coords": [geo_coord["海上换流站(DRU)"], geo_coord["陆上登陆点"]], 
                            "name": "柔直海缆", 
                            "tooltip": {"formatter": tooltip_cable}
                        },
                        {
                            "coords": [geo_coord["陆上登陆点"], geo_coord["多端口断路器(Hub)"]], 
                            "name": "柔直海缆", 
                            "tooltip": {"formatter": tooltip_cable}
                        },
                        {
                            "coords": [geo_coord["多端口断路器(Hub)"], geo_coord["大湾区负荷中心"]], 
                            "name": "柔直海缆", 
                            "tooltip": {"formatter": tooltip_cable}
                        }
                    ]
                },
                {
                    "type": "scatter",
                    "coordinateSystem": "geo",
                    "label": {
                        "show": True, "position": "right", "formatter": "{b}", 
                        "color": "#fff", "fontSize": 10, "backgroundColor": "rgba(0,0,0,0.5)",
                        "padding": [2, 4], "borderRadius": 4
                    },
                    "zlevel": 3,
                    "data": [
                        # 【关键修复】还原真实的 name，将 HTML 放入局部的 tooltip 中
                        {
                            "name": "阳江风电场群", 
                            "value": geo_coord["阳江风电场群"], 
                            "symbol": icon_wind,
                            "symbolSize": 30, 
                            "itemStyle": {"color": "#00eaff"},
                            "label": {"formatter": "阳江风电场", "color": "#00eaff", "fontWeight": "bold"},
                            "tooltip": {"formatter": tooltip_wind}
                        },
                        {
                            "name": "海上换流站(DRU)", 
                            "value": geo_coord["海上换流站(DRU)"], 
                            "symbol": icon_converter,
                            "symbolSize": 25, 
                            "itemStyle": {"color": "#f4e925"}, 
                            "label": {"formatter": "海上换流站"},
                            "tooltip": {"formatter": tooltip_dru}
                        },
                        {
                            "name": "多端口断路器(Hub)", 
                            "value": geo_coord["多端口断路器(Hub)"], 
                            "symbol": icon_breaker,
                            "symbolSize": 30, 
                            "itemStyle": {"color": "#ff4d4f"}, 
                            "label": {"formatter": "多端口断路器"},
                            "tooltip": {"formatter": tooltip_hub}
                        },
                        {
                            "name": "大湾区负荷中心", 
                            "value": geo_coord["大湾区负荷中心"], 
                            "symbol": icon_city,
                            "symbolSize": 25, 
                            "itemStyle": {"color": "#52c41a"}, 
                            "label": {"formatter": "大湾区负荷"},
                            "tooltip": {"formatter": tooltip_load}
                        }
                    ]
                }
            ]
        }

    # ==========================================
    # 界面布局划分
    # ==========================================
    
    # 【获取实时北京时间】强制设置时区为 UTC+8
    beijing_tz = timezone(timedelta(hours=8))
    current_time_str = datetime.now(beijing_tz).strftime("%H:%M:%S")

    col_left, col_map, col_right = st.columns([1, 3, 1])

    with col_left:
        st.markdown("#### ⚡ 源端监测")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">北京时间</div>
            <div class="kpi-value" style="font-size: 24px; color: #00ffcc; letter-spacing: 2px;">{current_time_str}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">海上风速</div>
            <div class="kpi-value" style="color: #00eaff;">{current_wind:.1f} m/s</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">总输出功率</div>
            <div class="kpi-value" style="color: #f4e925;">{int(current_p)} MW</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 动态功率曲线
        fig_p = go.Figure(go.Scatter(
            y=st.session_state.history_p, mode='lines', 
            line=dict(color='#f4e925', width=2, shape='spline'),
            fill='tozeroy', fillcolor='rgba(244,233,37,0.15)'
        ))
        fig_p.update_layout(
            height=120, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False), yaxis=dict(range=[0, 4000], visible=False), 
            annotations=[dict(text="实时功率趋势", x=0, y=1.0, xref="paper", yref="paper", showarrow=False, font=dict(color='#aaa', size=12))]
        )
        st.plotly_chart(fig_p, use_container_width=True, config={'displayModeBar': False})
        
        btn_label = "⏸ 暂停演示" if st.session_state.auto_play else "▶ 播放演示 (局部刷新)"
        if st.button(btn_label):
            st.session_state.auto_play = not st.session_state.auto_play

    with col_map:
        # 强制更新组件 key 为 v2，以应用最新的结构
        st_echarts(options=st.session_state.static_map_option_v2, map=Map("china", map_data), height="550px", key="static_map_component_v2")

    with col_right:
        st.markdown("#### 🔋 网端监测")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">直流母线电压</div>
            <div class="kpi-value" style="color: #00ff00;">{current_u:.1f} kV</div>
            <div style="font-size:12px; opacity:0.7;">额定电压 ±500kV</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 动态电压微波曲线
        fig_u = go.Figure(go.Scatter(
            y=st.session_state.history_u, mode='lines', 
            line=dict(color='#00ff00', width=2, shape='spline'),
            fill='tozeroy', fillcolor='rgba(0,255,0,0.15)'
        ))
        fig_u.update_layout(
            height=120, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False), yaxis=dict(range=[495, 505], visible=False), 
            annotations=[dict(text="实时电压微波", x=0, y=1.0, xref="paper", yref="paper", showarrow=False, font=dict(color='#aaa', size=12))]
        )
        st.plotly_chart(fig_u, use_container_width=True, config={'displayModeBar': False})

        st.markdown(f"""
        <div class="kpi-card" style="margin-top: 15px;">
            <div class="kpi-title">设备健康度</div>
            <div class="kpi-value">99.8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # --- 触发循环刷新 ---
    if st.session_state.auto_play:
        time.sleep(1)
        st.session_state.play_index = (st.session_state.play_index + 1) % 24
        st.rerun()


elif st.session_state.page == "文件管理":
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


elif st.session_state.page == "故障检测":
    st.title("故障监测")
    st.success("系统状态：正常运行。构网型算法正在提供惯量支撑。")
    st.json({
        "实时健康分": 98,
        "最近故障预警": "无",
        "直流电压波动": "0.02%",
        "谐波畸变率": "1.2%"
    })

# ============================
# 故障发生
# ============================
elif st.session_state.page == "故障发生":
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


elif page == "4. 使用说明":
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

# 渲染悬浮 AI 助手
render_floating_ai()