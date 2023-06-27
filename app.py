from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.todo'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(100))
    status = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list = todo_list)


#Adding a task to database
@app.route('/todo/add', methods=['POST'])
def add():

    task = request.form.get('task')

    if(len(task)==0 or task.isspace()):
        flash('Task cannot be empty or spaces..')
    
    else:
        new_todo = Todo(task = task, status = False)
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for('index'))

@app.route("/todo/edit/<int:todo_id>", methods = ['POST', 'GET'] )
def edit(todo_id):

    if request.method == 'POST':
        task = request.form.get('task')

        if(len(task)==0 or task.isspace()):
            flash('Task cannot be empty or spaces..')
        else:
            todo = Todo.query.filter_by(id = todo_id).first()
            todo.task = task
            db.session.commit()
            return redirect('/')

    todo = Todo.query.filter_by(id = todo_id).first()
    return render_template('edit.html', todo=todo)


@app.route("/todo/update/<int:todo_id>")
def update(todo_id):

    todo = Todo.query.filter_by(id = todo_id).first()
    todo.status = not todo.status
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/todo/delete/<int:todo_id>")
def delete(todo_id):

    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.secret_key = 'very secret key'    
    app.run(debug = True, port = 8000)