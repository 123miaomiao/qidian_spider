# qidian_spider
本次的爬虫项目实现了数据爬取、解析、储存、分析和可视化等需求。本项目整体使用了Python语言，爬取的目标是起点中文网，目的是获得其畅销榜单的100部小说的相关信息（排行，书名，作者，书籍类型，简介，最新章节，最近更新时间和书籍链接），然后在网页上进行相应的分析和可视化。

有两个文件夹，spider_qidian是对目标网站数据的爬取处理并将数据保存在excel和数据库中，flask_qidian则是对数据库中数据处理和可视化。
本次项目实现的大致功能：
（1）网页爬取。采用Python中的urlib库连接并且爬取了起点中文网畅销榜单，获得了需要的内容。
（2）数据解析。利用了BeautifulSoup和正则式对获取的网页内容进行了解析，拿到我们需要的信息（排行，书名，作者，书籍类型，简介，最新章节，最近更新时间和书籍链接）。
（3）数据存储。将拿到的数据保存在了Excel文件中同时也利用sqlite3库将相关的数据保存在了数据库中，以便于之后数据的利用。
（4）数据分析。利用flask框架构造了一个本地的网站，再次利用sqlite3操作数据库进行数据分析并且在网页上进行了展示。
数据可视化。通过echarts对书籍类型分布情况绘制了柱状图，然后又用wordcloud完成了对书籍简介词频分析和图像的制作，同时进行了展示。
display:
![image](https://github.com/123miaomiao/qidian_spider/blob/main/img/img1.png)
![image](https://github.com/123miaomiao/qidian_spider/blob/main/img/img2.png)
![image](https://github.com/123miaomiao/qidian_spider/blob/main/img/img3.png)
![image](https://github.com/123miaomiao/qidian_spider/blob/main/img/img4.png)
![image](https://github.com/123miaomiao/qidian_spider/blob/main/img/img5.png)
