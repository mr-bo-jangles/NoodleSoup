# Import libraries
import os
import functools
import discord
from discord.ext import commands

# Declare intents to enable full perms
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Declare the bot
bot = commands.Bot(command_prefix="!!", intents=intents)


# Declare check functions
def check_for_any_roles(ctx, role_ids):
    getter = functools.partial(discord.utils.get, ctx.author.roles)
    return not any(
        getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in role_ids)


def check_for_all_roles(ctx, role_ids):
    getter = functools.partial(discord.utils.get, ctx.author.roles)
    return not all(
        getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in role_ids)


# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!!info"))
    print('We have logged in as {0.user}'.format(bot))


# Commands
@bot.command(name="rateme")
async def _rateme(ctx):
    if check_for_any_roles(ctx, ["Degenerate"]):  # Check for role ID
        await ctx.send("You don't have true big dick energy.")
    else:
        await ctx.send('You got that true BDE.')
    await ctx.message.delete()  # Delete command message
    print(f'rateme command called by {ctx.author}')  # Log command usage


@bot.command(name="getinvite")
async def _getinvite(ctx):
    if check_for_any_roles(ctx, ["Verified Member"]):  # Check for role ID
        await ctx.send(
            "I'm sorry, you do not have the permissions to do this.  "
            "This command is restricted to Verified Members and above.")  # Lockout user
    else:
        channel = discord.utils.get(ctx.guild.text_channels, name='dyno-logs')  # Get server logging channel
        await channel.send(f"I generated an invite for user {ctx.author.mention} at their request.")  # Post in channel
        target = discord.utils.get(ctx.guild.text_channels, name='welcome-to-cl')  # Get invite target channel
        invite = await target.create_invite(reason=f"User {ctx.author} used the getinvite command.",
                                            max_age=12 * 60 * 60, max_uses=1)  # Create 12h 1 use invite to target ch.
        await ctx.send(
            f'Here is your one-time-use invite link {ctx.author.mention}.  It will last for 12 hrs. {invite.url}')
        # ^^^ Post invite to user in context channel
    await ctx.message.delete()  # Delete command message
    print(f'getinvite command called by {ctx.author}')  # Log command usage


@bot.command(name="info")
async def _info(ctx):
    await ctx.send(
        "**Hello, I'm Noodle Soup.  I'm an assistant bot for Crash Landing.**\n*Here are the commands you can use.  "
        "If you require a certain role to use a command, it will be listed in brackets (Like So).  "
        "Remember to put a !! before your command.*\n \n**getinvite** - *(Verified Member)* - "
        "I will generate a one-time-use invite link for you to be able to send to a friend.  "
        "Note that use of this command is logged. ")  # Post helptext in context channel
    await ctx.message.delete()  # Delete command usage
    print(f'info command called by {ctx.author}')  # Log command usage


bot.run(os.environ['TOKEN'])
