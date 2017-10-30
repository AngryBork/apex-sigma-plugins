import aiohttp
from lxml import html


async def csshumor(cmd, message, args):
    url = 'https://csshumor.com/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.text()
    root = html.fromstring(data)
    codeblock = root.cssselect('.crayon-code')[0]
    codeblock_content = codeblock.text_content()
    await message.channel.send(f'```css\n{codeblock_content}\n```')
