import inspect
import os

from utils import translate
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class TranslateCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.describe(
        string="A string",
        target_language="Target language"
    )
    async def translate(self, interaction: Interaction, string: str, target_language: str):
        """ Translate a string """
        print(f"> {interaction.user} used the command 'dictionary'.")
        await interaction.response.defer()
        result = translate.run(string, target_language)
        await interaction.followup.send(content=f"""
*Detected language: {result[1]}*
**{string}**

*Translated to: {target_language}*
**{result[0]}**
""")



async def setup(client):
    await client.add_cog(TranslateCog(client))
