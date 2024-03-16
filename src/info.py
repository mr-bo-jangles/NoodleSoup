from discord.app_commands import commands


@commands.command(name="info")
async def _info(ctx):
    await ctx.send(
        "**Hello, I'm Noodle Soup.  I'm an assistant bot for Crash Landing.**\n*Here are the commands you can use.  "
        "If you require a certain role to use a command, it will be listed in brackets (Like So).  "
        "Remember to put a !! before your command.*\n \n**verify** - *(No Requirement)* - "
        "I will notify Curators to start your verification progress, and give you the RSI link.  "
        "Note that use of this command is logged. "
        "\n**getinvite** - *(Verified Member)* - "
        "I will generate a one-time-use invite link for you to be able to send to a friend.  "
        "Note that use of this command is logged. "
    )  # Post helptext in context channel
    await ctx.message.delete()  # Delete command usage
    print(f'info command called by {ctx.author}')  # Log command usage

async def setup(bot: commands):
    bot.tree.add_command(_info)