import json
import aiohttp

session_id_cache = []

async def chat_bot(ev, message):
    active = ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
    if active:
        mention = f'<@{ev.bot.user.id}>'
        mention_alt = f'<@!{ev.bot.user.id}>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            args = message.content.split(' ')
            interaction = ' '.join(args[1:])
            if message.mentions:
                for mnt in message.mentions:
                    interaction = interaction.replace(mnt.mention, mnt.name)
            bot_url = f'http://www.zabaware.com/webhal/chat.asp?q={interaction}'
            async with aiohttp.ClientSession() as session:
                async with session.get(bot_url) as data:
                    data = await data.read()
                    data = json.loads(data)
            response = f'{message.author.mention} {data["HalResponse"]}'
            await message.channel.send(response)