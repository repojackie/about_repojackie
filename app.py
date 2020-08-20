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
@app.route("/chatroom")
def chatroom():
    return render_template("chatroom.html")

# external links and outlook
@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
