import discord
from discord.ext import commands

class Trader:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self,ctx):
        '''help menu'''
        await ctx.send("""```
Help Menu:

1.n!svrtime: To get the AE servertime.
2.n!gif: To get gif based on a search (Not accurate)

More commands and stuff will be added later.
        ```""")





def setup(bot):
    bot.add_cog(Trader(bot))
