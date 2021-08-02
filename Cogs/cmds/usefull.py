import datetime
import sys

import time
import discord
import humanize
import psutil
from dhooks import Webhook
from discord.ext import commands
from googletrans import Translator

from bot import start_time
from structures.database import *

trans = Translator()


class UsefullCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.settings = settings

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
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
        text = humanize.precisedelta(datetime.timedelta(seconds=difference))
        memory = psutil.virtual_memory().used
        memorystr = str(memory)
        pyversion = sys.version
        mongo_db_ping = cluster.settings.command('ping')
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Discord.py version", value=discord.__version__, inline=False)
        embed.add_field(name="Python version", value=pyversion[:5], inline=False)
        embed.add_field(name="Uptime", value=text, inline=False)
        embed.add_field(name="Bot ping", value=f'{round(self.client.latency * 1000)}ms', inline=False)
        embed.add_field(name="MongoDB ping", value=f'{mongo_db_ping["ok"]}ms', inline=False)
        embed.add_field(name="CPU", value=f'{psutil.cpu_percent()}%', inline=False)
        embed.add_field(name="Ram (whole vps)", value=f"{memorystr[:1]}GB ({psutil.virtual_memory().percent}%)",
                        inline=False)
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
    @commands.guild_only()
    async def current_settings(self, ctx):
        req = self.settings.find_one({"_id": ctx.message.guild.id})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name="Current settings")
        embed.add_field(name="Prefix", value=req["prefix"], inline=False)
        embed.add_field(name="Mute role", value=req["muterole"], inline=False)
        embed.add_field(name="Max warns", value=req["maxwarns"], inline=False)
        embed.add_field(name="Currency", value=req["currency"], inline=False)
        embed.add_field(name="Language", value=req["language"], inline=False)
        embed.add_field(name="Monetization", value=req["monetization"], inline=False)
        embed.add_field(name="NSFW", value=req["nsfw"], inline=False)
        embed.add_field(name="Autorole", value=req["autorole"], inline=False)
        embed.add_field(name="Logs", value=req["logs"], inline=False)
        embed.add_field(name="Linkvertise", value=req["linkvertise"], inline=False)
        embed.add_field(name="Join Messages", value=req["join_messages"], inline=False)
        embed.add_field(name="Leave Messages", value=req["leave_messages"], inline=False)
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
        embed.set_footer(text=f"By {ctx.message.author} | {ctx.message.author.id}",
                         icon_url=ctx.message.author.avatar_url)
        await channel.send(embed=embed)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Review", value="Review successfully sent!")
        await ctx.send(embed=embed)

    @commands.command(aliases=["name", "n"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def nick(self, ctx, member: discord.Member, *, new_nick):
        await member.edit(nick=new_nick)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed {member.mention} nick to {new_nick}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["rolemembers"])
    @commands.guild_only()
    async def role_members(self, ctx, role: discord.Role):
        role = discord.utils.get(ctx.guild.roles, name=role.name)
        role_members_list = []
        for member in ctx.guild.members:
            if role in member.roles:
                role_members_list.append(member.display_name + "#" + member.discriminator)

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name=f"Member(s) with certain role ({role.name}) | {len(role_members_list)} member(s)",
                        value=str.join(", ", role_members_list))
        await ctx.send(embed=embed)

    @commands.command(aliases=["sourcecode", "source_code"])
    async def source(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Github - Nohet\n_ _", value="**[Nohet/Discord-Bot---Dorayaki](https://github.com/Nohet/Discord-Bot---Dorayaki)**\n_ _ \nDiscord Bot, that have economy, multi-language, moderation, fun commands, etc. - Nohet/Discord-Bot---Dorayaki")
        embed.set_image(url="https://opengraph.githubassets.com/06d76570c2ceba497a1dad8ad8d6b0356e4b2b436e98dba69f6df118b2adc4f3/Nohet/Discord-Bot---Dorayaki")
        await ctx.send(embed=embed)

    @commands.command(aliases=["bannedusers", "banned_members", "bannedmembers"])
    @commands.guild_only()
    async def banned_users(self, ctx):
        guild_bans = await ctx.guild.bans()
        bans = []
        for ban_entry in guild_bans:
            user = ban_entry.user.name + "#" + ban_entry.user.discriminator
            bans.append(user)
        print(bans)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name=f"Bans in {ctx.guild.name} | {len(bans)} ban(s)",
                        value=str.join(", ", bans))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UsefullCog(client))
