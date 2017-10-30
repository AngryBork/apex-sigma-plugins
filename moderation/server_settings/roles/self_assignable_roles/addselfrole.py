﻿import discord

from sigma.core.utilities.role_processing import matching_role


async def addselfrole(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_roles:
        if args:
            lookup = ' '.join(args)
            target_role = matching_role(message.guild, lookup)
            if target_role:
                role_bellow = bool(target_role.position < message.guild.me.top_role.position)
                if role_bellow:
                    selfroles = cmd.db.get_guild_settings(message.guild.id, 'SelfRoles')
                    if selfroles is None:
                        selfroles = []
                    if target_role.id in selfroles:
                        response = discord.Embed(color=0xBE1931, title='❗ This role is already self assignable.')
                    else:
                        selfroles.append(target_role.id)
                        cmd.db.set_guild_settings(message.guild.id, 'SelfRoles', selfroles)
                        response = discord.Embed(color=0x77B255, title=f'✅ {target_role.name} added.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I can\'t find {lookup} on this server.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Roles needed.', color=0xBE1931)
    await message.channel.send(embed=response)
