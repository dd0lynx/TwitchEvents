from twitcheventsbot import discord
from twitcheventsbot.discord import interactions

# from api.discord.slash_commands import role, rolemenu, twitchauth

commands = {
    # "role": role,
    # "role-menu": rolemenu,
    # "twitch-auth": twitchauth
    }

def command_flags(interaction):
    # command_name = command_data["name"]
    if interaction.command["name"] in commands:
        # command_options = command_data["options"]
        return commands[interaction.command["name"]].flags(interaction)
    else:
        return 1<<6

def run_command(interaction):
    # command_name = request["data"]["name"]
    if interaction.command["name"] in commands:
        data = commands[interaction.command["name"]].command(interaction)
    else:
        data = invalid_command(interaction.command["name"])
    interactions.update_original_message(interaction.token, data)

def invalid_command(command_name):
    error_msg = f"command: \"{command_name}\" is invalid hasn't been implemented yet"
    print(error_msg)
    data = {
        "content": error_msg,
        "flag": interactions.EPHEMERAL
    }
    return data

# def update_original_message(message_token, data):
#     discord.patch(f"webhooks/{discord.client_id}/{message_token}/messages/@original", data)