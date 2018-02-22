import asyncio
import secrets

import aiohttp
import discord
from lxml import html

from .mech.utils import scramble

ongoing_list = []


async def animechargame(cmd, message, args):
    if message.channel.id not in ongoing_list:
        try:
            ongoing_list.append(message.channel.id)
            mal_icon = 'https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png'
            wait_embed = discord.Embed(color=0x1d439b)
            wait_embed.set_author(name='Hunting for a good specimen...', icon_url=mal_icon)
            working_response = await message.channel.send(embed=wait_embed)
            if args:
                if args[0].lower() == 'hint':
                    hint = True
                else:
                    hint = False
            else:
                hint = False
            ani_order = secrets.randbelow(3) * 50
            if ani_order:
                ani_top_list_url = f'https://myanimelist.net/topanime.php?limit={ani_order}'
            else:
                ani_top_list_url = 'https://myanimelist.net/topanime.php'
            async with aiohttp.ClientSession() as session:
                async with session.get(ani_top_list_url) as ani_top_list_session:
                    ani_top_list_html = await ani_top_list_session.text()
            ani_top_list_data = html.fromstring(ani_top_list_html)
            ani_list_objects = ani_top_list_data.cssselect('.ranking-list')
            ani_choice = secrets.choice(ani_list_objects)
            ani_url = ani_choice[1][0].attrib['href']
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{ani_url}/characters') as ani_page_session:
                    ani_page_html = await ani_page_session.text()
            ani_page_data = html.fromstring(ani_page_html)
            cover_object = ani_page_data.cssselect('.ac')[0]
            anime_cover = cover_object.attrib['src']
            anime_title = cover_object.attrib['alt'].strip()
            character_object_list = ani_page_data.cssselect('.borderClass')
            character_list = []
            for char_obj in character_object_list:
                if 'href' in char_obj[0].attrib:
                    if '/character/' in char_obj[0].attrib['href']:
                        character_list.append(char_obj)
            char_choice = secrets.choice(character_list)
            char_url = char_choice[0].attrib['href']
            async with aiohttp.ClientSession() as session:
                async with session.get(char_url) as char_page_session:
                    char_page_html = await char_page_session.text()
            char_page_data = html.fromstring(char_page_html)
            char_img_obj = char_page_data.cssselect('.borderClass')[0][0][0][0]
            char_img = char_img_obj.attrib['src']
            char_name = ' '.join(char_img_obj.attrib['alt'].strip().split(', '))
            await working_response.delete()
            question_embed = discord.Embed(color=0x1d439b)
            question_embed.set_image(url=char_img)
            question_embed.set_footer(text='You have 30 seconds to guess it.')
            question_embed.set_author(name=anime_title, icon_url=anime_cover, url=char_img)
            kud_reward = None
            name_split = char_name.split()
            for name_piece in name_split:
                if kud_reward is None:
                    kud_reward = len(name_piece)
                else:
                    if kud_reward >= len(name_piece):
                        kud_reward = len(name_piece)
            if hint:
                kud_reward = kud_reward // 2
                scrambled_name = scramble(char_name)
                question_embed.description = f'Name: {scrambled_name}'
            await message.channel.send(embed=question_embed)

            def check_answer(msg):
                if message.channel.id == msg.channel.id:
                    if msg.content.lower() in char_name.lower().split():
                        correct = True
                    elif msg.content.lower() == char_name.lower():
                        correct = True
                    else:
                        correct = False
                else:
                    correct = False
                return correct

            try:
                answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
                cmd.db.add_currency(answer_message.author, message.guild, kud_reward)
                author = answer_message.author.display_name
                currency = cmd.bot.cfg.pref.currency
                win_title = f'🎉 Correct, {author}, it was {char_name}. You won {kud_reward} {currency}!'
                win_embed = discord.Embed(color=0x77B255, title=win_title)
                await message.channel.send(embed=win_embed)
            except asyncio.TimeoutError:
                timeout_title = f'🕙 Time\'s up! It was {char_name} from {anime_title}...'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await message.channel.send(embed=timeout_embed)
        except IndexError:
            grab_error = discord.Embed(color=0xBE1931, title='❗ I failed to grab a character, try again.')
            await message.channel.send(embed=grab_error)
        if message.channel.id in ongoing_list:
            ongoing_list.remove(message.channel.id)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
        await message.channel.send(embed=ongoing_error)
