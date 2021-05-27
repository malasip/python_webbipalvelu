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

@app.route('/create', methods = ['GET', 'POST'])
def create():
    form = TaskForm()
    if form.validate_on_submit(): #m
        task = Task()
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()
        flash('Task created')
        return redirect('/')
    title = 'Create new task'
    return render_template('form.html', title = title, form = form)

@app.route('/edit', methods = ['GET', 'POST'])
def modify():
    if request.args.get('id'):
        id = int(escape(request.args.get('id')))
        task = Task.query.get(id)
        if task == None:
            flash(f'Invalid task ID')
            return redirect('/')
        form = TaskForm(obj = task) #m
        if form.validate_on_submit():
            form.populate_obj(task)
            db.session.commit()
            flash(f'Task {id} modified')
            return redirect('/')
        title = f'Edit task {id}'
        return render_template('form.html', title = title, form = form)
    flash(f'Invalid task ID')
    return redirect('/')

@app.route('/complete')
def complete():
    flash('Task id marked as completed')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)