import streamlit as st
from RAG import QueryEngine

st.title("營業稅智能問答系統")

st.write("有任何有關營業稅的問題都可以來問我喔 🚀")

# Streamlit 提供的一个裝飾器，用于緩存返回全局資源（如數據連接、機器學習模型等）的函數。
@st.cache_resource

#在進入頁面，第一步先載入模型
def load_engine():
    return QueryEngine("clean.csv")

#st.session_state 是一個「跨 rerun 記憶體」。
#是在 Streamlit 裡檢查 session_state 裡有沒有某個變數（key）
if "query_engine" not in st.session_state:
    placeholder = st.empty()
    placeholder.write("載入問答集")
    st.session_state.query_engine = load_engine() #初始化資料庫模型
    placeholder.write("✔ done")

#初始化訊息串列，將後續的結果都放進該串列中，讓畫面可以渲染之前的資料。
if "messages" not in st.session_state:
    st.session_state.messages = []

#根據角色(提問者、機器人)將之前的結果顯示在畫面上
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#提問者的資料
if prompt := st.chat_input("任何營業稅的問題都可以問我唷"): #設一變數prompt儲存提問者的問題
    st.session_state.messages.append({"role": "user", "content": prompt}) #提問者的問題存進訊息串列中
    with st.chat_message("user"):
        st.markdown(prompt) #問題顯示在畫面上

    query_engine = st.session_state.query_engine
    #設另一變數query_engine把session_state裡的query_engine拿出來使用

    with st.chat_message("assistant"):

        with st.spinner("思考中（計算向量 + 比對中）..."):

            response = query_engine.query(prompt) #使用query方法把所提問題和問題資料庫做比對，得出解答

        answer_text = f"""
        以下為相關條目
        """

        # 將相似度近的前3個問題使用 loop 組成文字區塊
        for i, item in enumerate(response, start=1):

            answer_text += f"""

        {i}、{item["question"]}

        {item["answer"]}
       
        ---
        """

        # 顯示
        st.markdown(answer_text)

        # 答案存進聊天紀錄
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text
        })