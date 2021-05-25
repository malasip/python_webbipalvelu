from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'pw2.1-template_vars'
    content = 'Some content'
    return render_template('index.html', title = title, content = content)

if __name__ == '__main__':
    app.run()