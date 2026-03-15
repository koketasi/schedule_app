from importlib.metadata import files
from flask import  render_template, request, redirect, url_for
from __init__ import app
import __init__
import sqlite3
from pathlib  import Path

from werkzeug.utils import secure_filename
import os

database='database.db'


data = []
def init_db():
    with sqlite3.connect(database) as con:
        con.execute('CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, year TEXT,month TEXT,day TEXT, event TEXT, file_name TEXT, file_title TEXT)')
        con.commit()
 


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method=='POST':
        action=request.form['action']
        
        match action:
            case 'add': #追加
                year=request.form['year']
                month=request.form['month']
                day=request.form['day']
                hour=request.form['hour']
                miute=request.form['minute']
                event=request.form['event']
                file=request.files.get('name')
                file_name=None
                file_title=request.form.get('title')

                if file and file.filename!='':
                    file_name=secure_filename(file.filename)
                    file.save(Path(__file__).parent /"static"/ file_name)



                with sqlite3.connect(database) as con:
                    con.execute('INSERT INTO schedule (year,month,day,hour,minute,event,file_name,file_title)VALUES(?,?,?,?,?,?,?,?)',[year,month,day,hour,miute,event,file_name,file_title])
                    con.commit()
                return redirect(url_for('index'))

            case 'edit':
                row=request.form['row']
                year=request.form['year']
                month=request.form['month']
                day=request.form['day']
                hour=request.form['hour']
                miute=request.form['minute']
                event=request.form['event']
                file=request.files.get('name')
                current_name=request.form.get('current_name')
                file_title=request.form.get('title')

                if file and file.filename!='':
                    current_name=secure_filename(file.filename)
                    file.save(Path(__file__).parent /"static"/ current_name)
                #print(f'current_name: {repr(current_name)}')
                with sqlite3.connect(database) as con:
                    con.execute('UPDATE schedule SET year=?,month=?,day=?,hour=?,minute=?,event=?,file_name=?,file_title=? WHERE rowid=?',[year,month,day,hour,miute,event,current_name,file_title,row])
                    con.commit()

                return redirect(url_for('index'))

            case 'delete':
                row=request.form['row']
                con=sqlite3.connect(database)
                con.execute('DELETE FROM schedule  WHERE  rowid=?',(row,))
                con.commit()
                con.close()
                return redirect(url_for('index'))

   # edit=request.args.get('edit')
    #if edit!=None:
     #   edit=int(edit)
    con=sqlite3.connect(database)
   # con.execute('CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, event TEXT, file_name TEXT, file_title TEXT)')#存在しないなら作らない
    schedule_list=con.execute('SELECT year,month,day,hour,minute,event,file_name,file_title,rowid from schedule where event is not NULL').fetchall()
    con.close()
    return render_template("index.html",schedule_list=schedule_list)




if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
