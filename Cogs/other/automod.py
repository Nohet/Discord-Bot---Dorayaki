import datetime

import discord
from discord.ext import commands

from database import *

now = datetime.datetime.now()


class AutoModCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        r = guildsett.find_one({"_id": message.guild.id})
        is_enabled = r["logs"]
        if is_enabled == "on" or is_enabled == "enable" or is_enabled == "True":
            channel = self.client.get_channel(r["logsChannel"])
            embed = discord.Embed(
                colour=discorda.Color.from_rgb(244, 182, 89)
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        r = guildsett.find_one({"_id": member.guild.id})
        is_enabled = r["autorole"]
        if is_enabled == "on" or is_enabled == "enable" or is_enabled == "True":
            role = discord.utils.get(member.guild.roles, name=r["autoroleRole"])
            await member.add_roles(role, reason="Autorole")

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

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        guildsett.update_one({"_id": ctx.message.guild.id},
                             {"$set": {"autoroleRole": role.name}})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed autorole role to {role.mention}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(AutoModCog(client))
