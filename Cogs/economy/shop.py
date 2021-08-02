import discord
from discord.ext import commands

from structures.database import *
from structures.decorators import is_registered

is_registered = commands.check(is_registered)

available_items = ["crystal", "fishing rod", "pickaxe", "sword", "dorayaki",
                   "pancake"]
items_price = ["crystal-price | 300", "fishing rod-price | 1200", "pickaxe-price | 1500",
               "sword-price | 700", "dorayaki-price | 12500", "pancake-price | 10000"]


class ShopCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.economy = economy
        self.settings = settings

    @commands.group(invoke_without_command=True)
    @is_registered
    async def shop(self, ctx):
        r = self.settings.find_one({"_id": ctx.guild.id})
        prefix = r["prefix"]
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Shop", value=f"In the shop you can buy, sell, and create items!", inline=False)
        embed.add_field(name="Available commands", value=f"""{prefix}shop buy <item>
                                                             {prefix}shop sell <item>
                                                             {prefix}shop create
                                                             {prefix}shop items""", inline=False)
        await ctx.send(embed=embed)

    @shop.command(aliases=["buyitem", "bi"])
    @is_registered
    async def buy(self, ctx, *, item):
        r = self.economy.find_one({"_id": ctx.message.author.id})
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
                        self.economy.update_one({"_id": ctx.message.author.id}, {"$set": {"items": your_items}})
                        self.economy.update_one({"_id": ctx.message.author.id},
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

    @shop.command(aliases=["sell", "si", "sellitem"])
    @commands.guild_only()
    @is_registered
    async def sell_item(self, ctx, *, item):
        r = self.economy.find_one({"_id": ctx.message.author.id})
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
                    self.economy.update_one({"_id": ctx.message.author.id},
                                          {"$set": {"items": your_items}})
                    self.economy.update_one({"_id": ctx.message.author.id},
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

    @shop.command(aliases=["createitem", "ci", "create"])
    @commands.guild_only()
    @is_registered
    async def create_item(self, ctx):
        r = self.settings.find_one({"_id": ctx.message.guild.id})
        r2 = self.economy.find_one({"_id": ctx.message.author.id})
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
                        self.economy.update_one({"_id": ctx.message.author.id},
                                              {"$set": {"bank": r2["bank"] - 5000}})
                        embed3 = discord.Embed(
                            colour=discord.Color.from_rgb(244, 182, 89)
                        )

                        embed3.add_field(name="Success",
                                         value=f"Successfully created item, now this item will be available global!\n"
                                               f"This item will be available until the bot restart.")
                        await ctx.send(embed=embed3)

    @shop.command()
    @commands.guild_only()
    async def items(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )

        embed.add_field(name="Available items", value=str.join(", ", available_items))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ShopCog(client))
