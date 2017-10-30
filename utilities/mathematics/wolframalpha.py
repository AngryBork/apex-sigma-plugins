﻿import discord
import wolframalpha as wa_wrapper

from sigma.plugins.minigames.quiz.mathgame import ongoing_list as math_chs


async def wolframalpha(cmd, message, args):
    if message.channel.id not in math_chs:
        if 'app_id' in cmd.cfg:
            if not args:
                response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
            else:
                wa_q = ' '.join(args)
                wac = wa_wrapper.Client(cmd.cfg['app_id'])
                results = wac.query(wa_q)
                try:
                    response = discord.Embed(type='rich', color=0x66cc66, title='✅ Processing Done')
                    for res in results.results:
                        if int(res['@numsubpods']) == 1:
                            response.add_field(name=res['@title'],
                                               value='```\n' + res['subpod']['plaintext'][:500] + '\n```')
                        else:
                            response.add_field(name=res['@title'],
                                               value='```\n' + res['subpod'][0]['img']['@title'][:500] + '\n```')
                except Exception:
                    title = '❗ We were unable to process that.'
                    response = discord.Embed(color=0xBE1931, title=title)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing API key.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Wolfram can\'t be used during an ongoing math game.')
    await message.channel.send(embed=response)
