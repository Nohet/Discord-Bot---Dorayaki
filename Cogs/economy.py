import discord
from discord.ext import commands
from database import *
import random
from bot import randomdata


class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded economy.py")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    async def open_account(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            try:
                usereconomy = {"_id": ctx.message.author.id, "wallet": 0, "bank": 0, "received": False}
                collection.insert_one(usereconomy)
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Success", value=f"Successfully created account for {ctx.message.author.mention}")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Error", value="You already have an account!")
                await ctx.send(embed=embed)
        elif language == ("pl"):
            try:
                usereconomy = {"_id": ctx.message.author.id, "wallet": 0, "bank": 0, "received": False}
                collection.insert_one(usereconomy)
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Sukces", value=f"Pomyślnie utworzono konto dla {ctx.message.author.mention}")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Błąd", value="Posiadasz już konto!")
                await ctx.send(embed=embed)

    @commands.command()
    async def balance(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            try:
                currency = guildsett.find_one({"_id": ctx.message.guild.id})
                actuallcurrency = currency["currency"]
                finduser = collection.find_one({"_id": ctx.message.author.id})
                wallet_amt = finduser["wallet"]
                bank_amt = finduser["bank"]
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.set_author(name=f"{ctx.message.author}'s balance")
                embed.add_field(name="Wallet:", value=f"{wallet_amt}{actuallcurrency}")
                embed.add_field(name="Bank:", value=f"{bank_amt}{actuallcurrency}")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Error", value=f"You don't have an account, to create one type >open_account")
                await ctx.send(embed=embed)
        elif language == ("pl"):
            try:
                currency = guildsett.find_one({"_id": ctx.message.guild.id})
                actuallcurrency = currency["currency"]
                finduser = collection.find_one({"_id": ctx.message.author.id})
                wallet_amt = finduser["wallet"]
                bank_amt = finduser["bank"]
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.set_author(name=f"Saldo {ctx.message.author}")
                embed.add_field(name="Portfel:", value=f"{wallet_amt}{actuallcurrency}")
                embed.add_field(name="Bank:", value=f"{bank_amt}{actuallcurrency}")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )
                embed.add_field(name="Błąd!", value=f"Nie masz konta, aby je założyć wpisz >open_account")
                await ctx.send(embed=embed)

    @commands.command()
    async def daily(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Daily bonus",
                            value="If u want to receive daily bonus [click here(Bot site)](https://nootey.xyz)",
                            inline=False)
            await ctx.send(embed=embed)
        elif language == ("pl"):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Dzienny bonus",
                            value="Jeśli chcesz odebrać swój dzienny bonus [kliknij tutaj(Strona bota)](https://nootey.xyz)",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def send(self, ctx, member: discord.Member, money):
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findmemberbank = collection.find_one({"_id": member.id})
        memberbank = findmemberbank["bank"]
        founduserbank = int(findbank)
        moneyint = int(money)
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        print(founduserbank, moneyint)

        if language == ("en"):
            if founduserbank > moneyint:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank - moneyint}})
                collection.update_one({"_id": member.id}, {"$set": {"bank": memberbank + moneyint}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Successfully send {money} money to {member}")
                await ctx.send(embed=embed)
        if language == ("en"):
            if findbank < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money!")
                await ctx.send(embed=embed)

        if language == ("pl"):
            if founduserbank > moneyint:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank - moneyint}})
                collection.update_one({"_id": member.id}, {"$set": {"bank": memberbank + moneyint}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Sukces", value=f"Pomyślnie wysłano {money} pieniędzy dla {member}")
                await ctx.send(embed=embed)

        if language == ("pl"):
            if findbank < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd", value=f"Nie masz wystarczająco pieniędzy!")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def deposit(self, ctx, money):
        tworeq = guildsett.find_one({"_id": ctx.message.guild.id})
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findwalletamt = req["wallet"]
        findbankint = int(findbank)
        moneyint = int(money)
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            if findwalletamt > moneyint:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneyint}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": findwalletamt - moneyint}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Successfully deposited {money} {tworeq['currency']} to your account!")
                await ctx.send(embed=embed)
            elif findwalletamt < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money to deposit!")
                await ctx.send(embed=embed)
        elif language == ("pl"):
            if findwalletamt > moneyint:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneyint}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": findwalletamt - moneyint}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Sukces", value=f"Pomyślnie wpłacono {money} {tworeq['currency']} na twoje konto!")
                await ctx.send(embed=embed)
            elif findwalletamt < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd", value=f"Nie masz tyle pieniędzy do wpłacenia!")
                await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def withdraw(self, ctx, money):
        tworeq = guildsett.find_one({"_id": ctx.message.guild.id})
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findwalletamt = req["wallet"]
        findbankint = int(findbank)
        moneyint = int(money)
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == ("en"):
            if findbankint > moneyint:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - moneyint}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": findwalletamt + moneyint}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Successfully withdrawn {money} {tworeq['currency']} from your account!")
                await ctx.send(embed=embed)

            elif findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money to withdraw!")
                await ctx.send(embed=embed)

        elif language == ("pl"):
            if findbankint > moneyint:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - moneyint}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": findwalletamt + moneyint}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Sukces", value=f"Pomyślnie wypłacono {money} {tworeq['currency']} z twojego konta!")
                await ctx.send(embed=embed)

            elif findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd", value=f"Nie masz tyle pieniędzy do wypłacenia!")
                await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    async def coinflip(self, ctx, money, arg):
        randomcf = random.choice(randomdata)
        reqbank = collection.find({"_id": ctx.message.author.id})
        bank = reqbank["bank"]
        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": bank - money}})

        if randomcf == arg:
            moneyx = money * 2
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": bank + moneyx}})
            await ctx.send(f"Wygrałeś {money}, bo wypadł {randomcf}")

        else:
            await ctx.send("Przegrałeś!")

def setup(client):
    client.add_cog(EconomyCog(client))
