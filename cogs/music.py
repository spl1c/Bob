import discord
from discord.ext import commands

class Music(commands.Cog, description='Listen to music!'):
    def __init__(self, bot):
        self.bot=bot
        self.bot_icon='https://cdn.discordapp.com/attachments/804110204110897192/851582958199635998/bob_logo_1.png'


    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *,song):
        pass


def setup(bot):
    bot.add_cog(Music(bot))