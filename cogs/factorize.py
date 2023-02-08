import inspect
import os


from utils import factor
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class FactorizeCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command()
	@app_commands.describe(number="A number greater than 2")
	async def factorize(self, interaction: Interaction, number: int):
		""" Prints the prime factorization of a number """
		print(f"> {interaction.user} used the command 'factorize'.")
		await interaction.response.defer()
		await interaction.response.send_message(factor.run(number))


async def setup(client):
	await client.add_cog(FactorizeCog(client))
