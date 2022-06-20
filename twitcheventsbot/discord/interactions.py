from twitcheventsbot import discord
# , guilds, roles
from twitcheventsbot.discord.slash_commands.commands import run_command, command_flags
# from tools import log

# incomming interaction requests
PING = 1
APPLICATION_COMMAND = 2
MESSAGE_COMPONENT = 3
APPLICATION_COMMAND_AUTOCOMPLETE = 4
MODAL_SUBMIT = 5

# outgoing interaction response
PONG = 1
CHANNEL_MESSAGE_WITH_SOURCE = 4
DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
DEFERRED_UPDATE_MESSAGE = 6
UPDATE_MESSAGE = 7
APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
MODAL = 9

# Flags
EPHEMERAL = 1<<6

class Interaction:
    def __init__(self, request):
        self.type = request["type"]
        self.guild_id = request["guild_id"]
        self.channel_id = request["channel_id"]
        self.sender = request["member"]
        self.command = request["data"]
        self.subcommand_group = None
        self.subcommand = None
        self.options = None
        self.token = request["token"]

        if self.command["options"]:
            # check if the command's options are a subcommand or subcommand group
            if len(self.command["options"]) == 1 and (self.command["type"] == 1 or self.command["type"] == 2):
                self.subcommand = self.command["options"][0]

                # check if the subcommand is actually a group
                if self.subcommand["type"] == 2:
                    self.subcommand_group = self.command["options"][0]
                    self.subcommand = self.subcommand["options"][0]

                # check if the subcommand has options
                if self.subcommand["options"]:
                    self.options = self.command["options"]
            else:
                 self.options = self.command["options"]

    def to_string(self):
        return f"type: {self.type}\ncommand: {self.command}\nsubcommand_group: {self.subcommand_group}\nsubcommand: {self.subcommand}\noptions: {self.options}\n"

# acknowlages a ping request from discord with a pong response
def ping(request):
    print("recived a ping")
    response = {
        "type": PONG
    }
    return response, 200

# acknowlages a user slash command
# may be marked ephemeral to display response to the original user of the command
def application_command(request):
    print("recived a app command")
    # log.print_json(request)
    app_interaction = Interaction(request)
    response = {
        "type": DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": "command is running",
            "flags": command_flags(app_interaction)
        }
    }
    discord.thread(run_command, app_interaction)
    return response, 200

# acknowlages interaction with message components on the bot's messages
def message_component(request):
    print("recived a message command")
    # log.print_json(request)
    response = {
        "type": DEFERRED_UPDATE_MESSAGE
    }
    return response, 200

# idk how this is used yet
def application_command_autocomplete(request):
    print("recived a app autocomplete command")
    # log.print_json(request)
    return {"type": PONG}, 200

# some kind of form from discord
def modal_submit(request):
    print("recived a modal submit thing")
    # log.print_json(request)
    return {"type": PONG}, 200

interaction_request = [
    ping,
    application_command,
    message_component,
    application_command_autocomplete,
    modal_submit
]

# takes request json from flask
# returns the format for the interaction message shown in discord
def interaction(request):
    if 0 < request["type"] < len(interaction_request):
        return interaction_request[request["type"]-1](request)
    else:
        print("recived an invalid request")
        return "invalid request", 400 

def update_original_message(message_token, data):
    discord.patch(f"webhooks/{discord.client_id}/{message_token}/messages/@original", data)