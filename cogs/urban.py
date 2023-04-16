# Someone is going to write this piece of code better than me.
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

ret = {}

class UrbanModal(Modal, title="Go to page..."):
    def __init__(self, id):
        super().__init__()
        self.id = id

    input = TextInput(label="Page", placeholder="1")

    async def on_submit(self, interaction: Interaction):
        global ret
        id = self.id
        length = ret[id]['max_index']
        index2 = ret[id]['index']
        try:
            index = int(self.input.value)
            if index > length:
                await interaction.response.send_message(f"""It looks like you are trying to go too far.
The last page is {length}.""", ephemeral=True)
            elif index < 1:
                await interaction.response.send_message(f"""It looks like you are trying to go too far.
The first page is 1.""", ephemeral=True)
            else:
                ret[id]['index'] = index
                ret[id]['defs'] = urban.run(ret[id]['word'], (index - 1) // 10 + 1)
                await interaction.response.edit_message(content=f"""
{index}/{length}
{parse(ret[id]['defs'][(ret[id]['index'] - 1) % 10])}
""")
        except ValueError:
            await interaction.response.send_message(f"""That is not a valid page number at all.""", ephemeral=True)
        except (KeyError, IndexError):
            await interaction.response.send_message(f"""Something goes wrong. Try again.""", ephemeral=True)


class UrbanView(View):
    def __init__(self, timeout, id):
        global ret
        super().__init__(timeout=timeout)
        self.id = id
        self.max_index = ret[id]['max_index']
        self.word = ret[id]['word']

    async def on_timeout(self) -> None:
        global ret
        ret.pop(self.id)
        self.stop()

    @discord.ui.button(label="<<",
                       style=ButtonStyle.green)
    async def prev(self, interaction: Interaction, button: Button):
        global ret
        id = self.id
        try:
            if ret[id]['index'] > 1:
                ret[id]['index'] -= 1
                if ret[id]['index'] % 10 == 0:
                    ret[id]['defs'] = urban.run(self.word, (ret[id]['index'] - 1) // 10 + 1)
            await interaction.response.edit_message(content=f"""
{ret[id]['index']}/{self.max_index}
{parse(ret[id]['defs'][(ret[id]['index'] - 1) % 10])}
""")
        except IndexError:
            ret[id]['index'] = index
            await interaction.response.send_message(f"""Something goes wrong. Try again.""", ephemeral=True)


    @discord.ui.button(label=">>",
                       style=ButtonStyle.green)
    async def next(self, interaction: Interaction, button: Button):
        global ret
        id = self.id
        try:
            if ret[id]['index'] < self.max_index:
                ret[id]['index'] += 1
                if ret[id]['index'] % 10 == 1:
                    ret[id]['defs'] = urban.run(self.word, (ret[id]['index'] - 1) // 10 + 1)
            await interaction.response.edit_message(content=f"""
{ret[id]['index']}/{self.max_index}
{parse(ret[id]['defs'][(ret[id]['index'] - 1) % 10])}
""")
        except IndexError:
            ret[id]['index'] = index
            await interaction.response.send_message(f"""Something goes wrong. Try again.""", ephemeral=True)

    @discord.ui.button(label="Go to...",
                       style=ButtonStyle.gray)
    async def goto(self, interaction: Interaction, button: Button):
        await interaction.response.send_modal(UrbanModal(id=self.id))


class UrbanCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command()
    @app_commands.describe(
        word="A word",
        fetch_all_results="Decides whether the bot should fetch all the results instead of just 10. Default to False."
    )
    @app_commands.choices(fetch_all_results=[
        app_commands.Choice(name="true", value=1),
        app_commands.Choice(name="false", value=0)
    ])
    async def urban(self, interaction: Interaction, word: str, fetch_all_results: int = 0):
        """ Get the definition of a word from Urban Dictionary """
        print(f"> {interaction.user} used the command 'urban'.")
        await interaction.response.defer()
        global ret, length, index
        index = 1
        res = urban.run(word)
        id = str(interaction.id)
        if fetch_all_results == 0:
            length = len(res)
        else:
            length = urban.get_def_count(word)
        if len(res) == 0:
            await interaction.followup.send("That word is not defined yet. May be it's your time to define it?")
        else:
            ret[id] = {
                "word": word,
                "defs": res,
                "index": index,
                "max_index": length
            }
            view = UrbanView(timeout=900, id=id)
            await interaction.followup.send(f"""
1/{length}
{parse(res[0])}
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
