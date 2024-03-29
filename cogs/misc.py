import datetime
import inspect
import os

import inspect
import os
import random
from discord import Interaction, app_commands, TextChannel
from discord.ext import commands
from utils import lunar

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class MiscCog(commands.GroupCog, group_name="misc"):
    def __init__(self, client):
        self.client = client


    @app_commands.command()
    @app_commands.describe(date="A date in ISO format. Example: 2022-07-19")
    async def lunar(self, interaction: Interaction, date: str = datetime.date.today().isoformat()):
        """ Get the lunar date """
        print(f"> {interaction.user} used the command 'lunar'.")
        await interaction.response.defer()
        await interaction.followup.send(lunar.run(date))


    @app_commands.command()
    async def badge(self, interaction: Interaction):
        """ For the surprise """
        print(f"> {interaction.user} used the command 'badge'.")

        await interaction.response.defer()
        await interaction.followup.send(inspect.cleandoc(f"""
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


    @app_commands.command()
    @app_commands.describe(
        string="A message",
        channel="Channel to send message to",
        effect="An additional effect. Defaults to none."
    )
    @app_commands.choices(effect=[
        app_commands.Choice(name="morse", value=2),
        app_commands.Choice(name="weeb", value=1),
        app_commands.Choice(name="none", value=0)
    ])
    async def say(self, interaction: Interaction, string: str, channel: TextChannel, effect: int = 0):
        """ Make the bot say something """
        print(f"> {interaction.user} used the command 'say'.")
        user = interaction.user
        await interaction.response.defer()
        if not channel.permissions_for(channel.guild.me).send_messages:
            await interaction.followup.send("I don't have permission to send messages to <#{}>. Sorry~".format(channel.id))
        elif not channel.permissions_for(user).send_messages:
            await interaction.followup.send("You don't have permission to send messages to <#{}>.".format(channel.id))
        else:
            final_string = string
            await interaction.followup.send(content="Done.")
            if effect == 1:
                weeb = str.maketrans({
                    "r": "w", "l": "w", "R": "W",
                    "L": "W", "u": "yu", "U": "yU"
                })
                smileys = [
                    "(ᵘʷᵘ)", "(ᵘﻌᵘ)", "(◡ ω ◡)", "(◡ ꒳ ◡)",
                    "(◡ w ◡)", "(◡ ሠ ◡)", "(˘ω˘)", "(⑅˘꒳˘)",
                    "(˘ᵕ˘)", "(˘ሠ˘)", "(˘³˘)", "(˘ε˘)", "(˘˘˘)",
                    "( ᴜ ω ᴜ )", "(„ᵕᴗᵕ„)", "(ㅅꈍ ˘ ꈍ)", "(⑅˘꒳˘)",
                    "( ｡ᵘ ᵕ ᵘ ｡)", "( ᵘ ꒳ ᵘ ✼)", "( ˘ᴗ˘ )",
                    "(ᵕᴗ ᵕ⁎)", "*:･ﾟ✧(ꈍᴗꈍ)✧･ﾟ:*", "*˚*(ꈍ ω ꈍ).₊̣̇.",
                    "(。U ω U。)", "(U ᵕ U❁)", "(U ﹏ U)",
                    "(◦ᵕ ˘ ᵕ◦)", "ღ(U꒳Uღ)", "♥(。U ω U。)",
                    "– ̗̀ (ᵕ꒳ᵕ) ̖́-", "( ͡U ω ͡U )", "( ͡o ᵕ ͡o )",
                    "( ͡o ꒳ ͡o )", "( ˊ.ᴗˋ )", "(ᴜ‿ᴜ✿)", "~(˘▾˘~)",
                    "(｡ᴜ‿‿ᴜ｡)", "uwu", "owo"
                ]
                final_string = string.translate(weeb) + ' ' + random.choice(smileys)
            if effect == 2:
                morse = str.maketrans({
                    "a": "•-", "b": "-•••", "c": "-•-•", "d": "-••",
                    "e": "•", "f": "••-•", "g": "--•", "h": "••••",
                    "i": "••", "j": "•---", "k": "-•-", "l": "•-••",
                    "m": "--", "n": "-•", "o": "---", "p": "•--•",
                    "q": "--•-", "r": "•-•", "s": "•••", "t": "-",
                    "u": "••-", "v": "•••-", "w": "•--", "x": "-••-",
                    "y": "-•--", "z": "--••", "0": "-----",
                    "1": "•----", "2": "••---", "3": "•••--",
                    "4": "••••-", "5": "•••••", "6": "-••••",
                    "7": "--•••", "8": "---••", "9": "----•",
                    ".": "•-•-•-", ",": "--••--", "?": "••--••",
                    "'": "•----•", ")": "-•--•-", ":": "---•••",
                    ";": "-•-•-•", "-": "-••••-", "_": "••--•-",
                    "\"": "•-••-•", "ŝ": "•••-•", "&": "•-•••",
                    "à": "•--•-", "ä": "•-•-", "å": "•--•-",
                    "æ": "•-•-", "ą": "•-•-", "ć": "-•-••",
                    "ĉ": "-•-••", "ç": "-•-••", "ĥ": "----",
                    "š": "----", "đ": "••-••", "ð": "••--•",
                    "é": "••-••", "ę": "••-••", "ĝ": "--•-•",
                    "ĵ": "•---•", "ł": "•-••-", "è": "•-••-",
                    "ń": "--•--", "ñ": "--•--", "ó": "---•",
                    "ö": "---•", "ø": "---•", "ś": "•••-•••",
                    "þ": "•--••", "ŭ": "••--", "ź": "--••-•",
                    "ż": "--••-"
                })
                morse_digraphs = str.maketrans({
                    "!": "kw", "/": "dn", "(": "kn", "&": "as",
                    "=": "bt", "+": "rn", "$": "sx", "@": "ac"
                })
                final_string = ' '.join(string.lower()).translate(morse_digraphs).translate(morse).replace("   ", " / ")
#                if final_string.replace('•', '').replace('-', '').replace(' ', '') is not None:
#                    final_string = string + "\n(not convertible)"
            await channel.send(content=f"{user} says: \n\n*{final_string}*")


async def setup(client):
    await client.add_cog(MiscCog(client))
