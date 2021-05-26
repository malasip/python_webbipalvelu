from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    value = db.Column(db.Integer, nullable = False)

@app.before_first_request
def initDatabase():
    db.create_all()

    db.session.add(Item(name = 'Golden Sword of Destiny', value = 152))
    db.session.add(Item(name = 'Broken Stick of Suck', value = 0))
    db.session.add(Item(name = 'Dirty Rag', value = 1))
    db.session.add(Item(name = 'Moldy Cheese', value = 0))
    db.session.commit()

@app.route('/')
def index():
    title = 'Adventurer\'s inventory'
    items = Item.query.all()

    return render_template('index.html', title = title, items = items)

if __name__ == '__main__':
    app.run()