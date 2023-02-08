import inspect
import os

from discord import Interaction, app_commands
from discord.ext import commands
from utils import pythagoras

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class PythagorasCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command()
	@app_commands.describe(number="A number greater than -1")
	async def pythagoras(self, interaction: Interaction, number: int):
		""" Prints a prime Pythagoras triple """
		print(f"> {interaction.user} used the command 'pythagoras'.")
		await interaction.response.defer()
		await interaction.followup.send(pythagoras.run(number))


async def setup(client):
	await client.add_cog(PythagorasCog(client))
