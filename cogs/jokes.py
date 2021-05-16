import discord
from discord.ext import commands
import csv
import random
from datetime import datetime
from discord.ext import menus

jokesfile = './attachments/jokes.csv'

with open(jokesfile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='|', skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
            jokes=[]
            for i in reader:
                jokes.append(i[1])

class MyPages(menus.MenuPages, inherit_buttons=False):

    @menus.button('⏪', position=menus.First(0))
    async def rewind(self, payload: discord.RawReactionActionEvent):
        await self.show_page(0)

    @menus.button('◀️', position=menus.First(1))
    async def back(self, payload: discord.RawReactionActionEvent):
        await self.show_checked_page(self.current_page - 1)
    
    @menus.button('▶️', position=menus.First(2))
    async def forward(self, payload: discord.RawReactionActionEvent):
        await self.show_checked_page(self.current_page + 1)

    @menus.button('⏩',position=menus.First(3))
    async def last(self, payload: discord.RawReactionActionEvent):

        await self.show_page(self._source.get_max_pages() - 1)


class MySource(menus.ListPageSource):
    def __init__(self, ctx, data):
        self.ctx=ctx
        super().__init__(data, per_page=10)

    async def write_page(self,menu, fields=[]):
        len_data = len(self.entries)
        embed=discord.Embed(title=f'Jokes List - Page {menu.current_page+1} of {int(len(jokes)/self.per_page)+1}',
                            colour=discord.Colour.blue(),
                            timestamp=datetime.utcnow())

        for name,value in fields:
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text=f'Requested by {self.ctx.author.name}#{self.ctx.author.discriminator}',icon_url=self.ctx.author.avatar_url)
        return embed

    async def format_page(self, menu, entries):
        fields=[]
        offset=(menu.current_page*self.per_page)
        number=0+offset
        
        for entry in entries:
            number+=1
            fields.append((number, entry))

        return await self.write_page(menu,fields)



class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='joke', help='Returns a random joke from the joke list.')
    async def joke(self, ctx):
        joke_choice = random.choice(jokes)
        
        embed_message = discord.Embed(name='Test Bot', title='Joke', description=str(joke_choice), color=discord.Colour.blue())          
        await ctx.channel.send(embed=embed_message)


    @commands.command(name='addjoke', help='Adds a new joke to the joke list.')
    async def addjoke(self, ctx, *,joke):
        if ctx.author.id == 345928604057731073:
            if joke != None:
                with open(jokesfile,'a',newline='') as csvfile:
                    writer=csv.writer(csvfile, delimiter='|', skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['', joke])
                    csvfile.close
                    embed=discord.Embed(description=f"Joke added successfully.",color=discord.Colour.green())
                    await ctx.channel.send(embed=embed)
            else:
                embed=discord.Embed(description=f"You did not provide any joke.",color=discord.Colour.red())
                await ctx.channel.send(embed=embed)  
        else:
            embed=discord.Embed(description=f"You do not have permission to execute such operation.",color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
    


    @commands.command(name='jokelist',help='Returns a list with all the jokes.')
    async def jokelist(self,ctx):
        
        pages = MyPages(source=MySource(ctx, list(jokes)),clear_reactions_after=True)
        await pages.start(ctx)



def setup(bot):
    bot.add_cog(Jokes(bot))