import discord
from discord.ext import commands
import random
from datetime import datetime
from discord.ext import menus
import sqlite3

database_file='./db/database.db'


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
            fields.append((number, entry[0]))

        return await self.write_page(menu,fields)



class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_icon='https://cdn.discordapp.com/attachments/804110204110897192/851582958199635998/bob_logo_1.png'


    @commands.group(invoke_without_command=True)
    async def joke(self, ctx):
        embed=discord.Embed(color=discord.Color.blue(),
                            timestamp=datetime.utcnow())
        embed.set_author(name="Available joke commands", icon_url=self.bot_icon)
        embed.add_field(name="Show", value="**.joke show**: Shows a random joke.", inline=True)
        embed.add_field(name="Suggest", value="**.joke suggest [joke]**: Suggests a joke that can later be added to the bot.", inline=False)
        embed.add_field(name="List", value="**.joke list**: Shows a list of the official jokes.", inline=True)
        embed.add_field(name="Pending list", value="**.joke pendinglist**: Shows a list of all the pending jokes.", inline=True)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @joke.command()
    async def show(self, ctx):
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT jokes FROM jokes")
        global jokes
        jokes = cursor.fetchall()
        cursor.close()
        db.close()
        joke_choice = random.choice(jokes)
        
        embed_message = discord.Embed(name='Test Bot', title='Joke', description=str(joke_choice[0]), color=discord.Colour.blue())          
        await ctx.channel.send(embed=embed_message)

    @joke.command()
    async def list(self,ctx):
        
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT * FROM jokes WHERE status=?",('official',))
        global jokes
        jokes = cursor.fetchall()
        cursor.close()
        db.close()

        pages = MyPages(source=MySource(ctx, jokes),clear_reactions_after=True)
        await pages.start(ctx)
 
    @joke.command()
    async def pendinglist(self,ctx):
        
        db=sqlite3.connect(database_file)
        cursor=db.cursor()
        cursor.execute("SELECT * FROM jokes WHERE status=?",('pending',))
        global jokes
        jokes = cursor.fetchall()
        cursor.close()
        db.close()

        pages = MyPages(source=MySource(ctx, jokes),clear_reactions_after=True)
        await pages.start(ctx)   


    @commands.command()
    async def suggest_joke(self, ctx, *,joke):
        if joke != None:
            db=sqlite3.connect(database_file)
            cursor=db.cursor()
            cursor .execute("INSERT INTO jokes(jokes,status) VALUES (?,?)", (str(joke),'pending'))
            db.commit()
            cursor.close()
            db.close()
        else:
            embed=discord.Embed(description=f"You did not provide any joke.",color=discord.Colour.red())
            await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @joke.command()
    async def add(self, ctx, *, joke):
        if joke != None:
            db=sqlite3.connect(database_file)
            cursor=db.cursor()
            cursor.execute("INSERT INTO jokes(jokes,status) VALUES (?,?)", (str(joke),'official'))
            db.commit()
            cursor.close()
            db.close()
        else:
            embed=discord.Embed(description=f"You did not provide any joke.",color=discord.Colour.red())
            await ctx.channel.send(embed=embed)

    @commands.is_owner()
    @joke.command()
    async def remove(self, ctx, number: int):
        if number != None:
            db=sqlite3.connect(database_file)
            cursor=db.cursor()
            cursor.execute("SELECT jokes, ROW_NUMBER() OVER() AS number FROM jokes WHERE status=?",('official',))
            jokes=cursor.fetchall()
            for i in jokes:
                if int(i[1])==number:
                    joke=i[0]
                else:
                    joke=None
                    pass
            if joke is None:
                embed=discord.Embed(description='That number is not on the list! Please provide a valid number.',colour=discord.Colour.red())
                await ctx.channel.send(embed=embed)
            else:
                cursor.execute('DELETE FROM jokes WHERE jokes=?', (str(joke),))
            db.commit()
            cursor.close()
            db.close()
        else:
            embed=discord.Embed(description=f"You did not provide any number.",color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
    
#    @commands.is_owner()
#    @joke.command(name='accept', help='Accepts a joke from the pending list.')
#    async def accept(self, ctx, number: int):
        

#    @commands.is_owner()
#    @joke.command(name='deny', help='Denys a joke from the pending list.')
#    async def deny(self, ctx, number: int):
        

def setup(bot):
    bot.add_cog(Jokes(bot))