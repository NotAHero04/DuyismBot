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
    @app_commands.describe(name="The whole CPU name or a part of it. Example: 'ryzen 7 5800x3d', 'i5-13500'")
    async def cpu(self, interaction: Interaction, name: str):
        """ Get info about x86-based CPUs """
        print(f"> {interaction.user} used the command 'cpu'.")
        await interaction.response.defer()
        try:
            result = cpu.run(name)[0]
        except IndexError:
            await interaction.followup.send("Oops, the CPU can not be found.")
        else:
            if result[0] == 429:
                await interaction.followup.send("We are being rate-limited. Please try again later.")
            else:
                d = list(zip(result[1].keys(), result[1].values()))
                msg = ""
                for i in d:
                    msg += ": ".join(i) + '\n'
                await interaction.followup.send(msg)


async def setup(client):
    await client.add_cog(CPUCog(client))
