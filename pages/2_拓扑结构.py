import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from streamlit_echarts import st_echarts
from datetime import datetime, timezone, timedelta

# 引入抽离的公共组件
from utils.common import set_page_style
from floating_ai import render_floating_ai

set_page_style()

# --- [UI] 顶部状态栏 ---
col_header_1, col_header_2 = st.columns([4, 1])
with col_header_1:
    st.markdown("### 🌐 深远海风电多端柔直送出系统 - 实时拓扑监控")
with col_header_2:
    st.markdown(
        "<div style='background-color:rgba(0, 255, 0, 0.1); border:1px solid #00ff00; border-radius:5px; padding:5px; text-align:center; color:#00ff00; font-weight:bold;'>● 集群状态: 并网稳定运行</div>", 
        unsafe_allow_html=True
    )

# --- 初始化基础数据 ---
if 'sim_data' not in st.session_state:
    x = np.linspace(0, 4 * np.pi, 24) 
    wind_wave = 10 + 8 * np.sin(x)    
    power_wave = wind_wave * 200      
    st.session_state.sim_data = pd.DataFrame({"Wind_Speed": wind_wave, "Power_Total": power_wave})
    st.session_state.play_index = 0 

if 'history_u' not in st.session_state:
    st.session_state.history_u = [500.0] * 20 
    st.session_state.history_p = [2000.0] * 20 

if 'auto_play' not in st.session_state:
    st.session_state.auto_play = True 

