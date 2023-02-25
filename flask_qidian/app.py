from flask import Flask,render_template
import sqlite3
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/bookdata')
def bookdata():
    datalist = []
    con = sqlite3.connect("book.db")
    cur = con.cursor()
    sql = "select * from book100"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template('bookdata.html',books = datalist)

@app.route('/<type>')
def pick(type):
    datalist = []
    print(type)
    nife = ""
    if type == 'dushi':
        nife = "都市"
    elif type =='xuanhuan':
        nife = "玄幻"
    elif type =='xianxia':
        nife = "仙侠"
    elif type == 'qingxiaoshuo':
        nife = "轻小说"
    elif type == 'kehuan':
        nife = "科幻"
    elif type == 'xuanyi':
        nife = "悬疑"
    elif type == 'lishi':
        nife = "历史"
    elif type == 'youxi':
        nife = "游戏"
    elif type == 'qihuan':
        nife = "奇幻"

    con = sqlite3.connect("book.db")
    cur = con.cursor()
    sql1 = "select * from book100 where booktype = '%s'"%nife
    data = cur.execute(sql1)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()

    return render_template('pick.html', books = datalist)

@app.route('/chart')
def chart():
    types =[]
    numbers = []   #每种书的数量，充当y坐标
    con = sqlite3.connect("book.db")
    cur = con.cursor()
    sql = "select booktype,count(booktype) from book100 group by booktype"
    data = cur.execute(sql)
    for item in data:
        types.append(item[0])
        numbers.append(item[1])
    cur.close()
    con.close()
    return render_template('chart.html',types=types,numbers=numbers)


@app.route('/wordcloud')
def wordcloud():
    return render_template("wordcloud.html")

if __name__ == '__main__':
    app.run()
