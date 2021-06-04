import discord
import time
from discord.ext import commands
import psutil
from database import *
from dhooks import Webhook
from bot import start_time
import sys


from googletrans import Translator

import datetime

trans = Translator()


class UsefullCog(commands.Cog):
    def __init__(self, client):
        self.client = client

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
    async def create_embed(self, ctx, *, args):
        embed_list = args.split(" | ")
        print(embed_list)
        if len(embed_list) == 2:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name=embed_list[0], value=embed_list[1])
            await ctx.send(embed=embed)
        elif len(embed_list) == 3:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name=embed_list[0], value=embed_list[1])
            embed.set_footer(text=embed_list[2])
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def info(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        memory = psutil.virtual_memory().used
        memorystr = str(memory)
        pyversion = sys.version
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Discord.py version", value=discord.__version__, inline=False)
        embed.add_field(name="Python version", value=pyversion[:5], inline=False)
        embed.add_field(name="Uptime", value=text, inline=False)
        embed.add_field(name="Ping", value=f'{round(self.client.latency * 1000)}ms', inline=False)
        embed.add_field(name="CPU", value=f'{psutil.cpu_percent()}%', inline=False)
        embed.add_field(name="Ram", value=f"{memorystr[:2]}MB ({psutil.virtual_memory().percent}%)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
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
    @commands.guild_only()
    async def settings(self, ctx, arg, arg1):
        if arg == "_id":
            return False
        else:
            try:
                r = guildsett.find_one({"_id": ctx.message.guild.id})
                getitem = r[arg]
                guildsett.update_one({"_id": ctx.message.guild.id}, {"$set": {arg: arg1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Success", value=f"Successfully changed `{arg}` to `{arg1}`")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Error", value=f"That setting is not exist")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def current_settings(self, ctx):
        req = guildsett.find_one({"_id": ctx.message.guild.id})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name="Current settings")
        embed.add_field(name="Prefix", value=req["prefix"])
        embed.add_field(name="Mute role", value=req["muterole"])
        embed.add_field(name="Max warns", value=req["maxwarns"])
        embed.add_field(name="Currency", value=req["currency"])
        embed.add_field(name="Language", value=req["language"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def webhook(self, ctx, url, *message):
        mesg = " ".join(message)
        hook = Webhook(url)
        hook.send(mesg)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully sent webhook!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def translate(self, ctx, lang, *, params):
        content = trans.translate(text=params, dest=lang)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name=f"Translator ({lang})")
        embed.add_field(name="Input:", value=params, inline=False)
        embed.add_field(name="Output:", value=content.text, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def review(self, ctx, *, params):
        channel = self.client.get_channel(847383602408325161)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Review", value=params)
        embed.set_footer(text=f"By {ctx.message.author} | {ctx.message.author.id}", icon_url=ctx.message.author.avatar_url)
        await channel.send(embed=embed)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Review", value="Review successfully sent!")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UsefullCog(client))
