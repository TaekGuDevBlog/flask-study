from flask import Flask

app = Flask(__name__)

#decorator
@app.route('/')
def hello_world():
    return 'Hello World!'

#decorator
@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

#decorator
@app.route("/debug", methods=['GET'])
def debug_test():
    return "debug ok";

if __name__ == '__main__':
    app.run()
