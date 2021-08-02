import discord
from discord.ext import commands

from structures.database import *
from structures.decorators import is_registered


class SettingsCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sett = settings

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        try:
            r = self.sett.find_one({"_id": ctx.guild.id})
            prefix = r["prefix"]
            settings_status = "Settings are available, and can be changed!"
        except Exception as e:
            print(e)
            prefix = ">"
            settings_status = """Settings are not available for this server (Server not added to database)
                                 Try readding the bot, if this not help, contact developer: Nohet#2453 (501072487258390539)"""

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Settings", value="In settings you can change settings for this server.", inline=False)
        embed.add_field(name="Settings status", value=settings_status)
        embed.add_field(name="Available settings", value=f"""{prefix}settings links_information 
                                                             {prefix}settings monetization
                                                             {prefix}settings prefix
                                                             {prefix}settings muterole 
                                                             {prefix}settings maxwarns
                                                             {prefix}settings currency
                                                             {prefix}settings autorole 
                                                             {prefix}settings leave_messages
                                                             {prefix}settings join_messages
                                                             {prefix}settings logs
                                                             {prefix}settings language""",
                        inline=False)
        await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def links_information(self, ctx, arg):
        available_options = ["on", "enable", "True", "off", "disable", "False"]
        if arg in available_options:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"links_information": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``links_information`` to **{arg}**")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"""This option does not exists!
                                                    Available options: ``{str.join(", ", available_options)}``""")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def monetization(self, ctx, arg):
        available_options = ["on", "enable", "True", "off", "disable", "False"]
        if arg in available_options:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"monetization": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``monetization`` to **{arg}**")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"""This option does not exists!
                                                    Available options: ``{str.join(", ", available_options)}``""")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, arg):
        if len(arg) >= 5:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"The maximum prefix length has been exceeded!")
            await ctx.send(embed=embed)
        else:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"prefix": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``prefix`` to **{arg}**")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def muterole(self, ctx, role: discord.Role):
        self.sett.update_one({"_id": ctx.message.guild.id},
                             {"$set": {"muterole": role.name}})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed ``muterole`` to {role.mention}")
        await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def maxwarns(self, ctx, arg: int):
        self.sett.update_one({"_id": ctx.message.guild.id},
                             {"$set": {"maxwarns": arg}})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed ``maxwarns`` to **{arg}**")
        await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def currency(self, ctx, arg: int):
        self.sett.update_one({"_id": ctx.message.guild.id},
                             {"$set": {"currency": arg}})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed ``currency`` to **{arg}**")
        await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, arg):
        available_options = ["on", "enable", "True", "off", "disable", "False"]
        if arg in available_options:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"autorole": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``autorole`` to **{arg}**")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"""This option does not exists!
                                                    Available options: ``{str.join(", ", available_options)}``""")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def leave_messages(self, ctx, arg):
        available_options = ["on", "enable", "True", "off", "disable", "False"]
        if arg in available_options:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"leave_messages": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``leave_messages`` to **{arg}**")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"""This option does not exists!
                                                    Available options: ``{str.join(", ", available_options)}``""")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def join_messages(self, ctx, arg):
        available_options = ["on", "enable", "True", "off", "disable", "False"]
        if arg in available_options:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"join_messages": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``join_messages`` to **{arg}**")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"""This option does not exists!
                                                    Available options: ``{str.join(", ", available_options)}``""")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def logs(self, ctx, arg):
        available_options = ["on", "enable", "True", "off", "disable", "False"]
        if arg in available_options:
            self.sett.update_one({"_id": ctx.message.guild.id},
                                 {"$set": {"logs": arg}})
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully changed ``logs`` to **{arg}**")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value=f"""This option does not exists!
                                                    Available options: ``{str.join(", ", available_options)}``""")
            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def language(self, ctx, arg: int):
        self.sett.update_one({"_id": ctx.message.guild.id},
                             {"$set": {"language": arg}})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully changed ``language`` to **{arg}**")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(SettingsCog(client))
