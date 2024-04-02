from flask import Flask, render_template, request
import string
import random 

app = Flask(__name__)

def passs_gen(length, include_caps, include_special, include_digits):
    characters = string.ascii_lowercase
    if include_caps == "1":
        characters += string.ascii_uppercase
    if include_special== "1":
        characters += string.punctuation
    if include_digits== "1":
        characters += string.digits 

    passs = ''.join(random.choice(characters) for _ in range(int(length)))
    return render_template('passgen.html', passs_gen=passs)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/passgen', methods=['GET', 'POST'])
def passgen():
    if request.method == 'POST' and 'include_caps' in request.form and 'include_special' in request.form and 'include_digits' in request.form:
        # length = 12  # Set your desired password length
        include_caps = request.form.get('include_caps')
        include_special = request.form.get('include_special')
        include_digits = request.form.get('include_digits')
        length = request.form.get('length', 12)
        return passs_gen(length, include_caps, include_special, include_digits)
    return render_template('passgen.html')

@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

if __name__ == '__main__':
    app.run(debug=True)