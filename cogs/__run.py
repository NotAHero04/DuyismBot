import os
import subprocess

from discord import Interaction, app_commands
from discord.ext import commands

home = os.getenv("HOME") + "/bot"


class RunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.describe(
        package="A package. Run /about to get a list of packages",
        program="Program name",
        args="A list of arguments, separated by spaces"
    )
    async def run(self, interaction: Interaction, package: str, program: str, args: str = ""):
        """ Run commands that are not yet aliased """
        if str(interaction.user) != "modern#0399":
            print(f"> Use of command 'run' by {interaction.user} has been denied.")
            await interaction.response.send_message(f"Use of command 'run' by {interaction.user} has been denied.")
        else:
            path = home + "/" + package + "/" + program
            print(f"> {interaction.user} used the command 'run'.")
            if os.path.isfile(path):
                output = subprocess.Popen([path] + [args], stdout=subprocess.PIPE).communicate()[0]
                await interaction.response.send_message(output.decode('utf-8'))
            else:
                await interaction.response.send_message("The program does not exist")


async def setup(client):
    await client.add_cog(RunCog(client))
