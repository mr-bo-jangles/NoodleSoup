import logging

import discord
from discord import app_commands, VoiceState, Member
from discord.ext import commands
from discord.ext.commands import Cog
from asynctinydb import Query, Document


from src.utils import admin_check

logger = logging.getLogger('discord')

class DynamicVoice(Cog):

    def __init__(self, bot):
        self.bot = bot

    def was_disconnected(self, before: VoiceState, after: VoiceState):
        return before.channel is None and after.channel is not None

    def in_chat_category(self, voice_state: VoiceState, channel_category_id: int):
        return voice_state.channel.category_id == channel_category_id

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if self.was_disconnected(
                before=before,
                after=after
        ) and self.in_chat_category(
            voice_state=after,
            channel_category_id=977917561243062322
        ) and await self.is_in_channel_table(after.channel.id
        ):
            channel = discord.utils.get(member.guild.text_channels, name='dyno-logs')
            await channel.send("Curator just joined the test voice channel, creating and moving.")
            new_channel = await after.channel.category.create_voice_channel(
                name=f"{after.channel.name} channel {(len(after.channel.category.voice_channels)-1)}",
                position=len(after.channel.category.channels),
            )
            # await new_channel.edit(status="I want to set a status too")
            await member.move_to(new_channel, reason="Moved member to generated voice channel")

    async def is_in_channel_table(self, channel_id: int):
        gen_channels = self.bot.db.table("gen_channels")
        return await gen_channels.contains(doc_id=channel_id)


    def in_channel_name(self, voice_state, channel_name: str):
        return voice_state.channel.name == channel_name

    @app_commands.command(name="createdynamicvoice", description="Create a dynamic voice channel")
    async def _create_dynamic_voice(self, interaction: discord.Interaction, category: discord.CategoryChannel, name: str):
        logger.info("fuck me")
        await interaction.response.defer(ephemeral=True)
        if admin_check(interaction):
            channel = await interaction.guild.create_voice_channel(
                name=name,
                overwrites={},
                category=category,
                position=len(interaction.channel.category.channels),
                bitrate=64_000,
                user_limit=0,
                video_quality_mode=discord.VideoQualityMode.auto
            )
            gen_channels = self.bot.db.table("gen_channels")
            await gen_channels.insert(Document({'name': channel.name}, doc_id=channel.id))
            await interaction.followup.send(f"{name} channel created in {category}.")
        else:
            await interaction.followup.send("This command is locked to Curators only.")


async def setup(bot):
    dynamic_voice = DynamicVoice(bot=bot)
    await bot.add_cog(dynamic_voice)