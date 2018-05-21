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

    @commands.command()
    async def resetcounter(self, ctx, *,uids:str = None):
        if ctx.author.guild_permissions.administrator == True:
            url2 = "{}".format(os.environ.get("warn_count"))
            warn = myjson.get(url2)
            warn = json.loads(warn)
            if uids == None:
                await ctx.send("`No member provided`")
                return
            if "{}".format(uids) in warn:
                warn[f"{uids}"]["count"] = 0
                url2 = myjson.store(json.dumps(warn),update=url2)
                await ctx.send("`Warnings reset.`")
            else:
                await ctx.send("`No such id in database`")

    async def on_message(self, message):
        '''cuss filter'''
        url = "{}".format(os.environ.get("cuss_filter"))
        texts = myjson.get(url)
        texts = json.loads(texts)
        url2 = "{}".format(os.environ.get("warn_count"))
        warn = myjson.get(url2)
        warn = json.loads(warn)
        msgs = message.content.lower()
        if message.author.id == self.bot.user.id:
            return
        if any(word in msgs for word in texts) and message.author.guild_permissions.administrator != True:
            #me = message.guild.get_member(user_id = 280271578850263040)
            if "{}".format(message.author.id) not in warn:
                warn[f"{message.author.id}"] = {}
                warn[f"{message.author.id}"]["count"] = 1
                url2 = myjson.store(json.dumps(warn),update=url2)
            else:
                warn[f"{message.author.id}"]["count"] += 1
                url2 = myjson.store(json.dumps(warn),update=url2)
            await message.author.send("Hello!\nYou are not allowed to use words that you used in your last message: `{0}`\n**it is against the community rules.**You m.\n`Doesn't matter how you used it.`\n\nWarning Count: {1}".format(message.content, warn[f"{message.author.id}"]["count"]))
            #await me.send("{0} wrote `{1}`\nCounter: {2}".format(message.author.name, message.content, warn[f"{message.author.id}"]["count"]))
            await asyncio.sleep(3)
            await message.delete()
def setup(bot):
	bot.add_cog(NightFilter(bot))
