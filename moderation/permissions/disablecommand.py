﻿import discord

from .nodes.permission_data import get_all_perms


async def disablecommand(cmd, message, args):
    if args:
        if not message.author.permissions_in(message.channel).manage_guild:
            response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
        else:
            cmd_name = args[0].lower()
            if cmd_name in cmd.bot.modules.alts:
                cmd_name = cmd.bot.modules.alts[cmd_name]
            if cmd_name in cmd.bot.modules.commands:
                perms = get_all_perms(cmd.db, message)
                disabled_commands = perms['DisabledCommands']
                if cmd_name in disabled_commands:
                    response = discord.Embed(color=0xFFCC4D, title='⚠ Command Already Disabled')
                else:
                    disabled_commands.append(cmd_name)
                    perms.update({'DisabledCommands': disabled_commands})
                    cmd.db[cmd.db.db_cfg.database].Permissions.update_one({'ServerID': message.guild.id},
                                                                          {'$set': perms})
                    response = discord.Embed(color=0x77B255, title=f'✅ `{cmd_name.upper()}` disabled.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 Command Not Found')
        await message.channel.send(embed=response)
