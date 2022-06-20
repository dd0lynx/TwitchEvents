from twitcheventsbot import db, discord
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(20))
    discord_token = db.Column(db.String(100))

    def get_guild_list(self):
        bot_guilds = [bot_guild["id"] for bot_guild in discord.get("users/@me/guilds").json()]
        guilds = discord.get("users/@me/guilds", bearer=self.discord_token).json()
        manageble_guilds = [guild for guild in guilds if int(guild["permissions"]) & 8]
        managed_guilds = [guild for guild in manageble_guilds if guild["id"] in bot_guilds]
        unmanaged_guilds = [guild for guild in manageble_guilds if guild["id"] not in bot_guilds]
        return unmanaged_guilds, managed_guilds