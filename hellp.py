from flask import Flask
app = Flask(__name__)

@app.route('/projects/')
def hello_world():
    return 'The Projects page'

@app.route('/about')
def hello():
    return 'The about page'

if __name__ == '__main__':
    app.debug = True   
    app.run()
