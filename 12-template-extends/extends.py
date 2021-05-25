from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Index page'
    content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    return render_template('index.html', title = title, content = content)

@app.route('/about')
def about():
    title = 'About page'
    content = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Sed vitae nulla a sem tincidunt commodo.
                Fusce nunc arcu, egestas sed dolor nec, feugiat venenatis eros.
                Mauris molestie, neque in eleifend consequat, dui sapien ultricies urna, at egestas mi nisi et ante.
                Aliquam erat volutpat. Vestibulum in tincidunt erat. Donec a nisi id odio posuere lobortis non quis lorem.
                Donec lobortis, dolor at egestas fringilla, dolor ligula volutpat sem, vitae fringilla elit lacus at massa.'''
    return render_template('about.html', title = title, content = content)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')