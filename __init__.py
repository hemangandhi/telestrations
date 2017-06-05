from flask import Flask
import eventlet
import eventlet.wsgi
import socketio

app = Flask(__name__)
sio = socketio.Server()

curr_round = 0
players = 0
waiting = 0

@app.route('/init', methods=['POST'])
def start():
    old_players = players
    players += 1
    return render_template('go_in.html', idx=old_players, round=0)

@sio.on('start_game', namespace='/game')
def start_game(sid):
    return sio.emit(players, True)

@app.route('/next', methods=['POST'])
def next_round():
    waiting += 1
    if waiting == players:
        waiting = 0
        curr_round += 1
        if curr_round > players:
            return render_template("ur_win.html", idx=request['idx'], players = players)
        else:
            return sio.emit(curr_round, False)
    else:
        return render_template('go_in.html', idx =request['idx'], round = 0)

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
