from datetime import datetime
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom
from markupsafe import escape

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String, nullable = False)
    created = db.Column(db.DateTime, default = datetime.utcnow())
    completed = db.Column(db.DateTime)

TaskForm = model_form(Task, base_class = FlaskForm, db_session = db.session, exclude = ['created', 'completed'])

@app.before_first_request
def initDB():
    db.create_all()

@app.route('/')
def index():
    title = 'To-do list'
    tasks = Task.query.all()
    return render_template('index.html', title = title, tasks = tasks)

@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
@app.route('/create', methods = ['GET', 'POST'])
def create(id = None):
    form = TaskForm()
    task = Task()
    title = 'Create new task'
    if id:
        title = f'Edit task {id}'
        task = Task.query.get_or_404(id)
        form = TaskForm(obj = task)
        flash(f'Task {id} modified')

    if form.validate_on_submit(): #m
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()
        return redirect('/')

    return render_template('form.html', title = title, form = form)

@app.route('/<int:id>/complete')
def complete(id = None):
    task = Task.query.get_or_404(id)
    if not task.completed: 
        task.completed = datetime.utcnow()
        flash(f'Task {id} marked as completed')
    else:
        task.completed = None
        flash(f'Task {id} marked as not completed')
    db.session.commit()
    return redirect('/')

@app.route('/<int:id>/delete')
def delTask(id = None):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    flash(f'Task {id} marked as deleted')
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)