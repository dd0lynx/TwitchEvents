from twitcheventsbot import app

@app.route("/")
@app.route("/home")
def home():
    return "welcome home"

@app.route("twitch")
def twitch():
    return "twitch page"

@app.route("discord")
def discord():
    return "discord page"