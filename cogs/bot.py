import inspect
import os
import glob
import sys
import platform
import discord
import datetime
import re
import subprocess
from discord import Interaction, app_commands
from discord.ext import commands

if sys.version_info[1] <= 8:
    home = os.path.dirname(os.getcwd() + '/' + __file__)
else:
    home = os.path.dirname(__file__)

class BotCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command()
    async def changelog(self, interaction: Interaction):
        """Bot's version historyq"""
        print(f"> {interaction.user} used the command 'changelog'.")
        await interaction.response.defer()
        await interaction.followup.send("""
Latest release: 0.1.5 (2023-2-8).
        - New commands:
		+ Maths for nerds

Version history:
	0.1.4 (2023-2-8): Added computer hardware-related commands.
        0.1.3 (2023-1-9): Added commands: "urban", "dictionary", "translate".
        0.1.2 (2023-1-1): Moved the entire bot's codebase to Python, was a mix between Python and Bash
        0.1.1 (2022-12-26): Fully modularized the bot, allowing for on-the-go modifications
	0.1.0 (2022-12-17): Initial release.

This bot uses these external services:
        - Google Translate (translate), via external APIs
        - TechPowerUP (cpu, gpu)
	- gsmarena (phone), via external APIs

Join https://discord.gg/S4gDrGpqev for support.
""")


    @app_commands.command()
    async def reload(self, interaction: Interaction):
        """Reload the bot and commands"""
        print(f"> {interaction.user} used the command 'reload'.")
        await interaction.response.defer()
        try:
            for extension in list(self.client.extensions):
                 await self.client.unload_extension(extension)
                 await self.client.load_extension(extension)
            await interaction.followup.send("Reload successful.")
        except Exception:
            try:
                await self.client.load_extension("cogs.bot")
            except Exception:
                await interaction.followup.send("An error occurred while reloading. Fallback to broken state failed. Restart the bot.")
            else:
                await interaction.followup.send("An error occurred while reloading.")




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
        version = "{}.{}.{}".format(*sys.version_info)
        output = """
Ultimate Duyism Bot, by modern#0399
Running in Python {}.
Bot version: 0.1.6+nightly.2023.4.15
""".format('.'.join(list(map(str,sys.version_info[0:3]))))
        if platform.system() == "Windows":
            output = inspect.cleandoc(f"""
                System info:
                    OS: {platform.platform().replace('-', ' ')}
                """)
        output += '\n' + inspect.cleandoc(f"""
        Bot info:
            Uptime: {round((datetime.datetime.now() - self.client.start_time).total_seconds() / 60)} minutes
        """)
        temp_output = "\n    External libraries: *Gathering info...*"
        await interaction.followup.send(output + temp_output)
        temp_output = "\n    External libraries: "
        libs = subprocess.getoutput('pip list').split('\n')
        pattern = re.compile("discord.py|requests|beautifulsoup4")
        no_info = True
        for lib in libs:
            if pattern.search(lib):
                temp_output += "```\n{}".format(lib)
                no_info = False
        if no_info:
            temp_output += "*No information.*"
        else:
            temp_output += "```"
        await interaction.edit_original_response(content=output+temp_output)


async def setup(client):
    await client.add_cog(BotCog(client))
