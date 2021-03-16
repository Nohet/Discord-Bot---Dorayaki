import discord
from discord.ext import commands
import psutil
from database import *

class UsefullCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded usefull.py")

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.message.author
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name=f"{member}", value=f"[[Download]]({member.avatar_url})")
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def say(self, ctx, *args):
        mesg = ' '.join(args)
        await ctx.send(mesg)

    @commands.command()
    @commands.guild_only()
    async def say_embed(self, ctx, *args):
        mesg = ' '.join(args)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name=ctx.message.guild.name, value=f"{mesg}")
        embed.set_footer(text=f"By {ctx.message.author}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def info(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Ping", value=f'{round(self.client.latency * 1000)}ms', inline=False)
        embed.add_field(name="CPU", value=f'{psutil.cpu_percent()}%', inline=False)
        embed.add_field(name="Ram", value=f"{psutil.virtual_memory().percent}%")
        await ctx.send(embed=embed)

    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Color.from_rgb(244, 182, 89), timestamp=ctx.message.created_at,
                              title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        embed.add_field(name="On mobile?", value=member.is_on_mobile())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, arg=None, arg1=None):

        if arg == ("muterole"):
            guildsett.update_one({"_id": ctx.message.guild.id}, {"$set":{"muteRole": arg1}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed mute role to `{arg1}`")
            await ctx.send(embed=embed)

        elif arg == ("prefix"):
            guildsett.update_one({"_id": ctx.message.guild.id}, {"$set":{"prefix": arg1}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed prefix to `{arg1}`")
            await ctx.send(embed=embed)

        elif arg == ("maxwarns"):
            guildsett.update_one({"_id": ctx.message.guild.id}, {"$set":{"maxwarns": arg1}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed maxwarns to `{arg1}`")
            await ctx.send(embed=embed)

        elif arg == ("language"):
            guildsett.update_one({"_id": ctx.message.guild.id}, {"$set":{"language": arg1}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed language to `{arg1}`")
            await ctx.send(embed=embed)

        elif arg == ("currency"):
            guildsett.update_one({"_id": ctx.message.guild.id}, {"$set":{"currency": arg1}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed currency to `{arg1}`")
            await ctx.send(embed=embed)

    @commands.command()
    async def current_settings(self, ctx):
        req = guildsett.find_one({"_id": ctx.message.guild.id})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name="Current settings")
        embed.add_field(name="Prefix", value=req["prefix"])
        embed.add_field(name="Mute role", value=req["muteRole"])
        embed.add_field(name="Max warns", value=req["maxwarns"])
        embed.add_field(name="Currency", value=req["currency"])
        embed.add_field(name="Language", value=req["language"])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UsefullCog(client))