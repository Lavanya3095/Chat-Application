from flask import Flask, render_template, flash, redirect, request, session, abort
from flask_socketio import SocketIO
import redis
import random
import string
from werkzeug.contrib.cache import SimpleCache
from diffie_hellman import rand, diffie_alice_public, diffie_bob_public, DSS_verify, shared_key
from des import des_enc, des_dec
from binascii import hexlify
import json

cache = SimpleCache()
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('alice', des_enc('cs@5173', 'ab562178de521165432fadc'))
r.set('bob', des_enc('cs@5173', 'ab562178de521165432fadc'))

secret_key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(17))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/AliceLoginPage', methods=['GET','POST'])
def login_alice():
    if not session.get('alice_logged_in'):
        return render_template('aliceLogin.html')
    else:
        return redirect("/AliceChat")

@app.route('/AliceChat')
def alice_chat():
    if session['alice_logged_in']:
        return render_template('alice_chat_box.html')
    else:
        return redirect("/AliceLoginPage")


@app.route('/BobLoginPage')
def login_bob():
    if not session.get('bob_logged_in'):
        return render_template('bobLogin.html')
    else:
        return redirect("/BobChat")

@app.route('/BobChat')
def bob_chat():
    if session['bob_logged_in']:
        return render_template('bob_chat_box.html')
    else:
        return redirect("/BobLoginPage")

@app.route('/Alice', methods=['GET','POST'])
def do_alice_login():
    if request.method == 'GET':
        if not session['alice_logged_in']:
            return redirect("/AliceLoginPage")
        else:
            return login_alice();
    if request.method == 'POST':
        key = request.form['username'];
        userPassword = request.form['password'];
        if (r.get(key) != None):
            redisStoredPassword = des_dec(r.get(key).decode('utf-8'), 'ab562178de521165432fadc');
            if redisStoredPassword == userPassword:
                session['alice_logged_in'] = True
                rand(1, 128, 24)
                h, s = diffie_alice_public()
                h1, s1 = diffie_bob_public()
                print(DSS_verify("a", h, s))
                print(DSS_verify("b", h1, s1))
                session['key'] = shared_key()
                return "success"
        return "wrong username / password"

@app.route('/Bob', methods=['GET','POST'])
def do_bob_login():
    if request.method == 'GET':
        if not session['bob_logged_in']:
            return redirect("/BobLoginPage")
        else:
            return login_bob();
    if request.method == 'POST':
        key = request.form['username'];
        userPassword = request.form['password'];
        if (r.get(key) != None):
            redisStoredPassword = des_dec(r.get(key).decode('utf-8'), 'ab562178de521165432fadc');
            if redisStoredPassword == userPassword:
                session['bob_logged_in'] = True
                return "success"
        return "wrong username / password"

@app.route('/aliceLogout', methods=['GET'])
def alice_logout():
    session['alice_logged_in'] = False;
    return "success"

@app.route('/bobLogout', methods=['GET'])
def bob_logout():
    session['bob_logged_in'] = False;
    return "success"

@app.route('/decryptAliceMsg', methods=['POST'])
def decryptAliceMsg():
    if request.method == 'POST':
        msg = json.loads(request.form['msg']);
        msg = des_dec(msg, session.get('key'))
        socketio.emit('bob response 2', msg, callback=messageReceived)
        return msg

@app.route('/decryptBobMsg', methods=['POST'])
def decryptBobMsg():
    if request.method == 'POST':
        msg = json.loads(request.form['msg']);
        msg = des_dec(msg, session.get('key'))
        socketio.emit('alice response 2', msg, callback=messageReceived)
        return msg

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('Alice event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received alice event: ' + str(json))
    if json and json.get('message') != None:
        encrypted = des_enc(json['message'], session.get('key'))
        socketio.emit('alice response', json, callback=messageReceived)
        json['message'] = encrypted
        socketio.emit('bob response 1', json, callback=messageReceived)

@socketio.on('Bob event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received bob event: ' + str(json))
    if json and json.get('message') != None:
        encrypted = des_enc(json['message'], session.get('key'))
        socketio.emit('bob response', json, callback=messageReceived)
        json['message'] = encrypted
        socketio.emit('alice response 1', json, callback=messageReceived)

@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    if request.method == 'POST':
        return request.form['src'];

if __name__ == '__main__':
    socketio.run(app, debug=True)