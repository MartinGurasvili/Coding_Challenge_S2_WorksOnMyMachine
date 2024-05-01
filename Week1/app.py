from flask import Flask, render_template, request, jsonify
import string
import random 
from Gameboard import Gameboard
import logging


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()
p1Color = None

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
        include_caps = request.form.get('include_caps')
        include_special = request.form.get('include_special')
        include_digits = request.form.get('include_digits')
        length = request.form.get('length', 12)
        return passs_gen(length, include_caps, include_special, include_digits)
    return render_template('passgen.html')

@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/connect4', methods=['GET'])
def player1_connect():
    game.newGame()
    return render_template("player1_connect.html", status="Pick a colour to start game")

@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")

@app.route('/p1Color', methods=['GET'])
def player1_config():
    if game.retrieveSave() == "FAIL":
        p1Color = request.args.get('color')
        game.player1 = p1Color
        game.current_turn = game.player1
        if game.player1 == "red":
            game.player2 = "yellow"
        elif game.player1 == "yellow":
            game.player2 = "red"
    return render_template("player1_connect.html", status=("You are player "+game.player1))


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if game.player2 == "" and game.retrieveSave() == "FAIL":
        return render_template("p2Join.html", status="Error")
    return render_template("p2Join.html", status=("You are player "+game.player2))


@app.route('/move1', methods=['POST'])
def p1_move():
    player = game.player1
    colName = request.get_json()["column"]
    col = int(colName[-1]) - 1
    moveFailReason = game.move(player, col)
    if moveFailReason is not None:
        return jsonify(
            move=game.board,
            invalid=True,
            reason=moveFailReason,
            winner=game.game_result)
    else:
        return jsonify(
            move=game.board,
            invalid=False,
            winner=game.game_result)


@app.route('/move2', methods=['POST'])
def p2_move():
    player = game.player2
    colName = request.get_json()["column"]
    col = int(colName[-1]) - 1
    moveFailReason = game.move(player, col)
    if moveFailReason is not None:
        return jsonify(
            move=game.board,
            invalid=True,
            reason=moveFailReason,
            winner=game.game_result)
    else:
        return jsonify(
            move=game.board,
            invalid=False,
            winner=game.game_result)



if __name__ == '__main__':
    app.run(debug=True)