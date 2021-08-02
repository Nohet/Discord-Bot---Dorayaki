import datetime
import random
from random import randint

import discord
import humanize
from discord.ext import commands

from bot import randomdata, give_voice_points
from structures.database import *
from structures.decorators import is_registered

is_registered = commands.check(is_registered)

with open("./settings.json") as f:
    bot_settings = json.load(f)

slots_random = bot_settings["bot settings"]["slots_data"]


class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.economy = economy
        self.settings = settings

    @commands.command(aliases=["profile", "account"])
    @is_registered
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        if language == "en":
            currency = self.settings.find_one({"_id": ctx.message.guild.id})
            actuallcurrency = currency["currency"]
            finduser = self.economy.find_one({"_id": member.id})
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
            currency = self.settings.find_one({"_id": ctx.message.guild.id})
            actuallcurrency = currency["currency"]
            finduser = self.economy.find_one({"_id": member.id})
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
                            value=f"""Wygrane rzuty monetą: **{finduser['coinflips']}** 
                                  Wygrane slotsy: **{finduser['slots']}**
                                  Pomyślne rabunki: **{finduser['rob']}**
                                  Wygrane wyscigi konne: **{finduser['horse_racing']}**""",
                            inline=False)
            embed.add_field(name="Statystyki Kanałów Głosowych", value=u"Spędzony czas: **{time}**".format(
                time=humanize.precisedelta(datetime.timedelta(minutes=voice_time)), inline=False))
            await ctx.send(embed=embed)

    @commands.command()
    @is_registered
    async def daily(self, ctx):
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
        language = reqlanguage["language"]
        r = self.economy.find_one({"_id": ctx.message.author.id})
        findbank = r["bank"]
        actuallcurrency = reqlanguage["currency"]
        randomamount = randint(50, 200)
        getcooldown = r["received"]
        if not getcooldown:
            if language == "en":
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank + randomamount}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"received": True}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Successfully recieved {randomamount}{actuallcurrency}")
                await ctx.send(embed=embed)
            if language == "pl":
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank + randomamount}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"received": True}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Sukces", value=f"Pomyślnie odebrano {randomamount}{actuallcurrency}")
                await ctx.send(embed=embed)
        elif getcooldown:
            if language == "en":
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank + randomamount}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"received": True}})
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
        rauthorbank = self.economy.find_one({"_id": ctx.message.author.id})
        rmemberbank = self.economy.find_one({"_id": member.id})
        authorbank = rauthorbank["wallet"]
        memberbank = rmemberbank["wallet"]
        rob_money = int(memberbank) / 3
        currency = self.settings.find_one({"_id": ctx.message.guild.id})
        actuallcurrency = currency["currency"]
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
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
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank + rob_money}})
                self.economy.update_one({"_id": member.id}, {"$set": {"wallet": memberbank - rob_money}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"rob": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success",
                                value=f"You successfully robbed {member} for {rob_money}{actuallcurrency}!")
                await ctx.send(embed=embed)
            if not is_successfull:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank - rob_money}})
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
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank + rob_money}})
                self.economy.update_one({"_id": member.id}, {"$set": {"wallet": memberbank - rob_money}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"rob": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Success", value=f"Pomyślnie okradłeś {member} z {rob_money}{actuallcurrency}!")
                await ctx.send(embed=embed)
            if not is_successfull:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"wallet": authorbank - rob_money}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Fail", value=f"Polcija Cię złapała, tracisz {rob_money}{actuallcurrency}!")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @is_registered
    async def send(self, ctx, member: discord.Member, money):
        req = self.economy.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findmemberbank = self.economy.find_one({"_id": member.id})
        memberbank = findmemberbank["bank"]
        founduserbank = int(findbank)
        moneyint = int(money)
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
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
                    self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank - moneyint}})
                    self.economy.update_one({"_id": member.id}, {"$set": {"bank": memberbank + moneyint}})
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
                    self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbank - moneyint}})
                    self.economy.update_one({"_id": member.id}, {"$set": {"bank": memberbank + moneyint}})
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
        tworeq = self.settings.find_one({"_id": ctx.message.guild.id})
        req = self.economy.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findwalletamt = req["wallet"]
        findbankint = int(findbank)
        moneyint = int(money)
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
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
                    self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneyint}})
                    self.economy.update_one({"_id": ctx.message.author.id},
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
                    self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneyint}})
                    self.economy.update_one({"_id": ctx.message.author.id},
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
        tworeq = self.settings.find_one({"_id": ctx.message.guild.id})
        req = self.economy.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findwalletamt = req["wallet"]
        findbankint = int(findbank)
        moneyint = int(money)
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
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
                    self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - moneyint}})
                    self.economy.update_one({"_id": ctx.message.author.id},
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
                    self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - moneyint}})
                    self.economy.update_one({"_id": ctx.message.author.id},
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
        req = self.economy.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findbankint = int(findbank)
        moneyint = int(money)
        normalmoney = int(money)
        moneymulti = moneyint * 2
        reqlanguage = self.settings.find_one({"_id": ctx.message.guild.id})
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
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"coinflips": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Win", value=f"You won because {arg} came out!")
                await ctx.send(embed=embed)
            else:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
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
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"coinflips": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Wygrana", value=f"Wygrałeś, ponieważ wyleciał {arg}!")
                await ctx.send(embed=embed)
            else:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
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
        req = self.economy.find_one({"_id": ctx.message.author.id})
        findbank = req["bank"]
        findbankint = int(findbank)
        moneyint = int(money)
        normalmoney = int(money)
        moneymulti = moneyint * 3
        r = self.settings.find_one({"_id": ctx.message.guild.id})
        language = r["language"]
        actuallcurrency = r["currency"]
        if language == "en":
            if findbankint < moneyint:
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Error", value=f"You don't have enough money!")
                await ctx.send(embed=embed)
            elif slotsdata4 == slotsdata5 and slotsdata6 == slotsdata4:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"slots": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"You won {money}{actuallcurrency}")
            else:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
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
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint + moneymulti}})
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"slots": +1}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"Wygrałeś {money}{actuallcurrency}")

            else:
                self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": findbankint - normalmoney}})
                embed = discord.Embed(
                    colour=discord.Color.from_rgb(244, 182, 89)
                )

                embed.add_field(name="Slots",
                                value=f"{slotsdata1} | {slotsdata2} | {slotsdata3}  \n \n {slotsdata4} | {slotsdata5} | {slotsdata6}  \n \n {slotsdata7} | {slotsdata8} | {slotsdata9}")
                await ctx.send(embed=embed)
                await ctx.send(f"Przegrałeś {money}{actuallcurrency}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            give_voice_points.start(member.id)
        if after.channel is None:
            give_voice_points.stop()


def setup(client):
    client.add_cog(EconomyCog(client))
