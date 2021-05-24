from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    content = 'Hello, world!'
    return render_template('hello.htlm', title = 'Hello', content = content)

@app.route("/secret")
def secret():
    content = 'You found a secret'
    return render_template('hello.htlm', title = 'Much secret', content = content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)