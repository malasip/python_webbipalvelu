from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    title = 'Index page'
    content = None
    if request.method == 'POST':
        content = {'name': request.form.get('name'),
                    'email': request.form.get('email'),
                    'password': request.form.get('password'),
                    'checkbox': request.form.get('checkbox')}
    return render_template('index.html', title = title, content = content)

if __name__ == '__main__':
    app.run()