import discord
from alexflipnote import MinecraftIcons
from discord.ext import commands
import requests
import random
from bot import blushgifdata, crygifdata, smilegifdata, thinkgifdata, hellogifdata, dancegifdata, sleepygifdata, thumbsupgifdata, happygifdata
from database import *
import requests
import alexflipnote

alex_api = alexflipnote.Client("")


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded fun.py")

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
            r = requests.get(f"https://artii.herokuapp.com/make?text={arg}") .text
            await ctx.send(f"```{r}```")

    @commands.command()
    @commands.guild_only()
    async def meme(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            r = requests.get("https://some-random-api.ml/meme") .json()
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name=f"{r['caption']}")
            embed.set_image(url=r["image"])
            await ctx.send(embed=embed)
        elif language == ("pl"):
            r = requests.get("https://ivall.pl/memy.php") .json()
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_image(url=r["url"])
            await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def dog_fact(self, ctx):
        r = requests.get("https://some-random-api.ml/facts/dog") .json()
        req = requests.get("https://some-random-api.ml/img/dog") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Dog facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def cat_fact(self, ctx):
        r = requests.get("https://some-random-api.ml/facts/cat") .json()
        r1 = requests.get("https://some-random-api.ml/img/cat") .json()

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Cat facts",value=r["fact"])
        embed.set_image(url=r1["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def panda_fact(self, ctx):
        r = requests.get("https://some-random-api.ml/facts/panda") .json()
        req = requests.get("https://some-random-api.ml/img/panda") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Panda facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def fox_fact(self, ctx):
        r = requests.get("https://some-random-api.ml/facts/fox") .json()
        req = requests.get("https://some-random-api.ml/img/fox") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Fox facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def bird_fact(self, ctx):
        r = requests.get("https://some-random-api.ml/facts/bird") .json()
        req = requests.get("https://some-random-api.ml/img/birb") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Bird facts", value=r["fact"])
        embed.set_image(url=req["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def koala_fact(self, ctx):
        r = requests.get("https://some-random-api.ml/facts/koala") .json()
        req = requests.get("https://some-random-api.ml/img/koala") .json()
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
        r = requests.get("https://some-random-api.ml/animu/hug") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Hug", value=f"{ctx.message.author} is hugging {member}")
        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    async def wink(self, ctx):
        r = requests.get("https://some-random-api.ml/animu/wink") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name="Wink")
        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pat(self, ctx, member: discord.Member):
        r = requests.get("https://some-random-api.ml/animu/wink") .json()
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
        r = requests.get("https://some-random-api.ml/img/pikachu") .json()
        print(r)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.set_image(url=r["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pokedex(self, ctx, arg):
        r = requests.get(f"https://some-random-api.ml/pokedex?pokemon={arg}") .json()
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.set_author(name=f"{r['name']} | {r['id']}", icon_url=r["sprites"]["animated"])
        embed.add_field(name="Abilities", value=f"{r['abilities'][0]} | {r['abilities'][1]}", inline=False)
        embed.add_field(name="Gender", value=f"{r['gender'][0]} | {r['gender'][1]}", inline=False)
        embed.add_field(name="Stats", value=f"Hp: {r['stats']['hp']} \n Attack: {r['stats']['attack']} \n Defense: {r['stats']['defense']} \n Sp_atk: {r['stats']['sp_atk']} \n Sp_def: {r['stats']['sp_def']} \n Speed: {r['stats']['speed']} \n Total: {r['stats']['total']}", inline=False)
        embed.add_field(name="Evolution line", value=f"{r['family']['evolutionLine']}", inline=False)
        embed.set_footer(text=r["description"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def joke(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            r = requests.get("https://some-random-api.ml/joke") .json()
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Joke", value=r["joke"])
            await ctx.send(embed=embed)
        elif language == ("pl"):
            r = requests.get("https://seobot.cf/api/v1/randomjoke") .json()
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Żart", value=r["joke"])
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


def setup(client):
    client.add_cog(FunCog(client))
