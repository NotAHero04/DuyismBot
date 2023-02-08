import inspect
import os

from utils import phone
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class PhoneCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command()
	@app_commands.describe(name="A phone name. Example: 'iphone 14 pro', 'galaxy a73'")
	async def phone(self, interaction: Interaction, name: str):
		""" Get info about smartphones """
		print(f"> {interaction.user} used the command 'phone'.")
		await interaction.response.defer()
		result = phone.run(name)
		d = list(zip(result.keys(), result.values()))
		msg = ""
		for i in d:
			msg += ": ".join(i) + '\n'
		await interaction.followup.send(msg)


async def setup(client):
	await client.add_cog(PhoneCog(client))
