from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'pw2.3-template_for-loop'
    content = [
        'Affenpinscher',
        'Afghan Hound',
        'Aidi',
        'Airedale Terrier',
        'Akbash Dog',
        'Akita',
        'Alano Español',
        'Alaskan Klee Kai',
        'Alaskan Malamute',
        'Alpine Dachsbracke',
        'Alpine Spaniel',
        'American Bulldog',
        'American Cocker Spaniel',
        'American Eskimo Dog',
        'American Foxhound',
        'American Hairless Terrier',
        'American Pit Bull Terrier',
        'American Staffordshire Terrier',
        'American Water Spaniel']
    return render_template('index.html', title = title, content = content)

if __name__ == '__main__':
    app.run()