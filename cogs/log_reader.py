import inspect
import os
import discord
import re
import hashlib
import tempfile

from utils import translate
from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class Reader(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        attachments = message.attachments
        if len(attachments) != 0:
            try:
                d = 0
                for attachment in attachments:
                    if re.match("latestlog.*\.txt", attachment.filename) is not None:
                        d = 1
                        print(f"> {message.author} sent a log.")
                        file = await attachment.read()
                        hash = hashlib.sha1(file).hexdigest()
                        path = "/tmp/duyismbot." + hash
                        if not os.path.isfile(path):
                            with open(path, 'w') as f:
                                f.write(str(file))
                            print(f"> Log saved to {path}")
                        else:
                            print("> Not saving log, it has been saved before")
                if "delete" in message.content and d == 1:
                    await message.delete()
            except discord.HTTPException:
                print("> Couldn't load the log!")


async def setup(client):
    await client.add_cog(Reader(client))
