import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter
from contextlib import redirect_stdout
from ext.utility import load_json
from urllib.parse import quote as uriquote
from lxml import etree
from ext import fuzzy
from ext import embedtobox
from PIL import Image
import unicodedata
import traceback
import textwrap
import aiohttp
import inspect
import asyncio
import time
import re
import io
import os
import random

class Utility:
    def __init__(self, bot):
        self.bot = bot
        self._last_embed = None
        self._rtfm_cache = None
        self._last_google = None
        self._last_result = None

    async def is_owner(ctx):
        return ctx.author.id == 280271578850263040


    @commands.command(name='logout')
    @commands.check(is_owner)
    async def _logout(self, ctx):
        '''
        Shuts down the bot,
        equi to a restart if you are hosting the bot on heroku.
        '''
        await ctx.send('`Logging out....`')
        await self.bot.logout()



    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.check(is_owner)
    async def _eval(self, ctx, *, body: str):
        """eval the python code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
            'source': inspect.getsource
        }

        env.update(globals())

        body = self.cleanup_code(body)
        #await self.edit_to_codeblock(ctx, body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await err.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = ctx.paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                self._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = ctx.paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await out.add_reaction('\u2705') #tick
        if err:
            await err.add_reaction('\u2049') #x


    #async def edit_to_codeblock(self, ctx, body):
        #msg = f'{ctx.prefix}eval\n```py\n{body}\n```'
        #await ctx.message.edit(content=msg)


    def cleanup_code(self, content):
        """removing the code block"""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    def get_parts(self, string):
        '''
        Splits the sections of the embed command
        '''
        for i, char in enumerate(string):
            if char == "{":
                ret = ""
                while char != "}":
                    i += 1
                    char = string[i]
                    ret += char
                yield ret.rstrip('}')

    def parse_field(self, string):
        '''
        Recursive function to get all the key val
        pairs in each section of the parsed embed command
        '''
        ret = {}

        parts = string.split(':')
        key = parts[0].strip().lower()
        val = ':'.join(parts[1:]).strip()

        ret[key] = val

        if '|' in string:
            string = string.split('|')
            for part in string:
                ret.update(self.parse_field(part))
        return ret



    async def to_embed(self, ctx, params):
        '''Actually formats the parsed parameters into an Embed'''
        em = discord.Embed()

        if not params.count('{'):
            if not params.count('}'):
                em.description = params

        for field in self.get_parts(params):
            data = self.parse_field(field)

            color = data.get('color') or data.get('colour')
            if color == 'random':
                em.color = random.randint(0, 0xFFFFFF)
            elif color == 'chosen':
                maybe_col = os.environ.get('COLOR')
                if maybe_col:
                    raw = int(maybe_col.strip('#'), 16)
                    return discord.Color(value=raw)
                else:
                    return await ctx.send('Chosen color is not defined.')

            elif color:
                color = int(color.strip('#'), 16)
                em.color = discord.Color(color)

            if data.get('description'):
                em.description = data['description']

            if data.get('desc'):
                em.description = data['desc']

            if data.get('title'):
                em.title = data['title']

            if data.get('url'):
                em.url = data['url']

            author = data.get('author')
            icon, url = data.get('icon'), data.get('url')

            if author:
                em._author = {'name': author}
                if icon:
                    em._author['icon_url'] = icon
                if url:
                    em._author['url'] = url

            field, value = data.get('field'), data.get('value')
            inline = False if str(data.get('inline')).lower() == 'false' else True
            if field and value:
                em.add_field(name=field, value=value, inline=inline)

            if data.get('thumbnail'):
                em._thumbnail = {'url': data['thumbnail']}

            if data.get('image'):
                em._image = {'url': data['image']}

            if data.get('footer'):
                em._footer = {'text': data.get('footer')}
                if data.get('icon'):
                    em._footer['icon_url'] = data.get('icon')

            if 'timestamp' in data.keys() and len(data.keys()) == 1:
                em.timestamp = ctx.message.created_at

        return em




    @commands.command()
    @commands.check(is_owner)
    async def embed(self, ctx, *, params):
        '''Send complex rich embeds with this command!

        ```
        {description: Discord format supported}
        {title: required | url: optional}
        {author: required | icon: optional | url: optional}
        {image: image_url_here}
        {thumbnail: image_url_here}
        {field: required | value: required}
        {footer: footer_text_here | icon: optional}
        {timestamp} <-this will include a timestamp
        ```
        '''
        em = await self.to_embed(ctx, params)
        #await ctx.message.delete()
        try:
            await ctx.send(embed=em)
            self._last_embed = params
        except:
            await ctx.send('Improperly formatted embed!')



def setup(bot):
    bot.add_cog(Utility(bot))
