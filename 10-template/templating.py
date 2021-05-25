from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Document title'
    content = 'Document content'
    return render_template('base.html', title = title, content = content)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')