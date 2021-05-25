from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    content = 'Hello, world!'
    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)