from datetime import datetime
from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'ypw8t82JppEGdSQ9pj5rzmOSypda4W7LI1hTefNGDWOKNwNq7RPSfTGqPjNZEI1HsmFh0ELxrWzGIzAysKAyyyhwBWHJVmCcaraTZkNHnk3TsMHVMciJrBH6359cmSJW'

db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default=datetime.now)
    devtype = db.relationship('Devtype', backref = db.backref('device', lazy = True))
    devtype_id = db.Column(db.Integer, db.ForeignKey('devtype.id'), nullable = False)

class Devtype(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

    def __str__(self) -> str:
        return escape(self.name)

DeviceForm = model_form(model = Device, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def initDB():
    db.create_all()
    db.session.add(Devtype(name = 'Laptop'))
    db.session.add(Devtype(name = 'Desktop'))
    db.session.commit()

@app.route('/')
def index():
    devices = Device.query.all()
    title = 'Simple database with relations'
    return render_template('index.html', title = title, devices = devices)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    title = 'Add new device'
    form = DeviceForm()
    return render_template('new.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug=True)