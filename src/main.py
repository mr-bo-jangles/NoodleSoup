# Import libraries

import asyncio
import logging
import logging.handlers
import os

from typing import List, Optional

import discord
from discord.ext import commands
from aiohttp import ClientSession

from asynctinydb import TinyDB, UUID, Document, Query

from migrations import Migrations


class NoodleSoup(commands.Bot):
    def __init__(
            self,
            *args,
            initial_extensions: List[str],
            web_client: ClientSession,
            db: TinyDB,
            testing_guild_id: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        self.db = db

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.

        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.



    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="you reprobates"
            )
        )
        print('We have logged in as {0.user}'.format(self))


async def main():
    # When taking over how the bot process is run, you become responsible for a few additional things.

    # 1. logging

    # for this example, we're going to set up a rotating file logger.
    # for more info on setting up logging,
    # see https://discordpy.readthedocs.io/en/latest/logging.html and https://docs.python.org/3/howto/logging.html

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    # Alternatively, you could use:
    # discord.utils.setup_logging(handler=handler, root=False)

    # One of the reasons to take over more of the process though
    # is to ensure use with other libraries or tools which also require their own cleanup.

    # Here we have a web client and a database pool, both of which do cleanup at exit.
    # We also have our bot, which depends on both of these.

    db_location = os.getenv('DB_LOCATION', 'db.json')

    async with ClientSession() as our_client, TinyDB(db_location, sort_keys=True, indent=4, separators=(',', ': ')) as db:
        # 2. We become responsible for starting the bot.

        exts = ['restart', 'reset', 'get_invite', 'verify', 'dynamic_voice']

        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True

        migrations = Migrations(db=db)
        await migrations.first_migration()
        await migrations.second_migration()

        async with NoodleSoup(
                commands.when_mentioned_or("&&"),
                web_client=our_client,
                initial_extensions=exts,
                intents=intents,
                testing_guild_id=977914778762760292,
                db=db
        ) as bot:
            await bot.start(os.getenv('TOKEN', ''))


if __name__ == "__main__":
    # For most use cases, after defining what needs to run, we can just tell asyncio to run it:
    asyncio.run(main())
