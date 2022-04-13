from flask import Flask, render_template, request
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
    date = db.Column(db.DateTime, default = datetime.utcnow)

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

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>This is product page</p>"

@app.route("/delete/<int:sno>")
def delete():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>This is product page</p>"

@app.route("/update")
def update():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>This is product page</p>"

if __name__ == "__main__":
    app.run(debug=True, port=8000)
