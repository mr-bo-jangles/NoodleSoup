import logging

import discord
from discord import app_commands, VoiceState, Member
from discord.ext import commands, tasks
from discord.ext.commands import Cog
from asynctinydb import Document

from main import NoodleSoup
from utils import admin_check

logger = logging.getLogger('discord')
INITIAL_DOCUMENT_COUNT = 1

class DynamicVoice(Cog):

    def __init__(self, bot: NoodleSoup):
        self.bot = bot
        self.channel_observe.start()

    def cog_unload(self):
        self.channel_observe.cancel()

    @tasks.loop(minutes=5)
    async def channel_observe(self):
        i = 0
        for guild in self.bot.guilds:
            channel_list = guild.voice_channels
            for x in channel_list:
                deleted = await self.safe_delete_channel(x)
                if deleted:
                    i += 1
            if i > 0:
                pass


    @channel_observe.before_loop
    async def before_channel_observe(self):
        print('waiting...')
        await self.bot.wait_until_ready()


    async def safe_delete_channel(self, channel: discord.VoiceChannel) -> bool:
        if await self.is_in_createdchannel_table(channel.id) and channel.members == []:
            gen_channels = self.bot.db.table("gen_channels")
            created_channels = self.bot.db.table("created_channels")
            assoc_id = await created_channels.get(doc_id=channel.id)
            parent_id = assoc_id.get("parent", 0)
            parent = await gen_channels.get(doc_id=parent_id)
            children = parent.get("children", {})
            new_children = {key:value for (key,value) in children.items() if value != channel.id}
            await gen_channels.update({"children": new_children}, doc_ids=[parent_id])
            await created_channels.remove(doc_ids=[channel.id])
            print(f" Deleted {channel.name} \n -----------------------------------------")
            await channel.delete(reason="No members in generated channel.")
            return True
        else:
            return False


    def was_disconnected(self, before: VoiceState, after: VoiceState):
        return before.channel is None and after.channel is not None

    def has_joined(self, before: VoiceState, after: VoiceState):
        if before.channel is None or after.channel is None:
            return False
        return before.channel.id != after.channel.id


    def in_chat_category(self, voice_state: VoiceState, channel_category_id: int):
        return voice_state.channel.category_id == channel_category_id

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if (self.was_disconnected(before=before, after=after) or self.has_joined(before=before, after=after)) and await self.is_in_genchannel_table(after.channel.id
        ):
            gen_channels = self.bot.db.table("gen_channels")
            document = await gen_channels.get(doc_id=after.channel.id)
            children = document.get("children", {})
            print("NEW CHANNEL CREATION")
            print(f"Request from {member.name}")
            print(f"{after.channel.name}")
            print(f"Children: {children}.  Checking Indexes...")
            for index in range(1, len(children)+2):
                child = children.get(str(index))
                print(f"{index}")
                if child is not None:
                    continue
                else:
                    print(f"First free index: {index}")
                    new_channel = await after.channel.category.create_voice_channel(
                        name=f"{after.channel.name.replace('Create', '')} {index}",
                        position=after.channel.position+index,
                    )
                    await new_channel.edit(position=after.channel.position+index)
                    await gen_channels.update({"children": { **children, str(index): new_channel.id}}, doc_ids=[after.channel.id])
                    created_channels = self.bot.db.table("created_channels")
                    await created_channels.insert(Document({'name': new_channel.name, 'parent': after.channel.id}, doc_id=new_channel.id))
                    # await new_channel.edit(status="I want to set a status too")
                    await member.move_to(new_channel, reason="Moved member to their generated voice channel")
                    print(f"Created {new_channel.name}, id {new_channel.id} \n -----------------------------------------")
                    break


    async def is_in_genchannel_table(self, channel_id: int):
        gen_channels = self.bot.db.table("gen_channels")
        return await gen_channels.contains(doc_id=channel_id)

    async def is_in_createdchannel_table(self, channel_id: int):
        created_channels = self.bot.db.table("created_channels")
        return await created_channels.contains(doc_id=channel_id)

    def in_channel_name(self, voice_state, channel_name: str):
        return voice_state.channel.name == channel_name

    @app_commands.describe(category="The category this channel be in",
                           name="Name of this channel's \bchildren\b")
    @app_commands.command(name="createdynamicvoice", description="Creates a new dynamic voice generator channel")
    async def _create_dynamic_voice(self, interaction: discord.Interaction, category: discord.CategoryChannel, name: str):
        await interaction.response.defer(ephemeral=True)
        if admin_check(interaction):
            channel = await interaction.guild.create_voice_channel(
                name=f"Create {name}",
                overwrites={},
                category=category,
                position=len(interaction.channel.category.channels),
                bitrate=64_000,
                user_limit=1,
                video_quality_mode=discord.VideoQualityMode.auto
            )
            gen_channels = self.bot.db.table("gen_channels")
            await gen_channels.insert(Document({'name': channel.name, 'children': {}}, doc_id=channel.id))
            await interaction.followup.send(f"{name} channel created in {category}.")
        else:
            await interaction.followup.send("This command is locked to Curators only.")
    @app_commands.describe(channel="The channel to register with the bot as a dynamic voice channel",
                           name="Channel to register")
    @app_commands.command(name="registerdynamicvoice", description="Register existing dynamic voice generator channel")
    async def _register_dynamic_voice(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await interaction.response.defer(ephemeral=True)
        if admin_check(interaction):
            gen_channels = self.bot.db.table("gen_channels")
            if gen_channels.contains(doc_id=channel.id):
                await interaction.followup.send(f"{channel.name} channel already registered in DB.")
                return
            await gen_channels.insert(Document({'name': channel.name, 'children': {}}, doc_id=channel.id))
            await interaction.followup.send(f"{channel.name} channel registered in DB.")
        else:
            await interaction.followup.send("This command is locked to Curators only.")

    @app_commands.command(name="deletedynamicvoice", description="Delete a dynamic voice generator channel")
    async def _delete_dynamic_voice(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await interaction.response.defer(ephemeral=True)
        if admin_check(interaction):
            name = channel.name
            category = channel.category
            await channel.delete(reason="Deleted at curator request.")
            gen_channels = self.bot.db.table("gen_channels")
            await gen_channels.remove(doc_ids=[channel.id])
            await interaction.followup.send(f"{name} deleted from {category}.")
        else:
            await interaction.followup.send("This command is locked to Curators only.")

async def setup(bot):
    dynamic_voice = DynamicVoice(bot=bot)
    await bot.add_cog(dynamic_voice)