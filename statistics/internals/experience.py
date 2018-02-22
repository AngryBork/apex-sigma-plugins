import discord

from sigma.core.utilities.data_processing import user_avatar


async def experience(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar = user_avatar(target)
    exp = cmd.db.get_experience(target, message.guild)
    response = discord.Embed(color=0x47ded4)
    response.set_author(name=f'{target.display_name}\'s Experience Data', icon_url=avatar)
    guild_title = '🎪 Local'
    global_title = '🌍 Global'
    local_level = int((exp['guild'] // ((((exp['guild'] // 690) * 0.0125) + 1) * 690)))
    global_level = int((exp['global'] // ((((exp['global'] // 690) * 0.0125) + 1) * 690)))
    response.add_field(name=guild_title, value=f"```py\nXP: {exp['guild']}\nLevel: {local_level}\n```", inline=True)
    response.add_field(name=global_title, value=f"```py\nXP: {exp['global']}\nLevel: {global_level}\n```", inline=True)
    response.set_footer(text=f'🔰 Experience is earned by being an active Sigma user.')
    await message.channel.send(embed=response)
