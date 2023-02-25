# _*_ coding : utf-8 _*_
# @Time : 2022/5/9 15:02
# @Author : miaosite

#起点畅销榜单
#第一页https://www.qidian.com/rank/hotsales/
#第二页https://www.qidian.com/rank/hotsales/page2/
#第三页https://www.qidian.com/rank/hotsales/page3/
#第五页https://www.qidian.com/rank/hotsales/page5/
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import xlwt
import sqlite3
def create_request(page):
    if page == 1:
        url = 'https://www.qidian.com/rank/hotsales/'
    else:
        url = 'https://www.qidian.com/rank/hotsales/'+'page'+str(page)+'/'
    print(url)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    request = urllib.request.Request(url=url,headers=headers)
    return request

def get_content(request):
    try:
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        #print(content)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,"resson"):
            print(e.reason)
    return content

#几个正则查找规则的全局变量

findbookName = re.compile(r'<h2><a data-bid.*?>(.*?)</a></h2>',re.S)
findbookWriter = re.compile(r'<a class="name" data-eid="qd_C41".*?>(.*?)</a><em>',re.S)
findbookType = re.compile(r'<a data-eid="qd_C42".*?>(.*?)</a><i>·</i><a class.*?>.*?</a>',re.S)
findbookIntro = re.compile(r'<p class="intro">(.*?) </p>',re.S)
findbookUpate = re.compile(r'<p class="update"><a data-bid.*?>(.*?)</a>',re.S)
findlastUpdate = re.compile(r'<em>·</em><span>(.*?)</span>',re.S)
findbookLink = re.compile(r'<h2><a data-bid=.*?href=(.*?)target=.*? title=.*?>',re.S)

datalist = []
def analysis(content):
    soup = BeautifulSoup(content,'html.parser')
    #datalist=[]         #保存全部小说的信息
    for item in soup.find_all('div',class_="book-mid-info"):#查找符合要求的项目，形成列表
        # print(item)
        data =[]        #保存每一部小说的信息
        item = str(item)


        bookName= re.findall(findbookName,item)[0]
        #print(bookName)
        data.append(bookName)

        bookWriter = re.findall(findbookWriter,item)[0]
        #print(bookWriter)
        data.append(bookWriter)

        bookType = re.findall(findbookType,item)[0]
        #print(bookType)
        data.append(bookType)

        bookIntro = re.findall(findbookIntro,item)[0]
        #print(bookIntro)
        data.append(bookIntro)

        bookUpate = re.findall(findbookUpate,item)[0]
        #print(bookUpate)
        data.append(bookUpate)

        lastUpdate = re.findall(findlastUpdate,item)[0]
        # print(lastUpdate)
        data.append(lastUpdate)

        bookLink = re.findall(findbookLink,item)[0]
        data.append(bookLink)

        datalist.append(data)
    #print(datalist)
    return datalist


def saveData(cols,bookdata):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('起点畅销排行top100',cell_overwrite_ok=True)
    column = ("书名","作者","类型","简介","最新章节","最近更新时间","链接")
    for i in range(0,7):
        sheet.write(0,i,column[i])      #表头的列名
    for i in range(0,cols):
        print("第%d条" %i)
        data = bookdata[i]
        for j in range(0,7):
              sheet.write(i+1,j,data[j])
    book.save('book1.xls')


def savaDataDB(bookdata,dbpath):
    create_db(dbpath)
    print('数据库已经建立完成')
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in bookdata:
        for index in range(len(data)):
            if index == 6:
                continue

            data[index] = '"'+data[index]+'"'
        sql = '''
                insert into book100 (
                bookname,bookwriter,booktype,bookinfo,bookupdate,lastupdate,booklink) 
                values(%s)'''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()






def create_db(dbpath):            #数据库的创建和初始化
    sql = '''
            create table book100
            (
            id integer primary key autoincrement,
            bookname varchar,
            bookwriter varchar,
            booktype varchar,
            bookinfo text,
            bookupdate text,
            lastupdate text ,
            booklink text
            )

    '''  # 创建数据表
    con = sqlite3.connect(dbpath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()



if __name__ == '__main__':
    start_page = int(input('please enter first page:'))
    end_page = int(input('please enter last page'))
    cols = (end_page - start_page + 1)*20    #确定Excel表里应该有多少行
    print(cols)
    #print(cols)
    for page in range(start_page,end_page+1):
        request = create_request(page)      #请求对象的定制
        content = get_content(request)      #获取相应数据,下一步就可以进行数据的解析和保存了
        bookdata = analysis(content)                          #数据解析和正则提取
    print(bookdata)
    saveData(cols,bookdata)                  #将数据保存在Excel里
    dbpath = 'book.db'
    #create_db(dbpath)
   # print('数据库已经建立完成')
    savaDataDB (bookdata,dbpath)                   #将数据保存在数据库

