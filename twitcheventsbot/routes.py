import secrets
import time


from flask import request, render_template, redirect, url_for, abort
from flask_login import UserMixin, current_user, login_user
from twitcheventsbot import app, db, discord, oauth_states
from twitcheventsbot.discord.interactions import interaction

base_url = "https://3841-2600-8801-ad00-3a1a-7956-33d1-d534-d161.ngrok.io"

@app.route("/")
@app.route("/home")
def home():
    return "welcome home"

@app.route("/twitch")
def twitch():
    return "twitch page"

@app.route("/discord")
def discord_home():
    
    return render_template("discord_dashboard_base.html")

@app.route("/discord/dashboard")
def discord_servers():
    if current_user.is_authenticated:

    # check if user is logged in
    # user is logged in
        # show server list
        unmanaged_guilds, managed_guilds = current_user.get_guild_list()
        return render_template("discord_dashboard_base.html", unmanaged_guilds=unmanaged_guilds, managed_guilds=managed_guilds)
    else:
    # user is not logged in
        # send user to login in page
        return redirect(url_for("discord_login"))

@app.route("/discord/dashboard/<guild_id>")
def discord_guild(guild_id):
    return f"guild {guild_id}'s page"

@app.route("/discord/login")
def discord_login():
    return render_template("discord_login.html")

@app.route("/discord/login/oauth")
def discord_oauth():
    state = secrets.token_hex()
    scopes = [
        "identify",
        "guilds",
        "email",
        "applications.commands.permissions.update"
    ]
    oauth_states[state] = time.time() + 60
    return redirect(discord.oauth_link(scopes, state, base_url + url_for("discord_callback")))

@app.route("/discord/login/callback")
def discord_callback():
    if "code" in request.args and "state" in request.args:
        code = request.args["code"]
        state = request.args["state"]

        if state in oauth_states and oauth_states[state] > time.time():
            r = discord.oauth_exchange(code, base_url + url_for("discord_callback"))

            token = r["access_token"]

            r = discord.get_token_owner(bearer=token)

            user = User.query.filter_by(discord_id=r["id"]).first()
            if user is None:
                user = User(discord_id=r["id"], discord_token=token)
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            del oauth_states[state]
            return redirect(url_for("discord_servers"))
        else:
            print("state code expired")
            print(f"state {oauth_states}: expires {oauth_states[state]}")
    else:
        print("bad url format")
    abort(400)

@app.route("/discord/logout")
def discord_logout():
    return "logout page"

@app.route("/discord/interaction", methods=['POST'])
def discord_interaction():
    # verify interaction signature
    if discord.verify_signature(request):
        return interaction(request.json)
    else:
        return 'invalid request signature', 401