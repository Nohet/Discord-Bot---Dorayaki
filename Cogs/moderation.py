import discord
from discord.ext import commands
from database import *
import asyncio

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded moderation.py")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            await member.ban(reason=reason)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Ban")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
            await ctx.send(embed=embed)
        elif language == ("pl"):
            await member.ban(reason=reason)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Ban")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            await member.kick(reason=reason)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Kick")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)
        elif language == ("pl"):
            await member.kick(reason=reason)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Kick")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        getmuterole = guildsett.find_one({"_id": ctx.message.guild.id})
        rolemute = getmuterole["muterole"]
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if member == ctx.message.author and language == ("en"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value="You can't mute yourself!")
            return False
        if member == ctx.message.author and language == ("pl"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Błąd", value="Nie możesz siebie wyciszyć!")
            return False

        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name=rolemute)

        if not muteRole:
            muteRole = await guild.create_role(name=rolemute)

            for channel in guild.channels:
                await channel.set_permissions(muteRole, speak=False, send_messages=False)

        await member.add_roles(muteRole, reason=reason)
        if language == ("en"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Mute")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)
        elif language == ("pl"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Mute")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        reqmaxwarns = guildsett.find_one({"_id": ctx.message.guild.id})
        maxwarns = reqmaxwarns["maxwarns"]
        try:
            warndatauser = {"_id": ctx.message.guild.id + member.id, "warns": 0}
            warnsdata.insert_one(warndatauser)

        except:
            reqfindwarns = warnsdata.find_one({"_id": ctx.message.guild.id + ctx.message.author.id})
            findwarns = reqfindwarns["warns"]
            findwarnstr = str(findwarns)
            warnsdata.update_one({"_id": ctx.message.guild.id + member.id},
                                 {"$set": {"warns": findwarns + 1}})
            reqwarnsreason = warnsdata.find_one({"_id": ctx.message.guild.id + ctx.message.author.id})
            warnreason = reqwarnsreason["warns"]
            warnreasonstr = str(warnreason)
            warnsdata.update_one({"_id": ctx.message.guild.id + member.id},
                                 {"$set": {"warn" + warnreasonstr: reason}})

        reqbanwarns = warnsdata.find_one({"_id": ctx.message.guild.id + member.id})
        banwarns = reqbanwarns["warns"]
        print(banwarns, maxwarns)

        if banwarns == maxwarns:
            warnsdata.update_one({"_id": ctx.message.guild.id + member.id}, {"$set": {"warns": 0}})
            await member.ban(reason=reason)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Ban", value=f"{member} has been banned because of maximum warns!")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Warn")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/833zGXxokmCmCDRkUd/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def checkwarns(self, ctx, arg, member: discord.Member=None):
        if not member:
            member = ctx.message.author
        argint = str(arg)
        reqgetwarnreason = warnsdata.find_one({"_id": ctx.message.guild.id + member.id})
        getwarnreason = reqgetwarnreason["warn" + argint]
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Warn " + argint, value=f"Reason: {getwarnreason}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def allwarns(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.message.author
        reqgetwarnreason = warnsdata.find_one({"_id": ctx.message.guild.id + member.id})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Warns", value=f"{member} | {reqgetwarnreason['warns']} warn(s)")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, time: int):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        await ctx.channel.edit(slowmode_delay=time)
        if language == ("en"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully set slow mode to {time}s")
            await ctx.send(embed=embed)
        elif language == ("pl"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Sukces", value=f"Pomyślnie ustawiono slowmode na {time}s")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def tempmute(self, ctx, member: discord.Member, time, *, reason):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        getmuterole = guildsett.find_one({"_id": ctx.message.guild.id})
        rolemute = getmuterole["muterole"]
        sleeptime = convert(time)
        if language == ("en"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="TempMute")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason:", value=reason)
            embed.add_field(name="Time:", value=time)
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)
        elif language == ("pl"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="TempMute")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.add_field(name="Czas:", value=time)
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)
        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name=rolemute)

        if not muteRole:
            muteRole = await guild.create_role(name=rolemute)

            for channel in guild.channels:
                await channel.set_permissions(muteRole, speak=False, send_messages=False)

        await member.add_roles(muteRole, reason=reason)
        await asyncio.sleep(sleeptime)
        await member.remove_roles(muteRole, reason="Automatic unmute")
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Unmute", value=f"{member} has been automatically unmuted!")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ModerationCog(client))
