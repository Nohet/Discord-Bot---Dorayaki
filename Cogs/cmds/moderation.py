import asyncio
import random

import discord
from discord.ext import commands

from structures.decorators import convert
from structures.database import settings, warns


class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.settings = settings
        self.warns = warns

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == "en":
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
        elif language == "pl":
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
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == "en":
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
        elif language == "pl":
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
        r = self.settings.find_one({"_id": ctx.message.guild.id})
        rolemute = r["muterole"]
        language = r["language"]
        if member == ctx.message.author and language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value="You can't mute yourself!")
            return False
        if member == ctx.message.author and language == "pl":
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
        if language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="Mute")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "pl":
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
        reqmaxwarns = self.settings.find_one({"_id": ctx.message.guild.id})
        maxwarns = reqmaxwarns["maxwarns"]
        try:
            warndatauser = {"_id": ctx.message.guild.id + member.id, "warns": 0}
            self.warns.insert_one(warndatauser)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Account created",
                            value=f"Successfully created account for {member}, use command again!")
            await ctx.send(embed=embed)
            return

        except Exception as e:
            print(e)
            reqfindwarns = self.warns.find_one({"_id": ctx.message.guild.id + member.id})
            findwarns = reqfindwarns["warns"]
            self.warns.update_one({"_id": ctx.message.guild.id + member.id},
                                  {"$set": {"warns": findwarns + 1}})
            reqwarnsreason = self.warns.find_one({"_id": ctx.message.guild.id + member.id})
            warnreason = reqwarnsreason["warns"]
            warnreasonstr = str(warnreason)
            self.warns.update_one({"_id": ctx.message.guild.id + member.id},
                                  {"$set": {"warn" + warnreasonstr: reason}})

        reqbanwarns = self.warns.find_one({"_id": ctx.message.guild.id + member.id})
        banwarns = reqbanwarns["warns"]

        if banwarns >= maxwarns:
            self.warns.update_one({"_id": ctx.message.guild.id + member.id}, {"$set": {"warns": 0}})
            await member.ban(reason="Max Warns")
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

    @commands.command(aliases=["removewarns", "rw"])
    async def remove_warns(self, ctx, member: discord.Member):
        self.warns.find_one_and_delete({"_id": ctx.message.guild.id + member.id})
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully deleted {member.display_name} warns!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def checkwarns(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        reqallwarns = self.warns.find_one({"_id": ctx.message.guild.id + member.id})
        allwarns = reqallwarns["warns"]
        i = 1
        embed = discord.Embed(title=f"Check warns | {allwarns} warns", colour=discord.Color.from_rgb(244, 182, 89))
        for _ in reqallwarns:
            getwarn = reqallwarns[f"warn{i}"]
            embed.add_field(name=f"Case #{i}", value=f"Reason: {getwarn}", inline=False)
            i += 1
            if i == allwarns + 1:
                break
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, time: int):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        await ctx.channel.edit(slowmode_delay=time)
        if language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value=f"Successfully set slow mode to {time}s")
            await ctx.send(embed=embed)
        elif language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Sukces", value=f"Pomyślnie ustawiono slowmode na {time}s")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def tempmute(self, ctx, member: discord.Member, time, *, reason):
        r = self.settings.find_one({"_id": ctx.message.guild.id})
        rolemute = r["muterole"]
        language = r["language"]
        sleeptime = await convert(time)
        if language == "en":
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
        elif language == "pl":
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

    @commands.command(aliases=["purge", "delete"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, param: int = 30):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == "en":
            await ctx.channel.purge(limit=param)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Clear", value=f"Successfully deleted {param} messages!")
            await ctx.send(embed=embed)
        elif language == "pl":
            await ctx.channel.purge(limit=param)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Clear", value=f"Pomyślnie usunięto {param} wiadomości!")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, time, *, reason):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        sleeptime = await convert(time)
        if language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="TempBan")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason:", value=reason)
            embed.add_field(name="Time:", value=time)
            embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="TempBan")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.add_field(name="Czas:", value=time)
            embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
            await ctx.send(embed=embed)

        await member.ban(reason=reason)
        await asyncio.sleep(sleeptime)
        await member.unban(reason="Automatic unban")
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Unban", value=f"{member} has been automatically unbanned!")
        await ctx.send(embed=embed)

    @commands.command(aliases=["rb", "random_ban"])
    @commands.has_permissions(ban_members=True)
    async def randomban(self, ctx):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        member = random.choice(ctx.guild.members)
        await member.ban(reason="Random Ban")
        if language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="RandomBan")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value="Random Ban")
            embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="RandomBan")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason:", value="Random Ban")
            embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command(aliases=["rk", "random_kick"])
    @commands.has_permissions(kick_members=True)
    async def randomkick(self, ctx):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        member = random.choice(ctx.guild.members)
        await member.kick(reason="Random Kick")
        if language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="RandomKick")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value="Random Kick")
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="RandomKick")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value="Random Kick")
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command(aliases=["random_mute", "rm"])
    @commands.has_permissions(kick_members=True)
    async def randommute(self, ctx):
        member = random.choice(ctx.guild.members)
        if member == self.client.user:
            member = random.choice(ctx.guild.members)
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        getmuterole = self.settings.find_one({"_id": ctx.message.guild.id})
        rolemute = getmuterole["muterole"]
        if language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="RandomMute")
            embed.add_field(name="Nick:", value=f"{member}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason:", value="Random Mute")
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="RandomMute")
            embed.add_field(name="Nazwa:", value=f"{member}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value="Random Mute")
            embed.set_image(url="https://media.giphy.com/media/My6LerZy9kQLwObqWk/giphy.gif")
            await ctx.send(embed=embed)
        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name=rolemute)

        if not muteRole:
            muteRole = await guild.create_role(name=rolemute)

            for channel in guild.channels:
                await channel.set_permissions(muteRole, speak=False, send_messages=False)

        await member.add_roles(muteRole, reason="Random Mute")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def idban(self, ctx, member_id, *, reason=None):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        member = discord.Object(id=member_id)
        await ctx.guild.ban(member)
        if language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="IDBan")
            embed.add_field(name="ID:", value=f"{member_id}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="IDBan")
            embed.add_field(name="ID:", value=f"{member_id}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def idkick(self, ctx, member_id, *, reason=None):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        member = discord.Object(id=member_id)
        await ctx.guild.kick(member)
        if language == "pl":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="IDKick")
            embed.add_field(name="ID:", value=f"{member_id}")
            embed.add_field(name="Moderator:", value=ctx.message.author)
            embed.add_field(name="Powód:", value=reason)
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)
        elif language == "en":
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name="IDKick")
            embed.add_field(name="ID:", value=f"{member_id}")
            embed.add_field(name="Admin:", value=ctx.message.author)
            embed.add_field(name="Reason", value=reason)
            embed.set_image(url="https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ModerationCog(client))
