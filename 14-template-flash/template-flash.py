from flask import Flask, render_template, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = b'798fgdlna9g8odfahgnadgfdabgap9g0aydfg7'

@app.route('/')
def index():
    title = 'Index page'
    content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    return render_template('index.html', title = title, content = content)

@app.route('/<subpath>')
def error(subpath):
    content = 'What did you expect to find here?'
    flash(content)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0')