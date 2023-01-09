import datetime
# import subprocess
import discord
import inspect
import sys
import platform

from discord import Interaction, app_commands
from discord.ext import commands


class HostInfoCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def hostinfo(self, interaction: Interaction):
        """ Get the host system information """
        print(f"> {interaction.user} used the command 'hostinfo'.")
        version = "{}.{}.{}".format(*sys.version_info)
        match platform.system():
            case "Windows":
                output = inspect.cleandoc(f"""
                System info:
                    OS: {platform.platform().replace('-', ' ')}
                """)
        output += '\n' + inspect.cleandoc(f"""
        Bot info:
            Language and libraries: Python version {version}, discord.py version {discord.__version__}
            Bot uptime: {round((datetime.datetime.now() - self.client.start_time).total_seconds() / 60)} minutes
        """)
        await interaction.response.send_message(output)


async def setup(client):
    await client.add_cog(HostInfoCog(client))
