import datetime
import inspect
import os

from discord import Interaction, app_commands
from discord.ext import commands
from utils import lunar

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class LunarCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.describe(date="A date in ISO format. Example: 2022-07-19")
    async def lunar(self, interaction: Interaction, date: str = datetime.date.today().isoformat()):
        """ Get the lunar date """
        print(f"> {interaction.user} used the command 'lunar'.")
        await interaction.response.send_message(lunar.run(date))


async def setup(client):
    await client.add_cog(LunarCog(client))
