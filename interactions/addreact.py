import secrets

import discord


async def addreact(cmd, message, args):
    if args:
        if len(args) >= 2:
            reaction_name = args[0]
            allowed_reactions = []
            for command in cmd.bot.modules.commands:
                if cmd.bot.modules.commands[command].category.lower() == 'interactions':
                    allowed_reactions.append(command)
            if reaction_name.lower() in allowed_reactions:
                reaction_url = '%20'.join(args[1:])
                if reaction_url.startswith('http'):
                    if reaction_url.endswith('.gif'):
                        exist_check = cmd.db[cmd.db.db_cfg.database]['Interactions'].find_one({'URL': reaction_url})
                        if not exist_check:
                            reaction_id = secrets.token_hex(4)
                            reaction_data = {
                                'Name': reaction_name.lower(),
                                'UserID': message.author.id,
                                'ServerID': message.guild.id,
                                'URL': reaction_url,
                                'ReactionID': reaction_id
                            }
                            cmd.db[cmd.db.db_cfg.database]['Interactions'].insert_one(reaction_data)
                            interactions = cmd.db[cmd.db.db_cfg.database]['Interactions'].find(
                                {'Name': reaction_name.lower()})
                            inter_count = len(list(interactions))
                            title = f'✅ Added **{reaction_name.lower()}** number **{inter_count}**.'
                            response = discord.Embed(color=0x77B255, title=title)
                            if 'log_ch' in cmd.cfg:
                                log_ch_id = cmd.cfg['log_ch']
                                log_ch = discord.utils.find(lambda x: x.id == log_ch_id, cmd.bot.get_all_channels())
                                if log_ch:
                                    author = f'{message.author.name}#{message.author.discriminator}'
                                    data_desc = f'Author: {author}'
                                    data_desc += f'\nAuthor ID: {message.author.id}'
                                    data_desc += f'\nGuild: {message.guild.name}'
                                    data_desc += f'\nGuild ID: {message.guild.id}'
                                    data_desc += f'\nReaction URL: [Here]({reaction_url})'
                                    data_desc += f'\nReaction ID: {reaction_id}'
                                    log_resp_title = f'🆙 Added {reaction_name.lower()} number {inter_count}'
                                    log_resp = discord.Embed(color=0x3B88C3)
                                    log_resp.add_field(name=log_resp_title, value=data_desc)
                                    log_resp.set_thumbnail(url=reaction_url)
                                    await log_ch.send(embed=log_resp)
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ Reaction already exists.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ Reaction URL must end with .gif.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ Not a valid URL.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Unrecognized interaction name.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing inputted.')
    await message.channel.send(embed=response)
