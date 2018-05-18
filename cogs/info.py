import discord
from discord.ext import commands

class Trader:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["help"])
    async def about(self,ctx):
        '''help menu'''
        about = """```Made By Neophyte#5556\n\n\nNight Watch: Watching over the server 24/7 (Seriously, Not Stalking XD)\n\n"Hard Coded" to work only in Night Watch Server!```"""
        helpm = "```\n1. n!svrtime: To get the AE servertime.\n2. n!gif [query]: Search gif.\n\nFilter(Admins):\n1. n!filtercheck\n2. n!addword\n3. n!delword\n\nMore coming Later!\n\nPlus, Logging #event-channels 👍 and Stalking the member activities :3```"

        em = discord.Embed(color = 0xffd500)
        em.set_thumbnail(url = self.bot.user.avatar_url)
        em.set_author(name = "About Night∆Watch:", icon_url = "https://image.ibb.co/bZ6yHx/profile.png")
        em.add_field(name = "Info:", value = about, inline = False)
        em.add_field(name = "Help:", value = helpm,inline = False)
        em.set_footer(text = "|NightWatch|",icon_url = self.bot.user.avatar_url)
        await ctx.send(embed = em)




def setup(bot):
    bot.add_cog(Trader(bot))
