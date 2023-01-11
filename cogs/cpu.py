import inspect
import os

from utils import cpu
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class CPUCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def cpu(self, interaction: Interaction):
        """ Get info about x86-based CPUs """
        print(f"> {interaction.user} used the command 'cpu'.")
        await interaction.response.defer()
        result = cpu.run()
        content = '\n'.join(result)
        await interaction.followup.send(content=content)


async def setup(client):
    await client.add_cog(CPUCog(client))
