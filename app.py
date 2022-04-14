from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #for sqlite database
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@server/db" #for mysql database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    # print(f' datetime is {datetime.utcnow}')
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:   #whenever you call the object of Todo class then the repr function will print first 
        return f"{self.sno} - {self.title}"



@app.route("/", methods = ['GET','POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo = allTodo)

# @app.route("/show")
# def products():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return "<p>This is product page</p>"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods = ['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("/update.html", todo = todo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
