from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    content = "Random tekstiääääääääääää punaisella"
    return render_template('index.html', content = content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)