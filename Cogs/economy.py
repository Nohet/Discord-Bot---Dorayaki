import discord
from discord.ext import commands
from database import *
import random
from random import randint
from bot import randomdata
from config import slotsrandomdata
from decorators import is_registered

is_registered = commands.check(is_registered)


class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded economy.py")

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
    @is_registered
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
    @is_registered
    async def daily(self, ctx):
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        reqfindbank = collection.find_one({"_id": ctx.message.author.id})
        findbank = reqfindbank["bank"]
        actuallcurrency = reqlanguage["currency"]
        randomamount = randint(50, 200)
        reqgetcooldown = collection.find_one({"_id": ctx.message.author.id})
        getcooldown = reqgetcooldown["received"]
        print(getcooldown)
        if not getcooldown:
            if language == "en":
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank + randomamount}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"received": True}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Successfully recieved {randomamount}{actuallcurrency}")
                await ctx.send(embed=embed)
            if language == "pl":
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank + randomamount}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"received": True}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Sukces", value=f"Pomyślnie odebrano {randomamount}{actuallcurrency}")
                await ctx.send(embed=embed)
        elif getcooldown:
            if language == "en":
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank + randomamount}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"received": True}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error",
                                value=f"You alredy received daily reward, you can receive it again in the 24 hours.")
                await ctx.send(embed=embed)
            if language == "pl":
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd",
                                value=f"Odebrałeś już dzienną nagrodę, możesz ją ponownie odebrać za 24 godziny")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @is_registered
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
        if "-" in money:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error", value=f"You can't send negative amount of money!!")
            await ctx.send(embed=embed)
            return
        else:
            if language == ("en"):
                if founduserbank > moneyint:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank - moneyint}})
                    collection.update_one({"_id": member.id}, {"$set": {"bank": memberbank + moneyint}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Success", value=f"Successfully send {money} money to {member}")
                    await ctx.send(embed=embed)

                if findbank < moneyint:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Error", value=f"You don't have enough money!")
                    await ctx.send(embed=embed)

            elif language == ("pl"):
                if founduserbank > moneyint:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank - moneyint}})
                    collection.update_one({"_id": member.id}, {"$set": {"bank": memberbank + moneyint}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Sukces", value=f"Pomyślnie wysłano {money} pieniędzy dla {member}")
                    await ctx.send(embed=embed)

                if findbank < moneyint:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Błąd", value=f"Nie masz wystarczająco pieniędzy!")
                    await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @is_registered
    async def deposit(self, ctx, money):
        tworeq = guildsett.find_one({"_id": ctx.message.guild.id})
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findwalletamt = req["wallet"]
        findbankint = int(findbank)
        moneyint = int(money)
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if "-" in money:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error", value=f"You can't deposit negative amount of money!!")
            await ctx.send(embed=embed)
            return
        else:
            if language == ("en"):
                if findwalletamt > moneyint:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneyint}})
                    collection.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"wallet": findwalletamt - moneyint}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Success",
                                    value=f"Successfully deposited {money} {tworeq['currency']} to your account!")
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
                    collection.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"wallet": findwalletamt - moneyint}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Sukces",
                                    value=f"Pomyślnie wpłacono {money} {tworeq['currency']} na twoje konto!")
                    await ctx.send(embed=embed)
                elif findwalletamt < moneyint:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Błąd", value=f"Nie masz tyle pieniędzy do wpłacenia!")
                    await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @is_registered
    async def withdraw(self, ctx, money):
        tworeq = guildsett.find_one({"_id": ctx.message.guild.id})
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findwalletamt = req["wallet"]
        findbankint = int(findbank)
        moneyint = int(money)
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if "-" in money:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error", value=f"You can't withdraw negative amount of money!!")
            await ctx.send(embed=embed)
            return
        else:
            if language == ("en"):
                if findbankint > moneyint:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - moneyint}})
                    collection.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"wallet": findwalletamt + moneyint}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Success",
                                    value=f"Successfully withdrawn {money} {tworeq['currency']} from your account!")
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
                    collection.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"wallet": findwalletamt + moneyint}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Sukces",
                                    value=f"Pomyślnie wypłacono {money} {tworeq['currency']} z twojego konta!")
                    await ctx.send(embed=embed)

                elif findbankint < moneyint:
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Błąd", value=f"Nie masz tyle pieniędzy do wypłacenia!")
                    await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @is_registered
    async def coinflip(self, ctx, arg, money):
        coinfliprandom = random.choice(randomdata)
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findbankint = int(findbank)
        moneyint = int(money)
        normalmoney = int(money)
        moneymulti = moneyint * 2
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        print(findbankint, moneyint)
        if language == ("en"):
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money!")
                await ctx.send(embed=embed)
            elif arg == coinfliprandom:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Win", value=f"You won because {arg} came out!")
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Loss", value=f"You lost because {arg} came out!")
                await ctx.send(embed=embed)
        elif language == ("pl"):
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Bład", value=f"Nie masz wystarczająco pieniędzy!")
                await ctx.send(embed=embed)
            elif arg == coinfliprandom:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Wygrana", value=f"Wygrałeś, ponieważ wyleciał {arg}!")
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Przegrana", value=f"Przegrałeś, ponieważ wyleciał {arg}!")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @is_registered
    async def slots(self, ctx, money):
        slotsdata1 = random.choice(slotsrandomdata)
        slotsdata2 = random.choice(slotsrandomdata)
        slotsdata3 = random.choice(slotsrandomdata)
        slotsdata4 = random.choice(slotsrandomdata)
        slotsdata5 = random.choice(slotsrandomdata)
        slotsdata6 = random.choice(slotsrandomdata)
        slotsdata7 = random.choice(slotsrandomdata)
        slotsdata8 = random.choice(slotsrandomdata)
        slotsdata9 = random.choice(slotsrandomdata)
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findbankint = int(findbank)
        moneyint = int(money)
        normalmoney = int(money)
        moneymulti = moneyint * 2
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        currency = guildsett.find_one({"_id": ctx.message.guild.id})
        actuallcurrency = currency["currency"]
        if language == ("en"):
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money!")
                await ctx.send(embed=embed)
            elif slotsdata4 == slotsdata5 and slotsdata6 == slotsdata4:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"You won {money}{actuallcurrency}")
            elif slotsdata4 != slotsdata5 and slotsdata6 != slotsdata4:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"You lost {money}{actuallcurrency}")

        elif language == ("pl"):
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd", value=f"Nie masz wystarczająco pieniędzy!")
                await ctx.send(embed=embed)

            elif slotsdata4 == slotsdata5 and slotsdata6 == slotsdata4:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"Wygrałeś {money}{actuallcurrency}")

            elif slotsdata4 != slotsdata5 and slotsdata6 != slotsdata4:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"Przegrałeś {money}{actuallcurrency}")

    @commands.command()
    async def leaderboard(self, ctx):
        rankings = collection.find().sort("bank")
        i = 1
        embed = discord.Embed(title="Money leaderboard", colour=discord.Color.from_rgb(244, 182, 89))
        for x in rankings:
            temp = await self.client.fetch_user(x["_id"])
            tempxp = x["bank"]
            print(embed.add_field(name=f'{i}: {temp}', value=f'Money in bank: {tempxp}', inline=False))
            i += 1
            if i == 11:
                break
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(EconomyCog(client))
