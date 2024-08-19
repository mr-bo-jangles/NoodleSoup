import sys

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from migrations import MIGRATION_TABLE
from utils import admin_check

class Reset(Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(name="reset", description="Resets all channel data in NoodleSoup")
    async def _restart(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if admin_check(interaction):
            await interaction.followup.send("Resetting...")
            await self.bot.db.drop_table(MIGRATION_TABLE)
            sys.exit(0)
        else:
            await interaction.followup.send("Only Curators can do this. Please get in touch with us if there's a problem!")

async def setup(bot):
    reset = Reset(bot=bot)
    await bot.add_cog(reset)


