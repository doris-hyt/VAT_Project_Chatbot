import csv
from sentence_transformers import SentenceTransformer, util

# 初始化物件。先讓系統讀取csv檔案將所需資料整理成串列
class QueryEngine:
   def __init__(self,csv_files):
      self.model = None
      self.faq_embeddings = None

      self.RequestQuestion=[] #初始化問題串列
      self.RequestAnswer=[] #初始化答案串列
      
      #讀取CSV
      with open(csv_files,mode="r",newline="",encoding="utf-8") as files:
        reader=csv.reader(files)
        next(reader,None)# 跳過標題列
        #讀取每一列資料，將問題及答案各自編列成串列        
        for row in reader:
              Question=row[3]
              Answer=row[4]
              self.RequestQuestion.append(Question)
              self.RequestAnswer.append(Answer)
      
       

   def _load_model(self):  #建立模型方法，等到輸入問題後才載入embedding模型
        if self.model is None:
            self.model = SentenceTransformer(
                "paraphrase-multilingual-MiniLM-L12-v2"
            )

        return self.model


    # 🔥 lazy embedding
   def _get_embeddings(self): #轉成向量資料的方法
        if self.faq_embeddings is None:
            model = self._load_model() #建立模型
            self.faq_embeddings = model.encode(
                self.RequestQuestion,
                show_progress_bar=False
            )
            #將先前的問題串列轉成向量

        return self.faq_embeddings
   
   def query(self,user_question): #尋找所提問題最佳問題解 
    #   model = self._load_model()

      #執行將問答集的問題轉化成向量資料
      faq_embeddings = self._get_embeddings()
      
     
      #將使用者問題轉embedding
      user_embedding = self.model.encode(user_question)

      #計算相似度
      scores = util.cos_sim(user_embedding, faq_embeddings)

      # 取前3名相似度近的問題及答案
      top_results = scores[0].topk(3)

      results = []

      for score, idx in zip(
         top_results.values,
         top_results.indices
      ):

         results.append({
               "question": self.RequestQuestion[idx],
               "answer": self.RequestAnswer[idx],
               "score": score.item()
         })

      return results

   

