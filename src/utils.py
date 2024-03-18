import functools

import discord

CURATOR_ROLE_ID = 977917138109087775


def check_for_any_roles(user: discord.Member, role_ids):
    getter = functools.partial(discord.utils.get, user.roles)
    return not any(
        getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in role_ids
    )


def time_to_int(dateobj):
    total = int(dateobj.strftime('%S'))
    total += int(dateobj.strftime('%M')) * 60
    total += int(dateobj.strftime('%H')) * 60 * 60
    total += (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total


def admin_check(ctx: discord.Interaction):
    role = discord.utils.get(ctx.guild.roles, id=CURATOR_ROLE_ID)
    if role in ctx.user.roles:
        return True
    else:
        return False
