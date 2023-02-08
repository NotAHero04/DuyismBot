import inspect
import os

from utils import dictionary
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class DictionaryCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command()
	@app_commands.describe(word="An English word")
	async def dictionary(self, interaction: Interaction, word: str):
		""" Get the meaning of an English word """
		print(f"> {interaction.user} used the command 'dictionary'.")
		await interaction.response.defer()
		for index, msg in enumerate(dictionary.run(word)):
			if index == 0:
				await interaction.followup.send(content=msg)
			else:
				await interaction.followup.send(msg)


async def setup(client):
	await client.add_cog(DictionaryCog(client))
