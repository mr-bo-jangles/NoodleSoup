import sys

import discord
from discord.app_commands import commands

from src.utils import CURATOR_ROLE_ID


@commands.command(name="restart")
async def _restart(ctx):
    role = discord.utils.get(ctx.guild.roles, id=CURATOR_ROLE_ID)
    if role in ctx.author.roles:
        sys.exit(0)


async def setup(bot: commands):
    bot.tree.add_command(_restart)
