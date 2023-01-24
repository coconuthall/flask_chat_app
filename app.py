from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
socket = SocketIO(app)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat')
def chat():
    username = request.args.get('name')
    room = request.args.get('room')

    if username and room:
        return render_template("chatroom.html", username=username, room=room)
    else:
        return redirect(url_for('home'))

@socket.on("join_room")
def join_room_handler(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socket.emit('join_room_announcement', data)

@socket.on('send_message')
def send_message_handler(data):
    app.logger.info("{} has sent message {} in room {}".format(
        data['username'], 
        data['message'], 
        data['room']))
    socket.emit('receive_message', data, room = data['room'])


@socket.on('leave_room')
def leave_room_handler(data):
    app.logger.info("{} has left the room {}".format(
        data['username'], 
        data['room']))
    leave_room(data['room'])
    socket.emit('leave_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    socket.run(app, debug = True)