﻿import json

import aiohttp
import discord


async def anime(cmd, message, args):
    if args:
        qry = '%20'.join(args)
        url = f'https://kitsu.io/api/edge/anime?filter[text]={qry}'
        kitsu_icon = 'https://avatars3.githubusercontent.com/u/7648832?v=3&s=200'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.read()
                data = json.loads(data)
        if data['data']:
            ani_url = data['data'][0]['links']['self']
            async with aiohttp.ClientSession() as session:
                async with session.get(ani_url) as data:
                    data = await data.read()
                    data = json.loads(data)
                    data = data['data']
            attr = data['attributes']
            slug = attr['slug']
            synopsis = attr['synopsis']
            if 'en' in attr['titles']:
                en_title = attr['titles']['en']
            else:
                en_title = attr['titles']['en_jp']
            if 'ja_jp' in attr['titles']:
                jp_title = attr['titles']['ja_jp']
            else:
                jp_title = attr['titles']['en_jp']
            if 'averageRating' in attr:
                rating = attr['averageRating'][:5]
            else:
                rating = 'None'
            episode_count = attr['episodeCount']
            episode_length = attr['episodeLength']
            start_date = attr['startDate']
            end_date = attr['endDate']
            nsfw = attr['nsfw']
            if nsfw:
                nsfw = 'Yes (º﹃º)'
            else:
                nsfw = 'No (ಠ\\_ಠ)'
            anime_desc = f'Title: {jp_title}'
            anime_desc += f'\nRating: {rating}%'
            anime_desc += f'\nAir Time: {start_date} - {end_date}'
            anime_desc += f'\nEpisodes: {episode_count}'
            if episode_length:
                anime_desc += f'\nDuration: {episode_length} Minutes'
            else:
                anime_desc += '\nDuration: Unknown'
            anime_desc += f'\nIs NSFW: {nsfw}'
            response = discord.Embed(color=0xff3300)
            response.set_author(name=f'{en_title or jp_title}', icon_url=kitsu_icon,
                                url=f'https://kitsu.io/anime/{slug}')
            response.add_field(name='Information', value=anime_desc)
            response.add_field(name='Synopsis', value=f'{synopsis[:384]}...')
            if attr['posterImage']:
                poster_image = attr['posterImage']['original'].split('?')[0]
                response.set_thumbnail(url=poster_image)
            response.set_footer(text='Click the title at the top to see the page of the anime.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
