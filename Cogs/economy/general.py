import datetime
import random
from random import randint

import discord
import humanize
from discord.ext import commands

from bot import randomdata, give_voice_points
from database import *
from decorators import is_registered

is_registered = commands.check(is_registered)

with open("./settings.json") as f:
    settings = json.load(f)

slots_random = settings["bot settings"]["slots_data"]

available_items = ["crystal", "fishing rod", "pickaxe", "sword", "dorayaki",
                   "pancake"]
items_price = ["crystal-price | 300", "fishing rod-price | 1200", "pickaxe-price | 1500",
               "sword-price | 700", "dorayaki-price | 12500", "pancake-price | 10000"]


class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["profile", "account"])
    @is_registered
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == "en":
            currency = guildsett.find_one({"_id": ctx.message.guild.id})
            actuallcurrency = currency["currency"]
            finduser = collection.find_one({"_id": member.id})
            wallet_amt = finduser["wallet"]
            bank_amt = finduser["bank"]
            items = finduser["items"]
            items = items.split(" | ")
            voice_time = finduser["voice_time"]
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name=f"{member} profile")
            embed.add_field(name="Economy Stats",
                            value=f"Items: **{str.join(', ', items)}**\n Wallet: **{wallet_amt}{actuallcurrency}**\nBank: **{bank_amt}{actuallcurrency}**\nTotal: **{wallet_amt + bank_amt}{actuallcurrency}**",
                            inline=False)
            embed.add_field(name="Game Stats",
                            value=f"Won coinflips: **{finduser['coinflips']}** \nWon slots: **{finduser['slots']}**\nSuccessfull robberies: **{finduser['rob']}** \nWon horse racing: **{finduser['horse_racing']}**",
                            inline=False)
            embed.add_field(name="Voice Channels Stats",
                            value=f"Time Spent: **{humanize.precisedelta(datetime.timedelta(minutes=voice_time))}**",
                            inline=False)

            await ctx.send(embed=embed)
        elif language == "pl":
            currency = guildsett.find_one({"_id": ctx.message.guild.id})
            actuallcurrency = currency["currency"]
            finduser = collection.find_one({"_id": member.id})
            wallet_amt = finduser["wallet"]
            bank_amt = finduser["bank"]
            items = finduser["items"]
            items = items.split(" | ")
            voice_time = finduser["voice_time"]
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.set_author(name=f"Profil {member}")
            embed.add_field(name="Statystyki Ekonomi",
                            value=f"Przedmioty: **{str.join(', ', items)}**\nPortfel: **{wallet_amt}{actuallcurrency}**\nBank: **{bank_amt}{actuallcurrency}**\nRazem: **{wallet_amt + bank_amt}{actuallcurrency}**",
                            inline=False)
            embed.add_field(name="Statystyki Gier",
                            value=u"""Wygrane rzuty monetą: **{coin_flips}** 
                                  Wygrane slotsy: **{won_slots}**
                                  Pomyślne rabunki: **{success_robberies}**
                                  Wygrane wyscigi konne: **{won_horse}**""".format(coin_flips=finduser['coinflips'],
                                                                                   won_slots=finduser['slots'],
                                                                                   success_robberies=finduser['rob'],
                                                                                   won_horse=finduser['horse_racing']),
                            inline=False)
            embed.add_field(name="Statystyki Kanałów Głosowych", value=u"Spędzony czas: **{time}**".format(
                time=humanize.precisedelta(datetime.timedelta(minutes=voice_time)), inline=False))
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
    @commands.cooldown(1, 28800, commands.BucketType.user)
    @is_registered
    async def rob(self, ctx, member: discord.Member):
        rauthorbank = collection.find_one({"_id": ctx.message.author.id})
        rmemberbank = collection.find_one({"_id": member.id})
        authorbank = rauthorbank["wallet"]
        memberbank = rmemberbank["wallet"]
        rob_money = int(memberbank) / 3
        currency = guildsett.find_one({"_id": ctx.message.guild.id})
        actuallcurrency = currency["currency"]
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        random_is_successfull = [True, False]
        is_successfull = random.choice(random_is_successfull)
        if language == "en":
            if int(memberbank) < 500:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Not Worth", value=f"Not worth, member doesn't even have 500 {actuallcurrency}!")
                await ctx.send(embed=embed)
                self.rob.reset_cooldown(ctx)
                return

            if int(authorbank) < rob_money:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error",
                                value=f"You can't rob someone, if you don't even have 1/3 of their wallet amont!")
                await ctx.send(embed=embed)
                self.rob.reset_cooldown(ctx)
                return

            if is_successfull:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank + rob_money}})
                collection.update_one({"_id": member.id}, {"$set": {"wallet": memberbank - rob_money}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"rob": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success",
                                value=f"You successfully robbed {member} for {rob_money}{actuallcurrency}!")
                await ctx.send(embed=embed)
            if not is_successfull:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank - rob_money}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Fail", value=f"The police caught you, you lose {rob_money}{actuallcurrency}!")
                await ctx.send(embed=embed)

        elif language == "pl":
            if int(memberbank) < 500:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Nie warto", value=f"Nie warto, użytkownik nie ma nawet 500 {actuallcurrency}!")
                await ctx.send(embed=embed)
                self.rob.reset_cooldown(ctx)
                return

            if int(authorbank) < rob_money:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd",
                                value=f"Nie możesz okraść kogoś, nie posiadając nawet 1/3 sumy jego/jej portfela!")
                await ctx.send(embed=embed)
                self.rob.reset_cooldown(ctx)
                return

            if is_successfull:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank + rob_money}})
                collection.update_one({"_id": member.id}, {"$set": {"wallet": memberbank - rob_money}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"rob": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Pomyślnie okradłeś {member} z {rob_money}{actuallcurrency}!")
                await ctx.send(embed=embed)
            if not is_successfull:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank - rob_money}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Fail", value=f"Polcija Cię złapała, tracisz {rob_money}{actuallcurrency}!")
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
            if language == "en":
                if founduserbank >= moneyint:
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

            elif language == "pl":
                if founduserbank >= moneyint:
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
            if language == "en":
                if findwalletamt >= moneyint:
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
            elif language == "pl":
                if findwalletamt >= moneyint:
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
            if language == "en":
                if findbankint >= moneyint:
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

            elif language == "pl":
                if findbankint >= moneyint:
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
        if language == "en":
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money!")
                await ctx.send(embed=embed)
            elif arg == coinfliprandom:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"coinflips": +1}})
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
        elif language == "pl":
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Bład", value=f"Nie masz wystarczająco pieniędzy!")
                await ctx.send(embed=embed)
            elif arg == coinfliprandom:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"coinflips": +1}})
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
        slotsdata1 = random.choice(slots_random)
        slotsdata2 = random.choice(slots_random)
        slotsdata3 = random.choice(slots_random)
        slotsdata4 = random.choice(slots_random)
        slotsdata5 = random.choice(slots_random)
        slotsdata6 = random.choice(slots_random)
        slotsdata7 = random.choice(slots_random)
        slotsdata8 = random.choice(slots_random)
        slotsdata9 = random.choice(slots_random)
        req = collection.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findbankint = int(findbank)
        moneyint = int(money)
        normalmoney = int(money)
        moneymulti = moneyint * 3
        reqlanguage = guildsett.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        currency = guildsett.find_one({"_id": ctx.message.guild.id})
        actuallcurrency = currency["currency"]
        if language == "en":
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money!")
                await ctx.send(embed=embed)
            elif slotsdata4 == slotsdata5 and slotsdata6 == slotsdata4:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"slots": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"You won {money}{actuallcurrency}")
            else:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"You lost {money}{actuallcurrency}")

        elif language == "pl":
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Błąd", value=f"Nie masz wystarczająco pieniędzy!")
                await ctx.send(embed=embed)

            elif slotsdata4 == slotsdata5 and slotsdata6 == slotsdata4:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"slots": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"Wygrałeś {money}{actuallcurrency}")

            else:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"Przegrałeś {money}{actuallcurrency}")

    @commands.command(aliases=["buyitem", "bi", "buy"])
    @commands.guild_only()
    @is_registered
    async def buy_item(self, ctx, *, item):
        r = collection.find_one({"_id": ctx.message.author.id})
        user_balance = r["bank"]
        your_items = r["items"]
        your_items = your_items.split(" | ")
        if item in your_items:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error", value=f"You already have that item!")
            await ctx.send(embed=embed)
            return

        if item in available_items:
            for item_price in items_price:
                if str(item) in item_price:
                    item_prc = item_price.split(" | ")
                    item_prc = item_prc[1].replace(" ", "")
                    if user_balance >= int(item_prc):
                        your_items.append(item)
                        your_items = str.join(" | ", your_items)
                        your_items = your_items.replace("None | ", "")
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"items": your_items}})
                        collection.update_one({"_id": ctx.message.author.id},
                                              {"$set": {"bank": user_balance - int(item_prc)}})
                        embed = discord.Embed(
                            colour=discord.Color.from_rgb(244, 182, 89)
                        )

                        embed.add_field(name="Success", value=f"Successfully bought **{item}**!")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            colour=discord.Color.from_rgb(244, 182, 89)
                        )

                        embed.add_field(name="Error", value=f"You don't have enought money to buy this item!")
                        await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error", value="This item does not exist!")
            await ctx.send(embed=embed)

    @commands.command(aliases=["sell", "si", "sellitem"])
    @commands.guild_only()
    @is_registered
    async def sell_item(self, ctx, *, item):
        r = collection.find_one({"_id": ctx.message.author.id})
        user_balance = r["bank"]
        your_items = r["items"]
        your_items_list = your_items.split(" | ")
        if item in your_items_list:
            for item_price in items_price:
                if str(item) in item_price:
                    item_prc = item_price.split(" | ")
                    item_prc = item_prc[1].replace(" ", "")
                    item_prc = int(item_prc) / 2
                    if your_items.endswith(item):
                        your_items = your_items + " |"
                    if your_items.startswith(item):
                        your_items = "| " + your_items
                    your_items = your_items.replace("| " + item + " |", "")
                    collection.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"items": your_items}})
                    collection.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"bank": user_balance + int(item_prc)}})
                    embed = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed.add_field(name="Success", value=f"Successfully sold **{item}**!")
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error", value=f"You don't have this item!")
            await ctx.send(embed=embed)

    @commands.command(aliases=["createitem", "ci"])
    @commands.guild_only()
    @is_registered
    async def create_item(self, ctx):
        r = guildsett.find_one({"_id": ctx.message.guild.id})
        r2 = collection.find_one({"_id": ctx.message.author.id})
        if r2["bank"] <= 5000:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Error",
                            value=f"You don't have enough money to create your item! (5000{r['currency']})")
            await ctx.send(embed=embed)
            return False
        else:
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )

            embed.add_field(name="Sure?",
                            value=f"Are you sure want to create your own item, this will cost you 5000{r['currency']}? (yes/no)")
            await ctx.send(embed=embed)
            msg1 = await self.client.wait_for("message", timeout=15)
            if msg1.content == "yes":
                embed1 = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed1.add_field(name="Name",
                                 value=f"Type name of your item.")
                await ctx.send(embed=embed1)
                msg2 = await self.client.wait_for("message", timeout=15)
                if msg2.content in available_items:
                    errembed1 = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    errembed1.add_field(name="Error", value="That item already exists!")
                    await ctx.send(embed=errembed1)
                    return
                if "-" in msg2.content or "|" in msg2.content:
                    errembed1 = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    errembed1.add_field(name="Error", value="Name can't include - or |")
                    await ctx.send(embed=errembed1)
                else:
                    embed2 = discord.Embed(
                        colour=discord.Color.from_rgb(244, 182, 89)
                    )

                    embed2.add_field(name="Price",
                                     value=f"Type price for your item.")
                    await ctx.send(embed=embed2)
                    msg3 = await self.client.wait_for("message", timeout=15)
                    if "-" in msg3.content or "|" in msg3.content:
                        errembed2 = discord.Embed(
                            colour=discord.Color.from_rgb(244, 182, 89)
                        )

                        errembed2.add_field(name="Error", value="Price can't include - or |")
                        await ctx.send(embed=errembed2)
                    else:
                        available_items.append(msg2.content)
                        items_price.append(f"{msg2.content}-price | {msg3.content}")
                        collection.update_one({"_id": ctx.message.author.id},
                                              {"$set": {"bank": r2["bank"] - 5000}})
                        embed3 = discord.Embed(
                            colour=discord.Color.from_rgb(244, 182, 89)
                        )

                        embed3.add_field(name="Success",
                                         value=f"Successfully created item, now this item will be available global!\n"
                                               f"This item will be available until the bot restart.")
                        await ctx.send(embed=embed3)

    @commands.command()
    @commands.guild_only()
    async def items(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Available items", value=str.join(", ", available_items))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            give_voice_points.start(member.id)
        if after.channel is None:
            give_voice_points.stop()


def setup(client):
    client.add_cog(EconomyCog(client))
