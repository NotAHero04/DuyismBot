import inspect
import os

from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]

class ReloadCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def reload(self, interaction: Interaction):
        """Reload the commands and events"""
        print(f"> {interaction.user} used the command 'reload'.")
        try:
            for extension in list(self.client.extensions):
                await self.client.unload_extension(extension)
            for filename in os.listdir(home):
                if filename.endswith(".py") and not filename.startswith("__"):
                    await self.client.load_extension(f"cogs.{filename[:-3]}")
            await interaction.response.send_message("Successfully reloaded!")
        except Exception:
            await interaction.response.send_message("An error occurred while reloading.")
            await self.client.load_extension("cogs.reload")


async def setup(client):
    await client.add_cog(ReloadCog(client))
