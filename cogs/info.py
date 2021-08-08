from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands.errors import MemberNotFound


class Info(commands.Cog, description='Stuff that will display information.'):
    def __init__(self, bot):
        self.bot=bot
        self.link='https://discord.com/api/oauth2/authorize?client_id=782232275558465557&permissions=2117463287&scope=bot'
        self.logo='https://cdn.discordapp.com/avatars/782232275558465557/42e7455f136d4f8945a2fe82967f1add.webp?size=2048'
    
    

    @commands.command(name='info', help='Show information about Bob.')
    async def info(self, ctx):
        owner=(await self.bot.application_info()).owner
        embed=discord.Embed(description=f'Bob was created by Gonçalo Francisco.\nThe discord bot was created by {owner.mention} (spl1ce#5225).',colour=0xf2f2f2,timestamp=datetime.utcnow())
        embed.set_author(name='Bob.',icon_url=self.logo)
        embed.set_thumbnail(url=self.logo)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}')
        embed.add_field(name='Servers',value=len(self.bot.guilds))
        embed.add_field(name='Users',value=len(self.bot.users))
        embed.add_field(name='Invite',value=f'[Invite]({self.link})')
        await ctx.channel.send(embed=embed)



    @commands.command(name='invite', help='Sends a link to invite Bob to your own server.')
    async def invite(self, ctx):
        embed=discord.Embed(title='Click here!',url=self.link,colour=0xf2f2f2)
        await ctx.channel.send(embed=embed)
    


    @commands.command(name='serverinfo', help='Returns information about a guild/server.')
    async def serverinfo(self, ctx):
        guild=ctx.message.guild
        icon=guild.icon_url
        name=guild.name
        id=guild.id
        created_at=guild.created_at
        members=guild.members
        member_count=guild.member_count
        bot_count=0
        role_count=len(guild.roles)
        owner=guild.owner
        text_channels=len(guild.text_channels)
        voice_cbannels=len(guild.voice_channels)
        stage_channels=len(guild.stage_channels)
        emoji_count=len(guild.emojis)
        region=guild.region
        invites=await guild.invites()

        for member in members:
            if member.bot==True:
                bot_count+=1

        embed=discord.Embed(description=f'**Description:** {guild.description}',color=discord.Colour.light_gray(),
                            timestamp=datetime.utcnow())
        embed.set_thumbnail(url=icon)
        embed.set_author(name=name, icon_url=icon, url=icon)
        embed.add_field(name='ID',value=id,inline=False)
        embed.add_field(name='Owner',value=f'{owner.mention}\n{owner.name}#{owner.discriminator} (`{owner.id}`)',inline=True)
        embed.add_field(name='Created at',value=created_at.strftime(f'%m/%d/%Y | %H:%M:%S UTC'),inline=True)
        embed.add_field(name='Channels',value=f'Text channels: {text_channels}\nVoice channels: {voice_cbannels}\nStage channels: {stage_channels}',inline=False)
        embed.add_field(name='Members',value=member_count,inline=True)
        embed.add_field(name='Bots',value=bot_count,inline=True)
        embed.add_field(name='Roles',value=role_count,inline=True)
        embed.add_field(name='Region',value=region,inline=True)
        embed.add_field(name='Emojis', value=emoji_count,inline=True)
        if len(invites)!=0:
            embed.add_field(name='Invite link', value=invites[0].url,inline=True)

        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)



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
        if isinstance(error, MemberNotFound):
            await ctx.channel.send(embed=discord.Embed(description='User not found!', colour=discord.Colour.red()))

    

    @commands.command(name='avatar', help='Shows the avatar of a user.',aliases=['av','pfp'])
    async def avatar(self, ctx, member=None):
        converter = MemberConverter()
        if member != None:
            user= await converter.convert(ctx,member)
        else:
            user=ctx.author
        embed=discord.Embed(colour=0xf2f2f2,
                            timestamp=datetime.utcnow())
        embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        embed.set_image(url=user.avatar_url_as(size=2048))

        await ctx.channel.send(embed=embed)

    @avatar.error
    async def avatar_error(self,ctx,error):
        if isinstance(error, MemberNotFound):
            embed=discord.Embed(description='Member not found!',colour=discord.Colour.red())
            await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Info(bot))