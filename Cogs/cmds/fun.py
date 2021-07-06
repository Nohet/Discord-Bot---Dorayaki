import random
from datetime import datetime

import aiohttp
import alexflipnote
import discord
from alexflipnote import MinecraftIcons
from discord.ext import commands

from bot import blushgifdata, crygifdata, smilegifdata, thinkgifdata, hellogifdata, dancegifdata, sleepygifdata, \
    thumbsupgifdata, happygifdata
from database import *

with open("./settings.json") as f:
    settings = json.load(f)

alex_api = alexflipnote.Client(settings["bot settings"]["alexflipnote_api_key"])


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def ascii(self, ctx, *, arg):
        if len(arg) > 22:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value="The maximum length has been exceeded")
            await ctx.send(embed=embed)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://artii.herokuapp.com/make?text={arg}") as response:
                    r = await response.text()
                    await ctx.send(f"```py\n{r}```")

    @commands.command()
    @commands.guild_only()
    async def meme(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == "en":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/meme") as response:
                    r = await response.json()
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )
                embed.set_author(name=f"{r['caption']}")
                embed.set_image(url=r["image"])
                await ctx.send(embed=embed)
        elif language == "pl":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ivall.pl/memy.php") as response:
                    r = await response.json()
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.set_image(url=r["url"])
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def dog_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/dog") as response:
                r = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/dog") as response:
                req = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Dog facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def cat_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/cat") as response:
                r = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/cat") as response:
                r1 = await response.json()

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Cat facts", value=r["fact"])
        embed.set_image(url=r1["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def panda_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/panda") as response:
                r = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/panda") as response:
                req = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Panda facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def fox_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/fox") as response:
                r = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/fox") as response:
                req = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Fox facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def bird_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/bird") as response:
                r = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/birb") as response:
                req = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Bird facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def koala_fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/koala") as response:
                r = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/koala") as response:
                req = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Koala facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def blush(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is blushing', inline=False)
        embed.set_image(url=random.choice(blushgifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def hug(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/hug") as response:
                r = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Hug", value=f"{ctx.message.author} is hugging {member}")
        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    async def wink(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/wink") as response:
                r = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name="Wink")
        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pat(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/wink") as response:
                r = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Pat", value=f"{ctx.message.author} is patting {member}")
        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def dance(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)()
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is dancing', inline=False)
        embed.set_image(url=random.choice(dancegifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def smile(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} smiled', inline=False)
        embed.set_image(url=random.choice(smilegifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def sleepy(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is sleepy', inline=False)
        embed.set_image(url=random.choice(sleepygifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def thinking(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is thinking', inline=False)
        embed.set_image(url=random.choice(thinkgifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def hello(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} says hello', inline=False)
        embed.set_image(url=random.choice(hellogifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def thumbsup(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} holds his thumbs up', inline=False)
        embed.set_image(url=random.choice(thumbsupgifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def happy(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is happy', inline=False)
        embed.set_image(url=random.choice(happygifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def cry(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is crying', inline=False)
        embed.set_image(url=random.choice(crygifdata))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pikachu(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/pikachu") as response:
                r = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pokedex(self, ctx, arg):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/pokedex?pokemon={arg}") as response:
                r = await response.json()
        evolution_line = r['family']['evolutionLine']
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.set_author(name=f"{r['name']} | {r['id']}", icon_url=r["sprites"]["animated"])
        embed.add_field(name="Abilities", value=f"{r['abilities'][0]} | {r['abilities'][1]}", inline=False)
        embed.add_field(name="Gender", value=f"{r['gender'][0]} | {r['gender'][1]}", inline=False)
        embed.add_field(name="Stats",
                        value=f"Hp: {r['stats']['hp']} \n Attack: {r['stats']['attack']} \n Defense: {r['stats']['defense']} \n Sp_atk: {r['stats']['sp_atk']} \n Sp_def: {r['stats']['sp_def']} \n Speed: {r['stats']['speed']} \n Total: {r['stats']['total']}",
                        inline=False)
        embed.add_field(name="Evolution line", value=f"{str.join(' | ', evolution_line)}", inline=False)
        embed.set_footer(text=r["description"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/joke") as response:
                r = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Joke", value=r["joke"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def mcsrv(self, ctx, arg):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.set_author(name="Minecraft server status")
        embed.set_image(url=f"https://mcapi.us/server/image?ip={arg}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def achievement(self, ctx, *, arg):
        aclogo_logo = await alex_api.achievement(arg, icon=MinecraftIcons.RANDOM)
        ac_bytes = await aclogo_logo.read()
        await ctx.send(file=discord.File(ac_bytes, filename="achievement.png"))

    @commands.command()
    @commands.guild_only()
    async def captcha(self, ctx, *, arg):
        captcha_logo = await alex_api.captcha(arg)
        captcha_bytes = await captcha_logo.read()
        await ctx.send(file=discord.File(captcha_bytes, filename="captcha.png"))

    @commands.command()
    @commands.guild_only()
    async def timer(self, ctx):

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Timer", value=f"Clicked in `???`")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("⏱️")
        a = datetime.now()

        def check(react, user):
            return user == ctx.message.author and ctx.message.channel == react.message.channel

        await self.client.wait_for("reaction_add", timeout=90, check=check)

        b = datetime.now()
        d = b - a
        newembed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 80)

        )
        newembed.add_field(name="Timer", value=f"Clicked in `{str(d.seconds) + ':' + str(d.microseconds)[:2]}s`")
        await msg.edit(embed=newembed)

    @commands.command(aliases=["writespeed", "ws", "typewriter"])
    @commands.guild_only()
    async def write_speed(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random-word-api.herokuapp.com/word?number=1") as response:
                r = await response.json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Write Speed", value=f"Write `{r[0]}`")
        msg = await ctx.send(embed=embed)
        a = datetime.now()

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        message = await self.client.wait_for("message", timeout=90, check=check)
        b = datetime.now()
        d = b - a
        if message.content == r[0]:
            newembed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            newembed.add_field(name="Write Speed",
                               value=f"Successfully writed `{message.content}` in {str(d.seconds) + ':' + str(d.microseconds)[:2]}s")
            await msg.edit(embed=newembed)

        else:
            emb = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            emb.add_field(name="Write Speed", value=f"You write wrong word!")
            await msg.edit(embed=emb)

    @commands.command(aliases=["guess", "wi"])
    async def whois(self, ctx):
        member = random.choice(ctx.guild.members)
        membername = member.name + "#" + member.discriminator
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Who is this?", value="Mention that member, or type name and discriminator! \nExample: "
                                                   "Nohet#2453")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        message = await self.client.wait_for("message", timeout=15, check=check)

        mess = message.content
        mess = mess.replace("!", "")

        if mess == member.mention or message.content == membername:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Success", value="Successfully guessed member!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Nope", value="Its not that member!")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(FunCog(client))
