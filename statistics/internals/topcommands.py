import discord
from humanfriendly.tables import format_pretty_table as boop


def count_all_commands(db):
    dbase = db[db.db_cfg.database]
    cmd_items = dbase['CommandStats'].aggregate(
        [
            {"$group": {
                "_id": {
                    "command": "$command.name",
                },
                "count": {"$sum": 1}
            }}
        ]
    )
    output = {}
    total = 0
    for x in cmd_items:
        output.update({x['_id']['command']: x['count']})
        total += x['count']
    return output, total


async def topcommands(cmd, message, args):
    cmd_dict, total = count_all_commands(cmd.db)
    cmd_key_list = sorted(cmd_dict, key=cmd_dict.__getitem__, reverse=True)
    stats_top = f'A total of {total} commands have been recorded.'
    stats_desc_list = []
    for cmd_key in cmd_key_list[:20]:
        stats_desc_list.append([cmd_key, cmd_dict[cmd_key]])
    stats_desc = f'```py\n{boop(stats_desc_list)}\n```'
    response = discord.Embed(color=0x1B6F5F)
    response.add_field(name='Command Count', value=stats_top, inline=False)
    response.add_field(name='Command List', value=stats_desc, inline=False)
    await message.channel.send(embed=response)
