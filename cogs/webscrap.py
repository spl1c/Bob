from time import timezone
import discord
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from discord.ext import commands, tasks

    
class WebScrap(commands.Cog, description='Retrieves information from the internet!'):
    def __init__(self, bot):
        self.bot = bot

    time = datetime.time(hour=11, tzinfo=datetime.timezone.utc)

    @tasks.loop(time=time)
    async def retrieve_loop(self):
        
        url = 'https://www.electrosacavem.com/info.php?identif=22444'
        page = urlopen(url)
        html = page.read().decode("ISO-8859-1")
        soup = BeautifulSoup(html, "html.parser")
        modelo = "SONY TV OLED XR65A90JAEP"
        price_line = soup.find_all(color="#CC0000")
        price = price_line[0].text
        img="https://www.electrosacavem.com/images/fotos/f22444foto1.jpg"

        guild = self.bot.get_guild(872127299854680124)
        channel = discord.utils.get(guild.channels, id=872127299854680127)
        nuno=guild.get_member(760089560595562508)

        embed=discord.Embed(
                            color=0xf2f2f2,
                            title=f'Preço: {price}',
                            timestamp=datetime.datetime.utcnow()
                            )
        embed.set_thumbnail(url=img)
        embed.set_footer(icon_url=nuno.avatar, text='Bababooey!')
        embed.set_author(url=url, name=modelo)


        await channel.send(f'Nuno! {nuno.mention}',embed=embed)

    @commands.slash_command(guild_ids=[872127299854680124], name='retrieve')
    async def retrieve(self, ctx):
        if self.retrieve_loop.is_running() == False:
            self.retrieve_loop.start()
            await ctx.respond('Started retrieving!')
        
        elif self.retrieve_loop.is_running() == True:
            self.retrieve_loop.stop()
            await ctx.respond('Stoped retrieving!')


def setup(bot):
    bot.add_cog(WebScrap(bot))