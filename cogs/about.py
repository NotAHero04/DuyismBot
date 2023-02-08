from discord import Interaction, app_commands
from discord.ext import commands

from utils import about


class AboutCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command()
	async def about(self, interaction: Interaction):
		""" About this bot and its components """
		print(f"> {interaction.user} used the command 'about'.")
		await interaction.response.defer()
		await interaction.followup.send(about.run())


async def setup(client):
	await client.add_cog(AboutCog(client))
