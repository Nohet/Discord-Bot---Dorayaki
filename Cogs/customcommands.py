import discord
from discord.ext import commands
from database import guildsett


class CustomCommandsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded customcommands.py")

    @commands.Cog.listener()
    async def on_message(self, message):
        r = guildsett.find_one({"_id": message.guild.id})
        getprefix = r["prefix"]
        getcommandname1 = r["1customcmdname"]
        getcommandtype1 = r["1customcmdtype"]
        getcommandcontent1 = r["1customcmdcontent"]
        getcommandname2 = r["2customcmdname"]
        getcommandtype2 = r["2customcmdtype"]
        getcommandcontent2 = r["2customcmdcontent"]
        getcommandname3 = r["3customcmdname"]
        getcommandtype3 = r["3customcmdtype"]
        getcommandcontent3 = r["3customcmdcontent"]
        getcommandname4 = r["4customcmdname"]
        getcommandtype4 = r["4customcmdtype"]
        getcommandcontent4 = r["4customcmdcontent"]
        getcommandname5 = r["5customcmdname"]
        getcommandtype5 = r["5customcmdtype"]
        getcommandcontent5 = r["5customcmdcontent"]
        if message.content == (f"{getprefix}{getcommandname1}"):
            if getcommandtype1 == ("text"):
                await message.channel.send(getcommandcontent1)

            elif getcommandtype1 == ("embed"):
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name=message.guild, value=getcommandcontent1)
                await message.channel.send(embed=embed)

        elif message.content == (f"{getprefix}{getcommandname2}"):
            if getcommandtype2 == ("text"):
                await message.channel.send(getcommandcontent2)

            elif getcommandtype2 == ("embed"):
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name=message.guild, value=getcommandcontent2)
                await message.channel.send(embed=embed)

        elif message.content == (f"{getprefix}{getcommandname3}"):
            if getcommandtype3 == ("text"):
                await message.channel.send(getcommandcontent3)

            elif getcommandtype3 == ("embed"):
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name=message.guild, value=getcommandcontent3)
                await message.channel.send(embed=embed)

        elif message.content == (f"{getprefix}{getcommandname4}"):
            if getcommandtype4 == ("text"):
                await message.channel.send(getcommandcontent4)

            elif getcommandtype4 == ("embed"):
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name=message.guild, value=getcommandcontent4)
                await message.channel.send(embed=embed)

        elif message.content == (f"{getprefix}{getcommandname5}"):
            if getcommandtype5 == ("text"):
                await message.channel.send(getcommandcontent5)
            elif getcommandtype5 == ("embed"):
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name=message.guild, value=getcommandcontent5)
                await message.channel.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def customcmd(self, ctx, number: int, method, type=None, name=None, *mess):
        content = (" ").join(mess)
        if number < 6:
            if method == ("edit"):
                guildsett.update_one({"_id": ctx.message.guild.id},
                                    {"$set": {f"{number}customcmdname": name, f"{number}customcmdtype": type, f"{number}customcmdcontent": content}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Success", value=f"Successfully edited command number {number}")
                await ctx.send(embed=embed)

            elif method == ("delete"):
                guildsett.update_one({"_id": ctx.message.guild.id},
                                    {"$set": {f"{number}customcmdname": None, f"{number}customcmdtype": None, f"{number}customcmdcontent": None}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Success", value=f"Successfully deleted command number {number}")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value="The max commands number is 5")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CustomCommandsCog(client))
