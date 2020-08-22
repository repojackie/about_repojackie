"""
ABOUT_REPOJACKIE -> Backend using Python-Flask

TO-DO: 
    [] Backend for blog - Create an account and allow people to post on certain circumstances? 
"""
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySHITTYbeingisSURREAL'
socketio = SocketIO(app)

# homepage 
@app.route("/")
def hello():
    return render_template("homepage.html")

# portfolio
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

# chat room
@app.route("/chatroom", methods=['GET', 'POST'])
def chatroom(methods=['GET', 'POST']):
    return render_template("chatroom.html")

# blog
@app.route("/blog")
def blog():
    return render_template("blog.html")

# external links and outlook
@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print("received an event: " + str(json))
    if (len(json) > 1):
        # not emitting preliminary connection message!
        socketio.emit('my response', json, callback=messageReceived)

if __name__ == "__main__":
    socketio.run(app, debug=True)
