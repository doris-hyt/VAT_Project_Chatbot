# VAT_Project_Chatbot

## 使用SentenceTransformer模型製作簡易型問答系統

https://vat-project-chatbot.streamlit.app/
1. 至政府公開資料平台下載稅務問答集檔案。
2. 使用python內的pandas模組將檔案內的問題及答案讀取出來。
3. 利用Sentence-Transformers模型將資料集問題轉換為固定維度數值向量（Embedding），同時使用者的問題也轉化為向量進行比對，選出相似度最高的三個問題及答案。
4. 使用Streamlit 製作聊天機器人的介面設計。
