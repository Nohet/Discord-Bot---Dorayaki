import discord, datetime, time
from discord.ext import commands
import psutil
from database import *
from dhooks import Webhook
from bot import start_time
import sys


from googletrans import Translator

import datetime

now = datetime.datetime.now()


class UsefullCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded usefull.py")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        r = guildsett.find_one({"_id": message.guild.id})
        is_enabled = r["logs"]
        if is_enabled == "on" or is_enabled == "enable" or is_enabled == "True":
            channel = self.client.get_channel(r["logsChannel"])
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name=f"Message Deleted | {now.strftime('%Y-%m-%d %H:%M:%S')}")
            embed.add_field(name="Message Content", value=f"```{message.content}```", inline=False)
            embed.add_field(name="Message Info",
                            value=f"Message Author: **{message.author} | {message.author.id}** \nMessage Length: **{len(message.content)}**\nMessage Timestamp: **{message.created_at}**\nMessage Guild: **{message.guild} | {message.guild.id}**\nMessage ID: **{message.id}**",
                            inline=False)
            embed.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
            await channel.send(embed=embed)

        else:
            return False

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        r = guildsett.find_one({"_id": before.guild.id})
        is_enabled = r["logs"]
        if is_enabled == "on" or is_enabled == "enable" or is_enabled == "True":
            channel = self.client.get_channel(r["logsChannel"])
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name=f"Message Edited | {now.strftime('%Y-%m-%d %H:%M:%S')}")
            embed.add_field(name="Before", value=f"```{before.content}```", inline=False)
            embed.add_field(name="After", value=f"```{after.content}```", inline=False)
            embed.add_field(name="Message Info",
                            value=f"Message Author: **{before.author} | {before.author.id}** \nMessage Length: **{len(before.content)} | {len(after.content)}**\nMessage Timestamp: **{after.created_at}**\nMessage Guild: **{before.guild} | {before.guild.id}**\nMessage ID: **{before.id}**",
                            inline=False)
            embed.set_footer(text=f"{before.author} | {before.author.id}", icon_url=before.author.avatar_url)
            await channel.send(embed=embed)

        else:
            return False



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
        embed_list = args.split("|")
        if not embed_list[2]:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name=embed_list[0], value=embed_list[1])
            await ctx.send(embed=embed)
        elif embed_list[2]:
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

    @commands.command(aliases=["whois"])
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
        mesg = (" ").join(message)
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
        trans = Translator()
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
    @commands.has_permissions(administrator=True)
    async def logs(self, ctx, channel: discord.TextChannel):
        guildsett.update_one({"_id": ctx.message.guild.id},
                             {"$set": {"logsChannel": channel.id}})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed logs channel to {channel.mention}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UsefullCog(client))