# ==========================================
# 动态生成拓扑图配置 (1对1 升级为 3对2 多端拓扑)
# ==========================================
def get_dynamic_topology_option(flow_period, current_wind, current_p):
    # 【核心升级1】：重新设计二维坐标，呈现完美的树状分支拓扑
    node_coord = {
        "风电场一期": [111.5, 22.5],
        "风电场二期": [111.5, 21.5],
        "风电场三期": [111.5, 20.5],
        "海上换流站(DRU)": [112.3, 21.5],
        "陆上登陆点": [112.8, 21.5],
        "多端口断路器(Hub)": [113.3, 21.5],
        "广州负荷中心": [114.1, 22.3],
        "深圳负荷中心": [114.1, 20.7]
    }
    
    icon_wind = "path://M12,2L12,2c0.55,0,1,0.45,1,1v8.59l6.07-6.07c0.39-0.39,1.02-0.39,1.41,0l0,0c0.39,0.39,0.39,1.02,0,1.41L14.41,13 H23c0.55,0,1,0.45,1,1l0,0c0,0.55-0.45,1-1,1h-8.59l6.07,6.07c0.39,0.39,0.39,1.02,0,1.41l0,0c-0.39,0.39-1.02,0.39-1.41,0 L13,16.41V25c0,0.55-0.45,1-1,1l0,0c-0.55,0-1-0.45-1-1v-8.59l-6.07,6.07c-0.39,0.39-1.02,0.39-1.41,0l0,0 c-0.39-0.39-0.39-1.02,0-1.41L9.59,15H1c-0.55,0-1-0.45-1-1l0,0c0-0.55,0.45-1,1-1h8.59L3.52,6.93C3.13,6.54,3.13,5.91,3.52,5.52l0,0 c0.39-0.39,1.02-0.39,1.41,0L11,11.59V3C11,2.45,11.45,2,12,2z"
    icon_converter = "path://M3,3v18h18V3H3z M19,19H5V5h14V19z M12,7l-3,3h2v4H9l3,3l3-3h-2v-4h2L12,7z"
    icon_breaker = "path://M12 2L2 12l10 10 10-10L12 2zm0 16l-6-6 6-6 6 6-6 6z"
    icon_city = "path://M12,3L2,12h3v8h6v-6h2v6h6v-8h3L12,3z"

    def make_canvas_rich_label(title, params_dict, pos="right"):
        formatter_str = f"{{title|{title}}}\n{{hr|}}"
        for k, v in params_dict.items():
            if isinstance(v, tuple):
                val_str, style = v
            else:
                val_str, style = v, "val"
            formatter_str += f"\n{{name|{k}}}{{{style}|{val_str}}}"

        return {
            "show": True,
            "position": pos, 
            "distance": 15,
            "formatter": formatter_str,
            "backgroundColor": "rgba(20,30,50,0.95)",
            "borderColor": "#00eaff",
            "borderWidth": 1,
            "borderRadius": 8,
            "padding": 12,
            "zIndex": 999,
            "rich": {
                "title": {"color": "#00eaff", "fontSize": 14, "fontWeight": "bold", "lineHeight": 24, "align": "left"},
                "hr": {"borderColor": "rgba(255,255,255,0.2)", "width": "100%", "borderWidth": 1, "height": 0, "lineHeight": 10},
                "name": {"color": "#aaa", "fontSize": 12, "lineHeight": 20, "align": "left", "width": 85},
                "val": {"color": "#fff", "fontSize": 12, "fontWeight": "bold", "lineHeight": 20, "align": "right", "width": 90},
                "val_wind": {"color": "#00eaff", "fontSize": 12, "fontWeight": "bold", "lineHeight": 20, "align": "right", "width": 90},
                "val_power": {"color": "#f4e925", "fontSize": 12, "fontWeight": "bold", "lineHeight": 20, "align": "right", "width": 90}
            }
        }
    
    # 构建海缆专用的悬浮卡片
    cable_label_dc = make_canvas_rich_label("柔直高压海缆", {"电压等级": "±500 kV", "线缆截面": "1×2500 mm²", "最大输送功率": "2215 MVA", "线路电阻": "2.0 Ω"}, "middle")
    cable_label_ac = make_canvas_rich_label("交流汇集海缆", {"电压等级": "66 kV", "传输状态": "运行正常", "海缆类型": "三芯海底电缆"}, "middle")

    # 【核心升级2】：定义所有连接线路 (共 7 条线)
    link_coords = [
        {"coords": [node_coord["风电场一期"], node_coord["海上换流站(DRU)"]]},
        {"coords": [node_coord["风电场二期"], node_coord["海上换流站(DRU)"]]},
        {"coords": [node_coord["风电场三期"], node_coord["海上换流站(DRU)"]]},
        {"coords": [node_coord["海上换流站(DRU)"], node_coord["陆上登陆点"]]},
        {"coords": [node_coord["陆上登陆点"], node_coord["多端口断路器(Hub)"]]},
        {"coords": [node_coord["多端口断路器(Hub)"], node_coord["广州负荷中心"]]},
        {"coords": [node_coord["多端口断路器(Hub)"], node_coord["深圳负荷中心"]]}
    ]

    return {
        "backgroundColor": '#0E1116',
        "tooltip": {"show": False}, 
        "grid": {"top": 40, "bottom": 40, "left": 60, "right": 100},
        "xAxis": {"type": "value", "show": False, "min": 110.5, "max": 115.0}, 
        "yAxis": {"type": "value", "show": False, "min": 19.5, "max": 23.5},
        "dataZoom": [{"type": "inside", "xAxisIndex": 0, "yAxisIndex": 0}],
        "series": [
            {
                "type": "lines", "coordinateSystem": "cartesian2d", 
                "silent": True, 
                "effect": {"show": True, "period": flow_period, "trailLength": 0.6, "color": "#00ffcc", "symbol": "arrow", "symbolSize": 8},
                "lineStyle": {"color": "#a6c84c", "width": 0, "curveness": 0.1}, "zlevel": 2, 
                "data": link_coords  # 应用所有7条飞线
            },
            {
                "type": "lines", "coordinateSystem": "cartesian2d", 
                "silent": False, 
                "lineStyle": {"color": "#a6c84c", "width": 6, "opacity": 0.3, "curveness": 0.1}, "zlevel": 1,
                "data": [
                    {"coords": link_coords[0]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_ac}},
                    {"coords": link_coords[1]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_ac}},
                    {"coords": link_coords[2]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_ac}},
                    {"coords": link_coords[3]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_dc}},
                    {"coords": link_coords[4]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_dc}},
                    {"coords": link_coords[5]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_dc}},
                    {"coords": link_coords[6]["coords"], "emphasis": {"lineStyle": {"width": 10, "opacity": 0.8}, "label": cable_label_dc}}
                ]
            },
            {
                "type": "scatter", "coordinateSystem": "cartesian2d", 
                "animationDurationUpdate": 0, 
                # 调整基础标签位置防重叠
                "label": {"show": True, "position": "right", "formatter": "{b}", "color": "#fff", "fontSize": 12, "backgroundColor": "rgba(0,0,0,0.5)", "padding": [4, 6], "borderRadius": 4},
                "zlevel": 3,
                "data": [
                    # 【核心升级3】：独立配置3个风电场，风速略有扰动，功率按比例分配
                    {
                        "name": "风电场一期", "value": node_coord["风电场一期"], "symbol": icon_wind, "symbolSize": 35, "itemStyle": {"color": "#00eaff"},
                        "label": {"show": True, "position": "left"}, # 标签放左边防遮挡
                        "emphasis": {"label": make_canvas_rich_label("阳江一期风电场", {
                            "实时风速": (f"{current_wind:.1f} m/s", "val_wind"),
                            "贡献功率": (f"{int(current_p * 0.35)} MW", "val_power"),
                            "装机容量": "1750 MVA"
                        }, "left")}
                    },
                    {
                        "name": "风电场二期", "value": node_coord["风电场二期"], "symbol": icon_wind, "symbolSize": 35, "itemStyle": {"color": "#00eaff"},
                        "label": {"show": True, "position": "left"},
                        "emphasis": {"label": make_canvas_rich_label("阳江二期风电场", {
                            "实时风速": (f"{current_wind + 0.2:.1f} m/s", "val_wind"),
                            "贡献功率": (f"{int(current_p * 0.35)} MW", "val_power"),
                            "装机容量": "1750 MVA"
                        }, "left")}
                    },
                    {
                        "name": "风电场三期", "value": node_coord["风电场三期"], "symbol": icon_wind, "symbolSize": 35, "itemStyle": {"color": "#00eaff"},
                        "label": {"show": True, "position": "left"},
                        "emphasis": {"label": make_canvas_rich_label("阳江三期风电场", {
                            "实时风速": (f"{current_wind - 0.3:.1f} m/s", "val_wind"),
                            "贡献功率": (f"{int(current_p * 0.30)} MW", "val_power"),
                            "装机容量": "1500 MVA"
                        }, "left")}
                    },
                    
                    {
                        "name": "海上换流站", "value": node_coord["海上换流站(DRU)"], "symbol": icon_converter, "symbolSize": 30, "itemStyle": {"color": "#f4e925"}, 
                        "label": {"show": True, "position": "bottom"},
                        "emphasis": {"label": make_canvas_rich_label("海上换流站(DRU)", {"额定电压": "±500 kV", "总送出功率": (f"{int(current_p)} MW", "val_power"), "子模块数量": "200"}, "bottom")}
                    },
                    {
                        "name": "多端口Hub", "value": node_coord["多端口断路器(Hub)"], "symbol": icon_breaker, "symbolSize": 35, "itemStyle": {"color": "#ff4d4f"}, 
                        "label": {"show": True, "position": "bottom"},
                        "emphasis": {"label": make_canvas_rich_label("多端口断路器(Hub)", {"分流模式": "双极对称", "动作时间": "3 ms", "关键功能": "主动限流/故障隔离"}, "bottom")}
                    },
                    
                    # 【核心升级4】：独立配置2个负荷中心
                    {
                        "name": "广州负荷", "value": node_coord["广州负荷中心"], "symbol": icon_city, "symbolSize": 35, "itemStyle": {"color": "#52c41a"}, 
                        "emphasis": {"label": make_canvas_rich_label("广州负荷中心", {"受端系统容量": "6000 MVA", "受端系统惯量": "3 s", "供电状态": "稳定"}, "right")}
                    },
                    {
                        "name": "深圳负荷", "value": node_coord["深圳负荷中心"], "symbol": icon_city, "symbolSize": 35, "itemStyle": {"color": "#52c41a"}, 
                        "emphasis": {"label": make_canvas_rich_label("深圳负荷中心", {"受端系统容量": "4000 MVA", "受端系统惯量": "2.5 s", "供电状态": "稳定"}, "right")}
                    }
                ]
            }
        ]
    }

