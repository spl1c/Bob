import discord
from discord.ext.commands import MemberConverter
from discord.ext import commands
from datetime import datetime


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    

    @commands.command(name='userinfo', help='Returns information about a user.')
    async def userinfo(self, ctx, member=None):

        #Convert the member argument to a discord.Member object
        converter = MemberConverter()
        if member != None:
            user= await converter.convert(ctx,member)
        else:
            user=ctx.author
        embed = discord.Embed(description=user.mention,
                              color=user.colour or discord.Colour.light_grey,
                              timestamp=datetime.utcnow()
                              )

        #Useful stuff        
        permissions = [permission[0] for permission in user.permissions_in(ctx.channel) if permission[1] == True]
        roles=[role for role in user.roles]


        #Embed message

        embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        embed.add_field(name='ID', value=user.id, inline=False)
        embed.add_field(name='Registered', value=user.created_at.strftime(f'%m/%d/%Y | %H:%M:%S UTC'),inline=True)
        embed.add_field(name='Joined', value=user.joined_at.strftime(f'%m/%d/%Y | %H:%M:%S UTC'),inline=True)
        if len(roles) >= 2:
            embed.add_field(name='Roles',value=' '.join([role.mention for role in roles[1:]]),inline=False)
        elif len(roles) == 1:
            embed.add_field(name='Roles',value='No Roles',inline=False)
        if len(permissions) != 0:
            embed.add_field(name='Permissions', value=', '.join([str(permission).replace('_',' ').title() for permission in permissions]),inline=False)

        #Add presence to embed message
        if str(user.raw_status) == 'offline':
            embed.add_field(name='Presence',value=f'<:offline:804123785795338300>  Offline', inline=True)
        elif str(user.raw_status) == 'online':
            embed.add_field(name='Presence',value=f'<:online:804123619399172147>  Online', inline=True)
        elif str(user.raw_status) == 'dnd':
            embed.add_field(name='Presence',value=f'<:dnd:804124142957887508>  Do not disturb', inline=True)
        elif str(user.raw_status) == 'idle':
            embed.add_field(name='Presence',value=f'<:idle:804125064643346452>  Idle', inline=True)

        #check if activities are not empty
        if len(user.activities) != 0:
            #Get user status
            status = discord.utils.get(user.activities, type=discord.ActivityType.custom)
            
            #Get the user activity
            activity_playing = discord.utils.get(user.activities, type=discord.ActivityType.playing)
            activity_listening = discord.utils.get(user.activities, type=discord.ActivityType.listening)
            activity_streaming = discord.utils.get(user.activities, type=discord.ActivityType.streaming)
            activity_watching = discord.utils.get(user.activities, type=discord.ActivityType.watching)
            activity_competing = discord.utils.get(user.activities, type=discord.ActivityType.competing)

            #Add status to the embed message
            if status is not None:
            
                embed.add_field(name='Status',value=f'{status}', inline=True)
            
            #Check and add the activity of the user to the embed message
            if activity_playing is not None:
                user_activity = '🎮 Playing '
                activity_name = activity_playing.name
                embed.add_field(name='Activity',value=f'{user_activity} {activity_name}', inline=True)
            elif activity_listening is not None:
                user_activity = '🎧 Listening to '
                activity_name = activity_listening.name
                embed.add_field(name='Activity',value=f'{user_activity} {activity_name}', inline=True)
            elif activity_watching is not None:
                user_activity = '🍿 Watching  '
                activity_name = activity_watching.name
                embed.add_field(name='Activity',value=f'{user_activity} {activity_name}', inline=True)
            elif activity_streaming is not None:
                user_activity = '<:streaming:804134619644952615> Streaming '
                activity_name = activity_streaming.name
                embed.add_field(name='Activity',value=f'{user_activity} {activity_name}', inline=True)
            elif activity_competing is not None:
                user_activity = '🏆 Competing in '
                activity_name = activity_competing.name
                embed.add_field(name='Activity',value=f'{user_activity} {activity_name}', inline=True)

        await ctx.channel.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=discord.Embed(description='User not found!', colour=discord.Colour.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(embed=discord.Embed(description='I do not have permission to do that! Make sure to ask the server administrator to give me permissions.', colour=discord.Colour.red()))
        else:
            print(error)
            await ctx.channel.send(embed=discord.Embed(description=error, colour=discord.Colour.red()))


def setup(bot):
    bot.add_cog(Userinfo(bot))