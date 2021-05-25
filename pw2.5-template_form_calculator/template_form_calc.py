from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    title = 'pw2.5-template_form_calculator'
    content = None
    if request.method == 'POST' and request.form.get('number1') != None and request.form.get('number2') != None:
        num1 = float(request.form.get('number1'))
        num2 = float(request.form.get('number2'))
        if request.form.get('operator') == '0': content = num1 + num2
        if request.form.get('operator') == '1': content = num1 - num2
        if request.form.get('operator') == '2': content = num1 / num2
        if request.form.get('operator') == '3': content = num1 * num2

    return render_template('index.html', title = title, content = content)

if __name__ == '__main__':
    app.run()