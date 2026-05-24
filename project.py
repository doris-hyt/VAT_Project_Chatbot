import pandas as pd
# 幫我把檔案csv轉成utf-8格式，以利讓系統可以抓取資料
# import sys
# print(sys.executable)

df = pd.read_csv("國稅問與答營業稅.csv", encoding="utf-8", engine="python")

df.to_csv("clean.csv", index=False, encoding="utf-8-sig")
