import datetime
import inspect
import json
import os
import requests
import glob
import sys
from discord import Intents
from discord.ext.commands import Bot

print(inspect.cleandoc("""
    Please enter your bot's token below to continue.
"""))
if sys.version_info[1] <= 8:
    home = os.path.dirname(os.getcwd() + '/' + __file__)
else:
    home = os.path.dirname(__file__)

try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

while True:
    token = config.get("token", None)
    if token:
        print("\n--- Detected token in config.json (saved from previous run). Using stored token. ---\n")
    else:
        token = input("> ")

    data = requests.get("https://discord.com/api/v10/users/@me", headers={
        "Authorization": f"Bot {token}"
    }).json()

    if data.get("id", None):
        break
    print("\nSeems like you entered an invalid token. Try again by entering the correct token.")
    config = {}

with open("config.json", "w") as f:
    config["token"] = token
    json.dump(config, f, indent=2)


class FunnyBadge(Bot):
    def __init__(self, *, intents: Intents):
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self) -> None:
        """ This is called when the bot boots, to setup the global commands """
        for filename in glob.glob(home + '/cogs/**/*.py', recursive=True):
            if not "__" in filename:
                await client.load_extension(filename.replace(home + '/', '').replace('/', '.')[:-3])
        await self.tree.sync(guild=None)


client = FunnyBadge(intents=Intents.all())


@client.event
async def on_ready():
    client.start_time = datetime.datetime.now()
    """ This is called when the bot is ready and has a connection with Discord
        It also prints out the bot's invite URL that automatically uses your
        Client ID to make sure you invite the correct bot with correct scopes.
    """
    print(inspect.cleandoc(f"""
        > Logged in as {client.user} (ID: {client.user.id})
    """))

# Runs the bot with the token you provided
client.run(token)
