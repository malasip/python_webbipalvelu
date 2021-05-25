from datetime import date
from flask import Flask, render_template, flash, url_for, request, redirect

app = Flask(__name__)
app.secret_key = b'798fgdlna9g8odfahgnadgfdabgap9g0aydfg7'

@app.route('/')
def index():
    title = 'Index page'
    content = [
                {'name': 'get',
                'url': url_for('get')},
                {'name': 'post',
                'url': url_for('post')}]
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
        content = {
            'name': request.form['name'],
            'date': request.form['date']
        }
    title = 'Index page'
    return render_template('post.html', title = title, content = content)

@app.route('/<path>')
def error(path):
    content = 'What did you expect to find here?'
    flash(content)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0')