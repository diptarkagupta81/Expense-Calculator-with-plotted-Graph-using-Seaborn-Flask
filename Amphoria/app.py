from flask import Flask,send_file,redirect,url_for,render_template,request
import yaml
import pymysql
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

app=Flask(__name__)

host = "127.0.0.1"
user = "root"
password = "Mpbirla25@"
db = "expense"
con = pymysql.connect(host=host , user=user , password=password , db=db , cursorclass=pymysql.cursors.DictCursor)
cursor=con.cursor()

x=[]
y=[]

@app.route('/input',methods=['GET','POST'])
def test():
    if request.method == 'POST':
        user = request.form
        income = user['Income']
        expense = user['Expense']
        cur=con.cursor()
        if income is not None:
            cur.execute("INSERT INTO expense.cost(Income,Expense) VALUES(%s,%s)",(income,expense))
        else:
            cur.execute("INSERT INTO expense.cost(Expense) VALUES(%s)",(expense))
        con.commit()

        #return 'success'
        return redirect(url_for('product'))
    return render_template('input.html')

@app.route('/product')
def product():
    cursor.execute("select Income,Expense from expense.cost")
    res=cursor.fetchall()
    return render_template("product.html",result=res)

fig,ax=plt.subplots(figsize=(6,6))
ax=sns.set_style(style="darkgrid")

#x=[1,28,34,45,77,78,89,99]
#y=[10,38,68,78,77,33,64,789]

def sum(arr):
    s=0
    for i in arr:
        s=s+1
    return s

@app.route('/')
def home():
    return render_template("index.html",content="Expense Graph")

@app.route('/visualize')
def visualize():
    #x=[]
    #y=[]
    cursor.execute("select Income,Expense from expense.cost")
    res=cursor.fetchall()
    for row in res:
        x.append(row['Income'])
        y.append(row['Expense'])
    #plt.plot(x,y)
    #s=sum(x)
    #res=y[0]-s

    z=sns.barplot(y,x)
    z.set(xlabel='Income',ylabel='Expense')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')

@app.route('/testy')
def testy():
    return render_template("testy.html",array=x)

if __name__=='__main__':
    app.run()
