import discord
import datetime as dt
from discord.app_commands import commands
from src.utils import check_for_any_roles, time_to_int, CURATOR_ROLE_ID


@commands.command(name="verify")
async def _verify(ctx):
    if check_for_any_roles(ctx, ["Verified Member"]):  # Check for role ID
        if check_for_any_roles(ctx, ["Server Visitor"]):
            joindate = ctx.author.joined_at
            joinint = time_to_int(joindate)
            currentdate = dt.datetime.now()
            currentint = time_to_int(currentdate)
            duration = (currentint - joinint) / (60 * 60 * 24)
            print(duration)
            if duration >= 6.9:
                channel = discord.utils.get(ctx.guild.text_channels, name='dyno-logs')  # Get server logging channel
                role = discord.utils.get(ctx.guild.roles, id=CURATOR_ROLE_ID)  # Get Curator role
                await channel.send(
                    f"{role.mention} User {ctx.author.mention} has requested verification!"
                )  # Post notif at curators

                await ctx.send(
                    f'{ctx.author.mention}I have let the Curators know that you want to be verified.\n '
                    'Please make sure you are registered here: https://robertsspaceindustries.com/orgs/CRSHLANDIN'
                )

            else:
                await ctx.send(
                    f'{ctx.author.mention}I am sorry, but you need to be on our discord for 7 days before you can be '
                    f'verified (your time is currently {round(duration, 1)} days).  Please try again later.'
                )

        else:
            await ctx.send(
                f'You cannot verify for SC membership as a Visitor,{ctx.author.mention}.'
            )
            # ^^^ Post notif to user in context channel

    else:
        await ctx.send(
            f'It seems you are already verified,{ctx.author.mention}.')
        # ^^^ Post notif to user in context channel
    await ctx.message.delete()  # Delete command message
    print(f'verify command called by {ctx.author}')  # Log command usage


async def setup(bot: commands):
    bot.tree.add_command(_verify)
