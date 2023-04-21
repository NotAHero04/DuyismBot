import inspect
import os
import glob
import sys
import platform
import discord
import datetime
import re
import json
import subprocess
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]
class BotCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command()
    async def changelog(self, interaction: Interaction):
        """Bot's version historyq"""
        print(f"> {interaction.user} used the command 'changelog'.")
        await interaction.response.defer()
        with open(home + "/../changelog.txt", 'r') as f:
            await interaction.followup.send(f.read())


    @app_commands.command()
    async def ping(self, interaction: Interaction):
        """Test the bot's latency"""
        print(f"> {interaction.user} used the command 'ping'.")
        await interaction.response.defer()
        await interaction.followup.send("*Pong!* Latency: {} ms".format(round(1000 * self.client.latency)))


    @app_commands.command()
    async def botinfo(self, interaction: Interaction):
        """Get basic bot information"""
        print(f"> {interaction.user} used the command 'botinfo'.")
        await interaction.response.defer()
        with open(home + "/../settings.json", 'r') as f:
            settings = json.load(f)
        now = datetime.datetime.now()
        output = """
Ultimate Duyism Bot, by modern#0399
Running in Python {}. Discord.py version {}.
""".format('.'.join(list(map(str,sys.version_info[0:3]))), '.'.join(list(map(str,discord.version_info[0:3]))))
        if platform.system() == "Windows":
            output = inspect.cleandoc(f"""
                System info:
                    OS: {platform.platform().replace('-', ' ')}
                """)
        output += '\n' + inspect.cleandoc(f"""
        Bot info:
            Bot version: {settings['version']}
            Uptime: {round((now - self.client.start_time).total_seconds() / 60)} minutes
            (since {self.client.start_time.replace(microsecond=0).astimezone().isoformat()})
        """)
        await interaction.followup.send(content=output)


async def setup(client):
    await client.add_cog(BotCog(client))
