# _*_ coding : utf-8 _*_
# @Time : 2022/5/11 22:56
# @Author : miaosite


import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3



con = sqlite3.connect("book.db")
cur = con.cursor()
sql = "select bookinfo from book100;"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
#print(text)
cur.close()
con.close()


cut = jieba.cut(text)
string = ' '.join(cut)
print(len(string))

img = Image.open(r'.\static\assets\img\gui.jpg')
img_array = np.array(img)

wc = WordCloud(
    background_color="white",
    mask=img_array,
    font_path="STXINWEI.TTF"
)
wc.generate_from_text(string)


#绘图
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
#plt.show()
plt.savefig(r'.\static\assets\img\wordcloud.jpg')