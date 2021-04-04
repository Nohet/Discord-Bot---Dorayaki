import discord
from discord.ext import commands
import requests
import random
from bot import blushgifdata, crygifdata, smilegifdata, thinkgifdata, hellogifdata, dancegifdata, sleepygifdata, thumbsupgifdata, happygifdata
from database import *
import requests


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    eightballquestions = ["It is certain :8ball:", "It is decidedly so :8ball:", "Without a doubt :8ball:",
                          "Yes, definitely :8ball:", "You may rely on it :8ball:", "As I see it, yes :8ball:",
                          "Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:", "Signs point to yes :8ball:",
                          "Reply hazy try again :8ball:", "Ask again later :8ball:", "Better not tell you now :8ball:",
                          "Cannot predict now :8ball:", "Concentrate and ask again :8ball:",
                          "Don't count on it :8ball:",
                          "My reply is no :8ball:", "My sources say no :8ball:", "Outlook not so good :8ball:",
                          "Very doubtful :8ball:"]

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
    async def blush(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Emotes", value=f'{ctx.message.author.mention} is blushing', inline=False)
        embed.set_image(url=random.choice(blushgifdata))
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
        embed.add_field(name="Abilities", value=f"{r['abilities'][0]} | {r['abilities'][1]}")
        embed.add_field(name="Gender", value=f"{r['gender'][0]} | {r['gender'][1]}")
        embed.add_field(name="Stats", value=f"Hp: {r['stats']['hp']} \n Attack: {r['stats']['attack']} \n Defense: {r['stats']['defense']} \n Sp_atk: {r['stats']['sp_atk']} \n Sp_def: {r['stats']['sp_def']} \n Speed: {r['stats']['speed']} \n Total: {r['stats']['total']}")
        embed.add_field(name="Evolution line", value=f"{r['family']['evolutionLine']}")
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
    async def mcsrv(self, ctx, arg):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.set_author(name="Minecraft server status")
        embed.set_image(url=f"https://mcapi.us/server/image?ip={arg}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(FunCog(client))
