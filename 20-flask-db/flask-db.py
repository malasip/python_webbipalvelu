from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

@app.before_first_request
def initDB():
    db.create_all()

    db.session.add(Device(name = 'ProBook 840', type = 'Laptop'))
    db.session.add(Device(name = 'EliteBook Z1', type = 'Laptop'))
    db.session.add(Device(name = 'EliteDesk Z', type = 'Desktop'))
    db.session.commit()

@app.route('/')
def index():
    devices = Device.query.all()
    title = 'Simple database'
    return render_template('index.html', title = title, devices = devices)

if __name__ == '__main__':
    app.run()