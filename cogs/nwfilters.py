import os
import discord
import asyncio
import json
from discord.ext import commands
import myjson


class NightFilter:

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def addword(self, ctx, *, args:str = None):
        '''add word to filter'''
        if ctx.author.guild_permissions.administrator == True:
            url = "{}".format(os.environ.get("cuss_filter"))
            if args == None:
                await ctx.send("`Word not specified!`")
                return
            else:
                data = myjson.get(url)
                data = json.loads(data)
                args = args.lower()
                if "{}".format(args) not in data:
                    data.append(args)
                    url = myjson.store(json.dumps(data),update=url)
                    await ctx.send("`Filter database updated.`")
                else:
                    await ctx.send("`Already added by an admin.`")


    @commands.command()
    async def filtercheck(self, ctx):
        '''check words'''
        if ctx.author.guild_permissions.administrator == True:
            url = "{}".format(os.environ.get("cuss_filter"))
            data = myjson.get(url)
            data = json.loads(data)
            if not data:
                await ctx.send("`Filter base is empty.`")
            else:
                await ctx.send("```"+str(data)+"```")

    @commands.command()
    async def delword(self, ctx, *, args:str = None):
        if ctx.author.guild_permissions.administrator == True:
            url = "{}".format(os.environ.get("cuss_filter"))
            data = myjson.get(url)
            data = json.loads(data)
            if args == None:
                await ctx.send("`no word given.`")
                return
            word = args
            for word in data:
                if word in data:
                    data.remove(word)
                    url = myjson.store(json.dumps(data),update=url)
            await ctx.send("`The word was removed.`")


    async def on_message(self, message):
        '''cuss filter'''
        url = "{}".format(os.environ.get("cuss_filter"))
        texts = myjson.get(url)
        texts = json.loads(texts)
        msgs = message.content.lower()
        if message.author.id == self.bot.user.id:
            return
        if any(word in msgs for word in texts) and message.channel.id == 356157029074862082:
            await message.author.send("Hello!\nYou are not allowed to use words that you used in your last message: `{}`\n**it is against the community rules.**You may want to **censor** cusses if you want to.\n`Doesn't matter how you used it.`".format(message.content))
            await asyncio.sleep(3)
            await message.delete()

def setup(bot):
	bot.add_cog(NightFilter(bot))