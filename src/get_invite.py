import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog


from src.utils import check_for_any_roles

class GetInvite(Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="getinvite", description="Generates a safe invite link for you to share")
    async def _get_invite(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if check_for_any_roles(interaction.user, ["Verified Member"]):  # Check for role ID
            await interaction.followup.send(
                "I'm sorry, you do not have the permissions to do this.  "
                "This command is restricted to Verified Members and above."
            )  # Lockout user
        else:
            channel = discord.utils.get(interaction.guild.text_channels, name='dyno-logs')  # Get server logging channel
            await channel.send(f"I generated an invite for user {interaction.user.mention} at their request.")  # Post in channel
            target = discord.utils.get(interaction.guild.text_channels, name='welcome-to-cl')  # Get invite target channel
            invite = await target.create_invite(
                reason=f"User {interaction.user} used the getinvite command.",
                max_age=12 * 60 * 60,
                max_uses=1
            )  # Create 12h 1 use invite to target ch.
            await interaction.followup.send(
                f'Here is your one-time-use invite link {interaction.user.mention}. It will last for 12 hrs -> {invite.url}'
            )
            # ^^^ Post invite to user in context channel
        print(f'getinvite command called by {interaction.user}')  # Log command usage

async def setup(bot):
    get_invite = GetInvite(bot=bot)
    await bot.add_cog(get_invite)