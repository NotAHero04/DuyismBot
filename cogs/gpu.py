import inspect
import os

from utils import gpu
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class GPUCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command()
	@app_commands.describe(name="The whole GPU name or a part of it. Example: 'geforce rtx 4080', 'hd 6990'")
	async def gpu(self, interaction: Interaction, name: str):
		""" Get info about GPUs """
		print(f"> {interaction.user} used the command 'gpu'.")
		await interaction.response.defer()
		result = gpu.run(name)
		if result[0] == 429:
			await interaction.followup.send("We are being rate-limited. Please try again later.")
		else:
			d = list(zip(result[1].keys(), result[1].values()))
			msg = ""
			for i in d:
				msg += ": ".join(i) + '\n'
			await interaction.followup.send(msg)


async def setup(client):
	await client.add_cog(GPUCog(client))
