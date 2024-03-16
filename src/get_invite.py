import discord
from discord.app_commands import commands

from src.utils import check_for_any_roles


@commands.command(name="getinvite")
async def _get_invite(ctx):
    if check_for_any_roles(ctx, ["Verified Member"]):  # Check for role ID
        await ctx.send(
            "I'm sorry, you do not have the permissions to do this.  "
            "This command is restricted to Verified Members and above."
        )  # Lockout user
    else:
        channel = discord.utils.get(ctx.guild.text_channels, name='dyno-logs')  # Get server logging channel
        await channel.send(f"I generated an invite for user {ctx.author.mention} at their request.")  # Post in channel
        target = discord.utils.get(ctx.guild.text_channels, name='welcome-to-cl')  # Get invite target channel
        invite = await target.create_invite(
            reason=f"User {ctx.author} used the getinvite command.",
            max_age=12 * 60 * 60,
            max_uses=1
        )  # Create 12h 1 use invite to target ch.
        await ctx.send(
            f'Here is your one-time-use invite link {ctx.author.mention}. It will last for 12 hrs. {invite.url}'
        )
        # ^^^ Post invite to user in context channel
    await ctx.message.delete()  # Delete command message
    print(f'getinvite command called by {ctx.author}')  # Log command usage

async def setup(bot: commands):
    bot.tree.add_command(_get_invite)