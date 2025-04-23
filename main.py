from datetime import datetime
from doctest import debug
from pickle import FALSE
from flask import  Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=FALSE

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"the sno is {self.sno} and The Title is {self.title} and description is {self.desc}"
    
@app.route('/add_task',methods=['GET','POST'])
def function():
    if request.method == 'POST':
        Title=request.form['title']
        Desc=request.form['desc']
        todo = Todo(title=Title , desc=Desc)
        if len(Title) == 0 :
            return ''' <script>alert("Both Title and Description are required!"); window.location.href="/add_task";</script>'''
            
        db.session.add(todo)
        db.session.commit()
    return render_template('index.html',todos=Todo.query.all())

@app.route('/')
def product():
    return   render_template('index.html',todos=Todo.query.all())

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    
#update
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        Title=request.form['title']
        Desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title = Title
        todo.desc = Desc
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


@app.route('/aboutus')
def home():
    return '''<h1>This Application is made for Learning! </h1>'''


if __name__=="__main__":
    app.run("0.0.0.0",debug=True,port=8080)
