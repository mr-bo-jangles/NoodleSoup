import discord
from discord.app_commands import commands



@commands.command(name="test", description="posts to sandbox")
async def _test(ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name='dyno-logs')
    await channel.send("Test print")

async def setup(bot: commands):
    bot.tree.add_command(_test)