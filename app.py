from importlib.metadata import files
from flask import  render_template, request, redirect, url_for
from __init__ import app
import sqlite3
from pathlib  import Path

from werkzeug.utils import secure_filename
from datetime import datetime
from zoneinfo import ZoneInfo

database='database.db'

#app = Flask(__name__)

# 仮のスケジュールデータ（メモリ上）
data = []
def init_db():
    with sqlite3.connect(database) as con:
        con.execute('CREATE TABLE IF NOT EXISTS schedule1(date TEXT, event TEXT, filename TEXT, filetitle TEXT)')
        con.commit()

init_db()


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method=='POST':
        action=request.form['action']
        if action=='delete':
            row=request.form['row']
            con=sqlite3.connect(database)
            con.execute('UPDATE schedule1 SET date=NULL,event=NULL WHERE  rowid=?',(row,))
            con.commit()
            con.close()
            redirect(url_for('index'))

    con=sqlite3.connect(database)
    con.execute('CREATE TABLE IF NOT EXISTS schedule1(date TEXT,event TEXT,filename TEXT,filetitle TEXT)')#存在しないなら作らない
    list_schedule=con.execute('select date,event,rowid from schedule1 where date is not NULL').fetchall()

 #   rowid = con.execute(
#    "SELECT rowid FROM schedule1 WHERE date IS NOT NULL and event IS NOT NULL ORDER BY rowid DESC LIMIT 1"
 #   ).fetchall()
  #  con.close()

    #day=[]
    #row={}
   # for i in list_schedule:
  #      day.append({ i[0]:i[1]} )
 #       row[i[0]]=i[2]
#    day={1:"アニメ",31:'自分が墓標になることだ'}

   # if request.method == "POST":
     #   task = request.form.get("task")
      #  if task:  # 入力があれば追加
       #     data.append(task)
        
       # return redirect("/")#ボタン押したら更新?
    now=datetime.now(ZoneInfo("Asia/Tokyo"))

    day=(f'{now.year}年{now.month}月{now.day}日{now.hour}時')
    return render_template("index.html",list_schedule=list_schedule,day=day)

@app.route("/form",methods=['POST','GET'])
def form():
    gender={}
    image={}
    image_title={}
    

    if request.method=='POST':
        action=request.form.get('sex')
        if action=='男性' or action=='女性':
             gender['sex']=request.form.get('sex')
        else:
                
            f=request.files['gazou']
            image['gazou']=secure_filename(f.filename)
            f.save(Path(app.root_path) /"static"/ secure_filename(f.filename))

            image_title['name']=request.form['name']



            con=sqlite3.connect(database)
            con.execute('INSERT INTO schedule1 (filename,filetitle) VALUES(?,?)',(image['gazou'], image_title['name'],))
            con.commit()
            con.close()

    #if request.method == "POST":
    #    return redirect(url_for('form'))
    con=sqlite3.connect(database)
    file=con.execute("SELECT filename, filetitle FROM schedule1 WHERE filename IS NOT NULL ORDER BY rowid DESC LIMIT 1").fetchall()
    con.close()
    return render_template("form.html",gender=gender,i=file)
 


@app.route("/register",methods=['POST'])
def register():
    if request.method=='POST':
        date2=request.form['date']
        event2=request.form['event']
        con=sqlite3.connect(database)
        con.execute('INSERT INTO schedule1 (date,event)VALUES(?,?)',[date2,event2])
        con.commit()
        con.close()


    return redirect(url_for('index'))

if __name__ == "__main__":
    # Render は環境変数 PORT で指定されることが多い
    #import os
    #port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)

    
#@app.route("/debug")
#def debug():
#    files = os.listdir(os.path.join(app.root_path,"static"))
 #   return str(files)