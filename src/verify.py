import discord
import datetime as dt
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog


from src.utils import check_for_any_roles, time_to_int, CURATOR_ROLE_ID

class Verify(Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot


    @app_commands.command(name="verify", description="Requests full server verification for your account")
    async def _verify(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if check_for_any_roles(interaction.user, ["Verified Member"]):  # Check for role ID
            if check_for_any_roles(interaction.user, ["Server Visitor"]):
                joindate = interaction.user.joined_at
                joinint = time_to_int(joindate)
                currentdate = dt.datetime.now()
                currentint = time_to_int(currentdate)
                duration = (currentint - joinint) / (60 * 60 * 24)
                print(duration)
                if duration >= 6.9:
                    channel = discord.utils.get(interaction.guild.text_channels, name='dyno-logs')  # Get server logging channel
                    role = discord.utils.get(interaction.guild.roles, id=CURATOR_ROLE_ID)  # Get Curator role
                    await channel.send(
                        f"{role.mention} User {interaction.user.mention} has requested verification!"
                    )  # Post notif at curators

                    await interaction.followup.send(
                        f'{interaction.user} I have let the Curators know that you want to be verified.\n '
                        'Please make sure you are registered here: https://robertsspaceindustries.com/orgs/CRSHLANDIN'
                    )

                else:
                    await interaction.followup.send(
                        f'I am sorry, but you need to be on our discord for 7 days before you can be '
                        f'verified (your time is currently {round(duration, 1)} days).  '
                        f'Please try again in {7-round(duration, 1)} days'
                    )

            else:
                await interaction.followup.send(
                    f'You cannot verify for SC membership as a Visitor, {interaction.user}.  '
                    f'You need to be an Unverified Member.'
                )
                # ^^^ Post notif to user in context channel

        else:
            await interaction.followup.send(
                f'It seems you are already verified, {interaction.user.mention}.')
            # ^^^ Post notif to user in context channel
        print(f'verify command called by {interaction.user}')  # Log command usage


async def setup(bot):
    verify = Verify(bot=bot)
    await bot.add_cog(verify)
