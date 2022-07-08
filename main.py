# Import libraries
import os
import functools
import discord as discord
from discord.ext import commands
from keep_alive import keep_alive, end_keep_alive
# Declare intents to enable full perms
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Declare the bot
bot = commands.Bot(command_prefix="!!", intents=intents)


def check_for_any_roles(ctx, role_ids):
    getter = functools.partial(discord.utils.get, ctx.author.roles)
    return not any(getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in role_ids)


def check_for_all_roles(ctx, role_ids):
    getter = functools.partial(discord.utils.get, ctx.author.roles)
    return not all(getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in role_ids)

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!!info"))
  print('We have logged in as {0.user}'.format(bot))

# Commands
@bot.command(name="rateme")
async def _rateme(ctx):  # Define the command as async with default context and the trigger string
    if check_for_any_roles(ctx, ["Degenerate"]):  # Check for role ID
        await ctx.send("You don't have true big dick energy.")
        await ctx.message.delete()
    else:
        await ctx.send('You got that true BDE.')
        await ctx.message.delete() # Send back a message to the context consisting of a string


@bot.command(name="getinvite")
async def _getinvite(ctx):  # Define the command as async with default context and the trigger string
    if check_for_any_roles(ctx, ["Verified Member"]):  # Check for role ID
        await ctx.send("I'm sorry, you do not have the permissions to do this.  This command is restricted to Verified Members and above.")
        await ctx.message.delete()
    else:
        channel = discord.utils.get(ctx.guild.text_channels, name='dyno-logs')
        await channel.send(f"I generated an invite for user {ctx.author.mention} at their request.")
        target = discord.utils.get(ctx.guild.text_channels, name='welcome-to-cl')
        invite = await target.create_invite(reason=f"User {ctx.author} used the getinvite command.", max_age=12 * 60 * 60, max_uses=1)
        await ctx.send(f'Here is your one-time-use invite link {ctx.author.mention}.  It will last for 12 hrs. {invite.url}')
        await ctx.message.delete()

@bot.command(name="info")
async def _info(ctx):
  await ctx.send("**Hello, I'm Noodle Soup.  I'm an assistant bot for Crash Landing.**\n*Here are the commands you can use.  If you require a certain role to use a command, it will be listed in brackets (Like So).  Remember to put a !! before your command.*\n \n**getinvite** - *(Verified Member)* - I will generate a one-time-use invite link for you to be able to send to a friend.  Note that use of this command is logged. ")
  await ctx.message.delete()


process = keep_alive()
bot.run(os.environ['TOKEN'])
end_keep_alive(process)