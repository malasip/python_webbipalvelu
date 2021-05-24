from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"

@app.route("/secret")
def secret():
    return "You found a secret"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
