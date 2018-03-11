import os
import json
import discord
import re
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
import aiohttp
import async_timeout
from random import randint

class NightWatch:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['svrtime'])
    async def servertime(self,ctx):
        '''servertime AE'''
        try:
            data = {}
            link = '{}'.format(os.environ.get("timee"))
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'lxml')
            time_data = soup.find("span",{"class": "fontTS"}).get_text()
            date_data = soup.find("span",{"class": "font6"}).get_text()
            time_data = time_data.replace(" ","")
            time_data = time_data.replace("\n","")
            date_data = date_data.replace(" ","")
            date_data = date_data.replace("\n","")
            data["time"] = time_data
            data["date"] = date_data
            #print(data["time"]+"\n"+data["date"])
            em = discord.Embed()
            em.set_thumbnail(url = "http://www.aq3d.com/media/1507/aq3d-full-logo760.png?width=760&height=760")
            em.set_author(name = "AE Server", icon_url = "https://designmodo.com/wp-content/uploads/2015/09/webview.gif")
            em.add_field(name = "Time:", value = data["time"],inline = True)
            em.add_field(name = "Date: ", value = data["date"], inline = True)
            em.colour = discord.Colour.green()
            em.set_footer(text = "|NightWatch| requested by {}".format(ctx.author.name),icon_url = self.bot.user.avatar_url)
            await ctx.send(embed = em)
        except Exception as e:
            print(e)

    @commands.command()
    async def gif(self, ctx, *, args:str = None):
        try:
            if args == None:
                await ctx.send("`Error: You didn't provide any search terms`")
                return
            new_text = args.replace(' ','+')
            link = "http://api.giphy.com/v1/gifs/search?&api_key={}&q={}".format(os.environ.get("gifphy"), new_text)
            random_entry = randint(1, 20)
            em = discord.Embed()
            async def fetch(session, url):
                with async_timeout.timeout(10):
                    async with session.get(url) as response:
                        return await response.json()
            async with aiohttp.ClientSession() as session:
                result = await fetch(session, link)
                #result = await r.json()
                if result["data"]:
                    em.set_image(url = "{}".format(result["data"][random_entry]['images']['fixed_height']['url']))
                    await ctx.send(embed =em)
                else:
                    await ctx.send("`Error: No results Found! `")
        except Exception as e:
            print(e)
            await ctx.send("`Some Internal error, sorry :sweat_smile:`")



    async def on_member_join(self, member):
        '''join for Night Watch'''
        try:
            server = member.guild
            user = member
            channel_id = 356157029074862082 #general of Night Watch server
            channel = self.bot.get_channel(channel_id)
            await channel.send(content = "Welcome {0.mention}, make sure to read <#358368642657812480>".format(user)) #as per alex
        except Exception as e:
            print(e)




def setup(bot):
    bot.add_cog(NightWatch(bot))
