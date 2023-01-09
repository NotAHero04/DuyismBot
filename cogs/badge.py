import inspect
from discord import Interaction, app_commands
from discord.ext import commands


class BadgeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def badge(self, interaction: Interaction):
        """ For the surprise """
        print(f"> {interaction.user} used the command 'badge'.")

        await interaction.response.send_message(inspect.cleandoc(f"""
            Hi **{interaction.user}**.
            > __**Where's my badge?**__
            > Eligibility for the badge is checked by Discord in intervals,
            > at this moment in time, 24 hours is the recommended time to wait before trying.

            > __**It's been 24 hours, now how do I get the badge?**__
            > If it's already been 24 hours, you can head to
            > https://discord.com/developers/active-developer and fill out the 'form' there.

            > __**Active Developer Badge Updates**__
            > Updates regarding the Active Developer badge can be found in the
            > Discord Developers server -> https://discord.gg/discord-developers - in the #active-dev-badge channel.
        """))


async def setup(client):
    await client.add_cog(BadgeCog(client))
