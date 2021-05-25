from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    content = 'Hello, world!'
    return content

@app.route('/foo')
def foo():
    content = 'Foo'
    return content
    
@app.route('/bar')
def bar():
    content = 'Bar'
    return content

@app.route('/rick')
def rick():
    content = '''<iframe
                    width="560"
                    height="315"
                    src="https://www.youtube.com/embed/dQw4w9WgXcQ?controls=0&autoplay=1"
                    title="YouTube video player"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>'''
    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)