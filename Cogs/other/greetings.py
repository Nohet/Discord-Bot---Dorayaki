import discord
from discord.ext import commands

from database import *
from decorators import is_disabled

is_disabled = commands.check(is_disabled)


class GreetingsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        r = guildsett.find_one({"_id": member.guild.id})
        is_enabled = r["join_messages"]
        if is_enabled == "on" or is_enabled == "enable" or is_enabled == "True":
            if r["join_messages_type"] == "embed":
                msg_content = r["join_messages_content"]
                msg_content = msg_content.replace("$member", str(member.name))
                msg_content = msg_content.replace("$mention", str(member.mention))
                msg_content = msg_content.replace("$guild", str(member.guild.name))
                msg_content = msg_content.replace("$count", str(member.guild.member_count))
                msg_content = msg_content.split(" | ")
                channel = self.client.get_channel(r["join_messages_channel"])
                if len(msg_content) == 2:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                    embed.add_field(name=msg_content[0],
                                    value=msg_content[1] + "\n_ _\n _ _ \n _ _")
                    await channel.send(embed=embed)

                elif len(msg_content) == 3:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                    embed.add_field(name=msg_content[0],
                                    value=msg_content[1] + "\n_ _\n _ _ \n _ _")
                    embed.set_footer(text=msg_content[2])
                    await channel.send(embed=embed)

                elif len(msg_content) == 4:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                    embed.add_field(name=msg_content[0],
                                    value=msg_content[1] + "\n_ _\n _ _ \n _ _")
                    embed.set_image(url=msg_content[3])
                    embed.set_footer(text=msg_content[2])
                    await channel.send(embed=embed)

            elif r["join_messages_type"] == "message" or r["join_messages_type"] == "text":
                msg_content = r["join_messages_content"]

                msg_content = msg_content.replace("$member", str(member.name))
                msg_content = msg_content.replace("$mention", str(member.mention))
                msg_content = msg_content.replace("$guild", str(member.guild.name))
                msg_content = msg_content.replace("$count", str(member.guild.member_count))

                channel = self.client.get_channel(["join_messages_channel"])
                channel.send(msg_content)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        r = guildsett.find_one({"_id": member.guild.id})
        is_enabled = r["leave_messages"]
        if is_enabled == "on" or is_enabled == "enable" or is_enabled == "True":
            if r["leave_messages_type"] == "embed":
                msg_content = r["leave_messages_content"]
                msg_content = msg_content.replace("$member", str(member.name))
                msg_content = msg_content.replace("$mention", str(member.mention))
                msg_content = msg_content.replace("$guild", str(member.guild.name))
                msg_content = msg_content.replace("$count", str(member.guild.member_count))
                msg_content = msg_content.split(" | ")
                channel = self.client.get_channel(r["leave_messages_channel"])
                if len(msg_content) == 2:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                    embed.add_field(name=msg_content[0],
                                    value=msg_content[1] + "\n_ _\n _ _ \n _ _")
                    await channel.send(embed=embed)

                elif len(msg_content) == 3:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                    embed.add_field(name=msg_content[0],
                                    value=msg_content[1] + "\n_ _\n _ _ \n _ _")
                    embed.set_footer(text=msg_content[2])
                    await channel.send(embed=embed)

                elif len(msg_content) == 4:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                    embed.add_field(name=msg_content[0],
                                    value=msg_content[1] + "\n_ _\n _ _ \n _ _")
                    embed.set_image(url=msg_content[3])
                    embed.set_footer(text=msg_content[2])
                    await channel.send(embed=embed)

            elif r["leave_messages_type"] == "message" or r["leave_messages_type"] == "text":
                msg_content = r["leave_messages_content"]

                msg_content = msg_content.replace("$member", str(member.name))
                msg_content = msg_content.replace("$mention", str(member.mention))
                msg_content = msg_content.replace("$guild", str(member.guild.name))
                msg_content = msg_content.replace("$count", str(member.guild.member_count))

                channel = self.client.get_channel(["leave_messages_channel"])
                channel.send(msg_content)

    @commands.command(aliases=["setmessagechannel", "setmsgchannel", "smc"])
    @commands.has_permissions(administrator=True)
    async def set_message_channel(self, ctx, value, channel: discord.TextChannel):
        if value == "leave":
            guildsett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"leave_messages_channel": channel.id}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed leave messages channel to {channel.mention}")
            await ctx.send(embed=embed)
        elif value == "join":
            guildsett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"join_messages_channel": channel.id}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed join messages channel to {channel.mention}")
            await ctx.send(embed=embed)

    @commands.command(aliases=["setmessagetext", "setmessagecontent", "setmsgcontent", "setmsgtext"])
    @commands.has_permissions(administrator=True)
    async def set_message_text(self, ctx, value, *, text):
        if value == "leave":
            guildsett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"leave_messages_content": text}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed leave messages text to **{text}**")
            await ctx.send(embed=embed)
        elif value == "join":
            guildsett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"join_messages_content": text}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed join messages text to **{text}**")
            await ctx.send(embed=embed)

    @commands.command(aliases=["setmessagetype", "setmsgtype", "smt"])
    @commands.has_permissions(administrator=True)
    async def set_message_type(self, ctx, value, type):
        if value == "leave":
            guildsett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"leave_messages_type": type}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed leave messages type to {type}")
            await ctx.send(embed=embed)
        elif value == "join":
            guildsett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"join_messages_type": type}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed join messages type to {type}")
            await ctx.send(embed=embed)

    @commands.command()
    async def variables(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Variables", value=f"**$member** - The name of the member who join/leave server "
                                                f"\n**$mention** - Mention the member who join/leave server"
                                                f"\n**$guild** - Name of server"
                                                f"\n**$count** - Server member count")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(GreetingsCog(client))
