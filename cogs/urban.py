# Someone is gonna write this piece of code better than me.
# Probably me in the future?

import inspect
import os
import discord
import datetime

from discord import Interaction, app_commands, ButtonStyle, TextStyle
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from utils import urban

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]

class UrbanModal(Modal, title="Go to page..."):
    def __init__(self, word):
        super().__init__()
        self.word = word

    input = TextInput(label="Page", placeholder="1")

    async def on_submit(self, interaction: Interaction):
        global index
        index2 = index
        try:
            index = int(self.input.value)
            if index > length:
                await interaction.response.send_message(f"""It looks like you are trying to go too far.
The last page is {length}.""", ephemeral=True)
            elif index < 1:
                await interaction.response.send_message(f"""It looks like you are trying to go too far.
The first page is 1.""", ephemeral=True)
            else:
                global ret
                ret = urban.run(self.word, (index - 1) // 10 + 1)
                await interaction.response.edit_message(content=f"""
{index}/{length}
{parse(ret[(index - 1) % 10])}
""")
        except ValueError:
            index = index2
            await interaction.response.send_message(f"""That is not a valid page number at all.""", ephemeral=True)
        except (KeyError, IndexError):
            index = index2
            await interaction.response.send_message(f"""Something goes wrong. Try again.""", ephemeral=True)


class UrbanView(View):
    def __init__(self, timeout, max_index, word):
        super().__init__(timeout=timeout)
        self.max_index = max_index
        self.word = word

    async def on_timeout(self) -> None:
        self.stop()

    @discord.ui.button(label="<<",
                       style=ButtonStyle.green)
    async def prev(self, interaction: Interaction, button: Button):
        global index
        index -= 1
        if index % 10 == 0:
            global ret
            ret = urban.run(self.word, (index - 1) // 10 + 1)
        if index < 1:
            index = 1
        await interaction.response.edit_message(content=f"""
{index}/{self.max_index}
{parse(ret[(index - 1) % 10])}
""")

    @discord.ui.button(label=">>",
                       style=ButtonStyle.green)
    async def next(self, interaction: Interaction, button: Button):
        global index
        try:
            index += 1
            if index % 10 == 1:
                global ret
                ret = urban.run(self.word, (index - 1) // 10 + 1)
            if index > self.max_index:
                index = self.max_index
            await interaction.response.edit_message(content=f"""
{index}/{self.max_index}
{parse(ret[(index - 1) % 10])}
""")
        except IndexError:


    @discord.ui.button(label="Go to...",
                       style=ButtonStyle.gray)
    async def goto(self, interaction: Interaction, button: Button):
        await interaction.response.send_modal(UrbanModal(word=self.word))

class UrbanCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.describe(
        word="A word",
        fetch_all_results="Decides whether the bot should fetch all the results instead of just 10. Default to False."
    )
    @app_commands.choices(fetch_all_results=[
        app_commands.Choice(name="true", value = 1),
        app_commands.Choice(name="false", value = 0)
    ])
    async def urban(self, interaction: Interaction, word: str, fetch_all_results: int = 0):
        """ Get the definition of a word from Urban Dictionary """
        print(f"> {interaction.user} used the command 'urban'.")
        await interaction.response.defer()
        global ret, length, index
        index = 1
        ret = urban.run(word)
        if fetch_all_results == 0:
            length = len(ret)
        else:
            length = urban.get_def_count(word)
        if len(ret) == 0:
            await interaction.followup.send("That word is not defined yet. May be it's your time to define it?")
        else:
            view = UrbanView(timeout=900, max_index=length, word=word)
            await interaction.followup.send(f"""
1/{length}
{parse(ret[0])}
""", view=view)
            await view.wait()


async def setup(client):
    await client.add_cog(UrbanCog(client))

def parse(msg: list):
    ret = f"""**{msg[0]}**
*by {msg[3]}*
*{msg[1]} 👍, {msg[2]} 👎*

*Definitions:*
{msg[4]}

*Examples:*
{msg[5]}

*Time of writing:*
{datetime.datetime.strptime(msg[6], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d, %H:%M:%S")}
"""

    if len(ret) > 2000:
        ret = ret[:1997] + "..."
    return ret
