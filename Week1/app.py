from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/passgen')
def passgen():
    return render_template('passgen.html')

if __name__ == '__main__':
    app.run(debug=True)