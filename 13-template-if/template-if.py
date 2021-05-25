from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Index page'
    content = 'Some content'
    weekday = datetime.isoweekday(datetime.now())
    weekdays = [
        'Maanantai',
        'Tiistai',
        'Keskiviikko',
        'Torstai',
        'Perjantai',
        'Lauantai'
        'Sunnuntai'
    ]
    return render_template('index.html', title = title, content = content, weekday = weekday, weekdays = weekdays)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')