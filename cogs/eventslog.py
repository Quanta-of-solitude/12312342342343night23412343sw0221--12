'''
Simple Event Logs for Night Watch
by: Neophyte#5556
'''
import discord
import asyncio
from discord.ext import commands

class EventLog:

    def __init__(self, bot):
        self.bot = bot

    async def on_message_delete(self, message):
        '''Message delete event'''
        msg = message.content
        author = message.author
        em = discord.Embed(color = 0xffd500)
        if author.id == self.bot.user.id or author.bot == True:
            return
        if message.attachments:
            links = []
            for x in message.attachments:
                links.append(x.url)
            linkss = '\n'.join(links)
            data = "```Message Deleted! <Attachments Detected>"
            data += f"\nAuthor: {message.author}\nID: {author.id}\n"
            data += f"Message ID: {message.id}\n"
            data += f"Channel:\nName: {message.channel.name}\nID: {message.channel.id}\n\n"
            data += f"Content:```\n {msg}\n{linkss}"
            channel_id = 424195382172450817   #424195382172450817
            channel = self.bot.get_channel(channel_id)
            await channel.send(data)
        else:
            em.set_author(name = "Message Deleted! <Text Type>", icon_url = "https://image.ibb.co/bZ6yHx/profile.png")
            em.add_field(name = "Author: ", value = str(message.author) + f"\nID: {author.id}",inline = False)
            em.add_field(name = "Message ID:", value = message.id, inline = False)
            em.add_field(name = "Channel:", value = f"Name: {message.channel.name}" + f"\nID: {message.channel.id}", inline = False)
            em.add_field(name = "Content: ", value = "```"+msg+"```", inline = False)
            em.set_thumbnail(url = author.avatar_url)
            em.set_footer(text = "|NightWatch|",icon_url = self.bot.user.avatar_url)
            channel_id = 424195382172450817 #424195382172450817
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed = em)

    async def on_message_edit(self, before, after):
        '''Message EDIT EVENT'''
        author = before.author = after.author
        if author.id == self.bot.user.id or author.bot == True:
            return
        msg_before = before.content
        msg_after = after.content
        em =discord.Embed(color = 0xffd500)
        em.set_author(name = "Message Edited!", icon_url = "https://image.ibb.co/bZ6yHx/profile.png")
        em.add_field(name = "Author:", value = str(author) + f"\nID: {author.id}" ,inline = False)
        em.add_field(name = "Channel:", value = f"Name: {before.channel.name}\nID: {before.channel.id}", inline = False)
        em.add_field(name = "Original Message:", value = "```"+msg_before+"```", inline = False)
        em.add_field(name = "New Message:", value = "```"+msg_after+"```", inline = False)
        em.set_thumbnail(url = author.avatar_url)
        em.set_footer(text = "|NightWatch|",icon_url = self.bot.user.avatar_url)
        channel_id = 424195442314575882   #424195442314575882
        channel = self.bot.get_channel(channel_id)
        await channel.send(embed = em)

    async def on_member_update(self, before, after):
        '''Member Nick Name update'''
        if before.nick != after.nick:
            em =discord.Embed(color = 0xffd500)
            em.set_author(name = "Nick Name Update!", icon_url = "https://image.ibb.co/bZ6yHx/profile.png")
            em.add_field(name = "User:", value = f"Name: {before.name}\nID: {before.id}", inline = False)
            em.add_field(name = "Old NickName: ", value = f"```{before.nick}```", inline = False)
            em.add_field(name = "New NickName:", value = f"```{after.nick}```", inline = False)
            em.set_thumbnail(url = before.avatar_url)
            em.set_footer(text = "|NightWatch|",icon_url = self.bot.user.avatar_url)
            channel_id = 424200050860752907   #424200050860752907
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed = em)

def setup(bot):
    bot.add_cog(EventLog(bot))