# ==========================================
# 核心大一统：整体 Dashboard 同步刷新
# ==========================================
@st.fragment(run_every=1 if st.session_state.auto_play else None)
def render_dashboard():
    if st.session_state.auto_play:
        st.session_state.play_index = (st.session_state.play_index + 1) % 24

    idx = st.session_state.play_index
    current_row = st.session_state.sim_data.iloc[idx]
    
    current_wind = current_row['Wind_Speed']
    current_p = current_row['Power_Total']
    current_u = round(500.0 + np.random.uniform(-0.5, 0.5), 1) 
    
    st.session_state.history_p.append(current_p)
    st.session_state.history_p.pop(0)
    st.session_state.history_u.append(current_u)
    st.session_state.history_u.pop(0)
    
    dynamic_flow_period = max(0.8, 4.5 - current_wind * 0.18)
    
    col_left, col_map, col_right = st.columns([1, 3, 1])

    with col_left:
        beijing_tz = timezone(timedelta(hours=8))
        current_time_str = datetime.now(beijing_tz).strftime("%H:%M:%S")

        st.markdown("#### ⚡ 源端集群监测")
        st.markdown(f"""
        <div class="kpi-card"><div class="kpi-title">北京时间</div><div class="kpi-value" style="font-size: 24px; color: #00ffcc;">{current_time_str}</div></div>
        <div class="kpi-card"><div class="kpi-title">集群平均风速</div><div class="kpi-value" style="color: #00eaff;">{current_wind:.1f} m/s</div></div>
        <div class="kpi-card"><div class="kpi-title">集群总功率</div><div class="kpi-value" style="color: #f4e925;">{int(current_p)} MW</div></div>
        """, unsafe_allow_html=True)
        
        fig_p = go.Figure(go.Scatter(y=st.session_state.history_p, mode='lines', line=dict(color='#f4e925', width=2, shape='spline'), fill='tozeroy', fillcolor='rgba(244,233,37,0.15)'))
        fig_p.update_layout(height=120, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(range=[0, 4000], visible=False))
        st.plotly_chart(fig_p, width="stretch", config={'displayModeBar': False}, key="fig_p")

    with col_map:
        dynamic_topology_opt = get_dynamic_topology_option(dynamic_flow_period, current_wind, current_p)
        st_echarts(options=dynamic_topology_opt, height="550px", key="fixed_topology_component")

    with col_right:
        st.markdown("#### 🔋 网端分配监测")
        st.markdown(f"""
        <div class="kpi-card"><div class="kpi-title">直流母线电压</div><div class="kpi-value" style="color: #00ff00;">{current_u:.1f} kV</div><div style="font-size:12px; opacity:0.7;">额定电压 ±500kV</div></div>
        """, unsafe_allow_html=True)
        
        fig_u = go.Figure(go.Scatter(y=st.session_state.history_u, mode='lines', line=dict(color='#00ff00', width=2, shape='spline'), fill='tozeroy', fillcolor='rgba(0,255,0,0.15)'))
        fig_u.update_layout(height=120, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(range=[495, 505], visible=False))
        st.plotly_chart(fig_u, width="stretch", config={'displayModeBar': False}, key="fig_u")

        st.markdown('<div class="kpi-card" style="margin-top: 15px;"><div class="kpi-title">全网健康度</div><div class="kpi-value">99.8%</div></div>', unsafe_allow_html=True)

# 渲染顶部控制按钮
btn_label = "⏸ 暂停演示" if st.session_state.auto_play else "▶ 播放演示"
if st.button(btn_label):
    st.session_state.auto_play = not st.session_state.auto_play
    st.rerun()

# 运行整合后的面板
render_dashboard()

# 渲染 AI 悬浮球
render_floating_ai()