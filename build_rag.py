import os
from langchain_community.document_loaders import Docx2txtLoader, UnstructuredPowerPointLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_db():
    print("1. 正在扫描 data 目录下的文档...")
    docs = []
    data_dir = "data/"
    
    # 确保 data 文件夹存在
    if not os.path.exists(data_dir):
        print(f"错误：找不到 {data_dir} 文件夹！")
        return

    # 遍历文件夹，智能匹配不同格式的文件
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        
        try:
            if filename.endswith(".docx"):
                print(f"   -> 正在读取 Word: {filename}")
                loader = Docx2txtLoader(filepath)
                docs.extend(loader.load())
            elif filename.endswith(".pptx"):
                print(f"   -> 正在读取 PPT: {filename}")
                loader = UnstructuredPowerPointLoader(filepath)
                docs.extend(loader.load())
            elif filename.endswith(".pdf"):
                print(f"   -> 正在读取 PDF: {filename}")
                loader = PyPDFLoader(filepath)
                docs.extend(loader.load())
        except Exception as e:
            print(f"   ❌ 读取 {filename} 时出错: {e}")

    if not docs:
        print("\n错误：没有在 data 目录下找到任何支持的文档内容！请确保文件不是空的，且格式为 docx/pptx/pdf。")
        return

    print(f"\n2. 成功读取内容，正在将文档切分成知识块...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)

    print("3. 正在加载本地嵌入模型 (初次运行需下载模型，请耐心等待)...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

    print("4. 正在生成向量数据库...")
    db = FAISS.from_documents(chunks, embeddings)
    
    db.save_local("faiss_index")
    print("✅ 知识库构建完成！已保存在 faiss_index 文件夹中。")

if __name__ == "__main__":
    create_vector_db()