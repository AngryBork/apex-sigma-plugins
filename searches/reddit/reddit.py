import functools
import secrets
from concurrent.futures import ThreadPoolExecutor

import discord
import praw
from prawcore.exceptions import Redirect, NotFound

reddit_client = None
threads = ThreadPoolExecutor(max_workers=2)


def grab_post(subreddit, argument):
    if argument == 'tophot':
        post = list(subreddit.hot(limit=1))[0]
    elif argument == 'topnew':
        post = list(subreddit.new(limit=1))[0]
    elif argument == 'randomnew':
        post = secrets.choice(list(subreddit.new(limit=100)))
    elif argument == 'toptop':
        post = list(subreddit.top(limit=1))[0]
    elif argument == 'randomtop':
        post = secrets.choice(list(subreddit.top(limit=100)))
    else:
        post = secrets.choice(list(subreddit.hot(limit=100)))
    return post


async def reddit(cmd, message, args):
    global reddit_client
    if 'client_id' in cmd.cfg and 'client_secret' in cmd.cfg:
        if args:
            client_id = cmd.cfg['client_id']
            client_secret = cmd.cfg['client_secret']
            if reddit_client is None:
                reddit_client = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='Apex Sigma')
            subreddit = args[0]
            argument = args[-1].lower()
            try:
                subreddit = reddit_client.subreddit(subreddit)
                grab_func = functools.partial(grab_post, subreddit, argument)
                try:
                    post = await cmd.bot.loop.run_in_executor(threads, grab_func)
                except NotFound:
                    post = None
                if post:
                    if not post.over_18 or message.channel.is_nsfw():
                        reddit_icon = 'https://i.imgur.com/5w7eJ5A.png'
                        post_desc = f'Author: {post.author.name}'
                        post_desc += f' | Score: {post.score}'
                        post_desc += f' | Views: {post.view_count}'
                        author_link = f'https://www.reddit.com{post.permalink}'
                        response = discord.Embed(color=0xcee3f8)
                        response.set_author(name=post.title, url=author_link, icon_url=reddit_icon)
                        response.set_footer(text=post_desc)
                        try:
                            if post.preview:
                                if 'images' in post.preview:
                                    prev_img = post.preview['images'][0]['source']['url']
                                    response.set_image(url=prev_img)
                        except AttributeError:
                            pass
                    else:
                        nsfw_warning = '❗ NSFW Subreddits and posts are not allowed here.'
                        response = discord.Embed(color=0xBE1931, title=nsfw_warning)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ No such subreddit.')
            except Redirect:
                response = discord.Embed(color=0xBE1931, title='❗ No such subreddit.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
