from datetime import datetime
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    content = {
        'title': 'Flask templates demo',
        'name': 'ranbomWebUser #1202868',
        'dateTime': datetime.now()
    }
    return render_template('base.html', content = content)

@app.route('/secret')
def secret():
    content = 'You found a secret'
    return render_template('hello.html', title = 'Much secret', content = content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)