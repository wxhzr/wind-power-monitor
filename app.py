import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# ----------------------------
# 1. 页面配置
# ----------------------------
st.set_page_config(
    page_title="深远海风电构网型监测平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 2. 全局 CSS 优化（含导航栏对齐与卡片样式）
# ----------------------------
st.markdown("""
<style>
    /* 统一导航栏对齐：解决 Button 和 Expander 宽度不一致 */
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

# 主目录 5
if st.sidebar.button("5. AI 助手"):
    st.session_state.page = "5. AI 助手"

# ----------------------------
# 4. 页面分发
# ----------------------------
page = st.session_state.page

if page == "1. 平台首页":
    st.title("深远海风电构网型控制监测平台")
    st.info("欢迎。本项目旨在研究深远海风电在弱网环境下的构网型控制策略稳定性。")
    st.image("https://via.placeholder.com/1000x300.png?text=Platform+Overview", use_column_width=True)

# ============================
# 2.1 实时监测 (根据你的截图修改)
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

# 其他占位页面
elif st.session_state.page == "拓扑结构":
    st.title("系统拓扑连接")
    st.markdown("""
    ### 构网型送出系统逻辑架构
    通过下方拓扑图可以观察从源端到网端的能量流向。
    """)
    # Mermaid 流程图展现专业感
    st.markdown("""
    ```mermaid
    graph LR
        A[PMSG风机群] -- 交流 --> B(机侧换流器 MSC)
        B -- 直流 --> C{直流集电系统}
        C -- 直流 --> D(网侧换流器 VSC)
        D -- 直流海缆 --> E(陆上换流站)
        E -- 构网型控制 --> F[交流弱电网 SCR<3]
    ```
    """)
    st.info("注：点击节点可查看详细参数（开发中）。")

elif st.session_state.page == "文件管理":
    st.title("文件管理与分析")
    
    # 顶部的分析 KPI
    st.subheader("历史仿真性能摘要")
    c1, c2, c3 = st.columns(3)
    c1.metric("平均电压跌落深度", "12.4%", "-2.1%")
    c2.metric("频率恢复耗时", "0.42 s", "-0.05 s")
    c3.metric("VSG阻尼比评估", "0.707", "优")
    
    # 上传组件
    uploaded_file = st.file_uploader("上传仿真数据 (.csv, .xlsx)", type=["csv", "xlsx"])
    
    # 模拟展示一张数据表
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
# 3.2 故障发生
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
        # 模拟故障恢复曲线
        t_f = np.linspace(0, 5, 100)
        v_f = np.ones(100)
        v_f[20:40] = 0.4  # 跌落
        v_f[40:70] = 0.4 + 0.6*(t_f[40:70]-0.4) # 恢复
        fig_f = go.Figure(go.Scatter(x=t_f, y=v_f, name="电压恢复曲线", line=dict(color='red')))
        fig_f.update_layout(title="故障恢复能力分析", xaxis_title="时间", yaxis_title="标幺值电压")
        st.plotly_chart(fig_f, use_container_width=True)

elif page == "4. 使用说明":
    col_doc, col_toc = st.columns([4, 1])
    with col_doc:
        st.header("1. 欢迎使用")
        st.write("这是系统手册正文...")
    with col_toc:
        st.markdown('<div class="toc-box"><b>目录索引</b><br><a href=" ">1. 欢迎使用</a ></div>', unsafe_allow_html=True)

elif page == "5. AI 助手":
    st.title("🤖 智能助教")
    st.chat_input("询问关于构网型控制的问题...")