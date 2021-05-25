from flask import Flask, render_template, flash, url_for, request, redirect
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'798fgdlna9g8odfahgnadgfdabgap9g0aydfg7'

@app.route('/')
def index():
    title = 'Index page'
    content = 'Content'
    return render_template('index.html', title = title, content = content)

@app.route('/get')
def get():
    title = 'Index page'
    content = ''
    content = request.args.get('q')
    return render_template('get.html', title = title, content = content)

@app.route('/post', methods = ['GET', 'POST'])
def post():
    content = None
    if request.method == 'POST':
        content = escape(request.form['name'])
    title = 'Index page'
    return render_template('post.html', title = title, content = content)

@app.route('/<path>')
def error(path):
    content = 'What did you expect to find here?'
    flash(content)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0')