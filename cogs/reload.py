# This cog should only be reloaded when restarting the bot, to prevent
# breaking changes to it from impacting the bot's functionalities.

import traceback
from discord import Interaction, app_commands
from discord.ext import commands

class ReloadCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def reload(self, interaction: Interaction):
        """Reload the bot and commands"""
        print(f"> {interaction.user} used the command 'reload'.")
        await interaction.response.defer()
        try:
            for extension in list(self.client.extensions):
                if extension != "cogs.reload":
                # DANGEROUS. DON'T REMOVE!
                    await self.client.reload_extension(extension)
            await interaction.followup.send("Reload successful.")
        except Exception:
            print(traceback.format_exc())
            await interaction.followup.send("An error occurred while reloading.")

async def setup(client):
    await client.add_cog(ReloadCog(client))
