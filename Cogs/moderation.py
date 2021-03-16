import discord
from discord.ext import commands
from database import *


class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded moderation.py")

    @commands.command()
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        getmuterole = guildsett.find_one({"_id": ctx.message.guild.id})
        rolemute = getmuterole["muteRole"]
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
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        reqmaxwarns = guildsett.find_one({"_id": ctx.message.guild.id})
        maxwarns = reqmaxwarns["maxwarns"]
        try:
            warndatauser = {"_id": ctx.message.guild.id + member.id, "warns": 0}
            warnsdata.insert_one(warndatauser)

        except:
            reqfindwarns = warnsdata.find_one({"_id": ctx.message.guild.id + ctx.message.author.id})
            findwarns = reqfindwarns["warns"]
            warnsdata.update_one({"_id": ctx.message.guild.id + member.id},
                                 {"$set": {"warns": findwarns + 1}})

        reqbanwarns = warnsdata.find_one({"_id": ctx.message.guild.id + member.id})
        banwarns = reqbanwarns["warns"]
        print(banwarns, maxwarns)

        if banwarns == maxwarns:
            warnsdata.update_one({"_id": ctx.message.guild.id + member.id}, {"$set": {"warns": 0}})
            await member.ban(reason=reason)
            await ctx.send("Zbanowano użytkownika ponieważ miał za dużo warnów!")

        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Warn")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/Q87XzlKSuHqnT2FEHE/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def checkwarns(self, ctx, member: discord.Member):
        req = warnsdata.find_one({"_id": ctx.message.guild.id + member.id})
        checkwarns = req["warns"]
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Check warns", value=f"{member} has {checkwarns} warn(s)")
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(ModerationCog(client))
