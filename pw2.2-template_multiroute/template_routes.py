from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'pw2.2-template_multiroute'
    content = 'Some content'
    return render_template('index.html', title = title, content = content)

@app.route('/foo')
def foo():
    title = 'pw2.2-template_multiroute - Foo'
    content = 'Foo'
    return render_template('foo.html', title = title, content = content)

@app.route('/bar')
def bar():
    title = 'pw2.2-template_multiroute - Bar'
    content = 'Bar'
    return render_template('bar.html', title = title, content = content)

if __name__ == '__main__':
    app.run()