import math
import discord
from discord.ext import commands
from discord.ext import pages
from discord.ext.commands import Group
from datetime import datetime


class MyHelp(commands.HelpCommand):
    

    def get_pages(self, entry, embed_title, embed_description, embed_inline, author, limit):
        
        totalpages=math.ceil(len(entry)/limit)
        
        pages=[]

        for i in range(totalpages):
            offset=(i*limit)
            number=0+offset
    
            embed=discord.Embed(title=embed_title,
                description=embed_description,
                colour=0xf2f2f2,
                timestamp=datetime.utcnow())

            embed.set_footer(text=f"Only {author.name}#{author.discriminator} can control the buttons!",icon_url=author.avatar)
            
            fields=[(f"{i[0]}", i[1]) for i in entry if entry.index(i) >= number and entry.index(i) < number+limit]
            for name,value in fields:
                embed.add_field(name=name, value=value, inline=embed_inline)
            pages.append(embed)

        
        return pages

    def get_clean_command_signature(self, command):

        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        prefix=self.context.clean_prefix

        description=f"*Hi, I'm Bob and I'm here to help you!*\n\n**Do you need help with a command?**\nType `{prefix}help [command]`.\n\n**Do you need help with a category?**\nType `{prefix}help [category]`.\n\n**__CATEGORIES__**"

        coglist=[]
        cogs = dict(self.context.bot.cogs)
        del cogs['WebScrap']
        for k, v in cogs.items():
            coglist.append([k, cogs[k].description])


        paginator = pages.Paginator(pages=self.get_pages(coglist, embed_title='Help', embed_description=description, embed_inline=True, author=self.context.author, limit=6), use_default_buttons=False)
        paginator.add_button(pages.PaginatorButton("prev", label="←", style=discord.ButtonStyle.green))
        paginator.add_button(pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True))
        paginator.add_button(pages.PaginatorButton("next", label="→", style=discord.ButtonStyle.green))
        await paginator.send(self.context)


    async def send_cog_help(self, cog):
        commandlist=[]
        filtered_commands=await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered_commands:
            signature=self.get_clean_command_signature(command)
            commandlist.append([str(signature), str(command.help)])


        paginator = pages.Paginator(pages=self.get_pages(commandlist, embed_title=cog.qualified_name, embed_description='', embed_inline=False, author=self.context.author, limit=10), use_default_buttons=False)
        paginator.add_button(pages.PaginatorButton("prev", label="←", style=discord.ButtonStyle.green))
        paginator.add_button(pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True))
        paginator.add_button(pages.PaginatorButton("next", label="→", style=discord.ButtonStyle.green))
        await paginator.send(self.context)


    async def send_group_help(self, group):
        commandlist=[]
        filtered_commands=await self.filter_commands(group.commands, sort=True)
        for command in filtered_commands:
            commandlist.append([str(self.get_clean_command_signature(command)),str(command.help)])

        paginator = pages.Paginator(pages=self.get_pages(commandlist, embed_title=group.qualified_name, embed_description='*This is a group of commands*', embed_inline=False, author=self.context.author, limit=10), use_default_buttons=False)
        paginator.add_button(pages.PaginatorButton("prev", label="←", style=discord.ButtonStyle.green))
        paginator.add_button(pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True))
        paginator.add_button(pages.PaginatorButton("next", label="→", style=discord.ButtonStyle.green))
        await paginator.send(self.context)
    

    async def send_command_help(self, command):
        embed=discord.Embed(title=self.get_command_signature(command), description=command.help, colour=0xf2f2f2)
        
        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def command_not_found(self, string):
        embed = discord.Embed(description=f'No command called "{string}" found.', colour=discord.Colour.red())
        await self.context.send(embed=embed)

    async def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            embed = discord.Embed(description=f'Command "{command.qualified_name}" has no subcommand named {string}', colour=discord.Colour.red())
        else:
            embed = discord.Embed(description=f'Command "{command.qualified_name}" has no subcommand', colour=discord.Colour.red())

        await self.context.send(embed=embed)

# The cog.
class Help(commands.Cog, description='If you need help, this is the category for you!'):
    def __init__(self, bot):
       self.bot = bot
       help_command = MyHelp()
       help_command.cog = self
       bot.help_command = help_command


def setup(bot):
    bot.add_cog(Help(bot))