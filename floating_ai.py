import streamlit as st
from openai import OpenAI
import time
# --- RAG 必需的依赖库 ---
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# =========================================================
# 0. 核心模块：加载本地向量知识库 (之前缺失的就是这一段)
# =========================================================
@st.cache_resource
def load_knowledge_base():
    # 使用与 build_rag.py 中相同的模型
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    # 加载已生成的 faiss_index 文件夹
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db


# =========================================================
# 1. 主函数：渲染悬浮助手界面与交互逻辑
# =========================================================
def render_floating_ai():
    # --- CSS 样式注入 ---
    st.markdown("""
    <style>
        /* 锁定 Popover 的外壳，强行钉在屏幕右下角 */
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 40px !important;
            right: 40px !important;
            width: 65px !important;  
            height: 65px !important; 
            z-index: 999999 !important;
            background-color: transparent !important;
        }

        /* 将按钮改造成科技感悬浮球 */
        div[data-testid="stPopover"] > button {
            width: 100% !important;
            height: 100% !important;
            border-radius: 50% !important; 
            background: linear-gradient(135deg, #0078D4, #005a9e) !important; 
            border: 2px solid #ffffff !important; 
            box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important; 
            padding: 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            transition: all 0.3s ease !important; 
        }

        /* 鼠标放上去时的放大动画 */
        div[data-testid="stPopover"] > button:hover {
            transform: scale(1.1) !important;
        }

        /* 强行隐藏自带的向下小箭头 */
        div[data-testid="stPopover"] > button svg, 
        div[data-testid="stPopover"] > button span[data-testid="stDropzoneIcon"] {
            display: none !important;
        }

        /* 让里面的机器人 Emoji 完美居中并放大 */
        div[data-testid="stPopover"] > button p {
            font-size: 32px !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }

        /* 气泡弹出框的位置约束 */
        div[data-testid="stPopoverBody"] {
            position: fixed !important; 
            bottom: 120px !important; 
            right: 40px !important;   
            width: 380px !important;  
            max-height: 70vh !important; 
            border-radius: 16px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3) !important;
            border: 1px solid #444 !important; 
            z-index: 999999 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- UI 渲染与对话流 ---
    with st.popover("🤖", use_container_width=False):
        st.markdown("### ⚡ 智多星助手")
        st.caption("已连接深远海风电知识库")
        st.divider()

        # 初始化历史记录
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = [
                {"role": "assistant", "content": "你好！我是本平台的智能助手。请问关于直流短路故障或系统电压有什么我可以帮你的？"}
            ]

        # 聊天记录容器
        chat_container = st.container(height=350)
        with chat_container:
            for msg in st.session_state.ai_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # 输入框处理
        if prompt := st.chat_input("请输入问题...", key="floating_chat_input_final"):
            st.session_state.ai_messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
            
            with chat_container:
                with st.chat_message("assistant"):
                    if "DEEPSEEK_API_KEY" not in st.secrets:
                        error_msg = "⚠️ 平台未检测到 DEEPSEEK_API_KEY！请在项目根目录创建 `.streamlit/secrets.toml` 文件配置密钥。"
                        st.error(error_msg)
                        st.session_state.ai_messages.append({"role": "assistant", "content": error_msg})
                    else:
                        try:
                            # 1. 翻阅知识库
                            with st.spinner("📚 正在翻阅风电知识库..."):
                                db = load_knowledge_base()
                                search_docs = db.similarity_search(prompt, k=3)
                                context = "\n\n".join([doc.page_content for doc in search_docs])
                            
                            # 2. 调用大模型
                            with st.spinner("🤖 智多星正在思考..."):
                                rag_prompt = f"""你是一个深远海风电电气工程专家。
                                请严格根据以下【参考资料】回答【用户问题】。
                                如果参考资料中没有相关答案，请直接回答“知识库中未找到相关内容”，不要随意编造。
                                
                                【参考资料】：
                                {context}
                                
                                【用户问题】：
                                {prompt}
                                """
                                
                                # 将带知识库的 Prompt 伪装成最后一条用户消息发给 API
                                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.ai_messages[:-1]]
                                api_messages.append({"role": "user", "content": rag_prompt})
                                
                                client = OpenAI(
                                    api_key=st.secrets["DEEPSEEK_API_KEY"],
                                    base_url="https://api.deepseek.com"
                                )
                                stream = client.chat.completions.create(
                                    model="deepseek-chat",
                                    messages=api_messages,
                                    stream=True,
                                )
                                response = st.write_stream(stream)
                                st.session_state.ai_messages.append({"role": "assistant", "content": response})
                        
                        except Exception as e:
                            error_msg = f"🚨 运行中断，后台报错信息: {e}"
                            st.error(error_msg)
                            st.session_state.ai_messages.append({"role": "assistant", "content": error_msg})
            
            st.rerun()