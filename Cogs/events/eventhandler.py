import datetime
import logging
import sys
import time

import discord
import humanize
import psutil
from discord.ext import commands

from bot import start_time
from structures.database import settings, cluster

now = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
now = str(now).replace(":", "-")

logging.basicConfig(filename=f"logs/{now}.log",
                    format='%(asctime)s --- %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

general_chat_name = ["general", "chat", "czat", "rozmowa", "główny", "ogólny", "offtopic",
                     "pogaduchy", "rozmowy", "ogólne", "main", "ogolny", "off-topic",
                     "pisanko"]


class EventHandlerCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.settings = settings

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        haveGuildSetiings = self.settings.find_one({"_id": guild.id})
        if not haveGuildSetiings:
            webhook_list = []
            for channel in guild.text_channels:
                for name in general_chat_name:
                    if name in channel.name:
                        webhook = await channel.create_webhook(name="Dorayaki-Monetize-Module")
                        webhook_list.append(webhook.url)
                        embed = discord.Embed(
                            colour=discord.Color.from_rgb(244, 182, 89)
                        )
                        embed.add_field(name="Automatical Chat Detection", value=f"Successfully detected "
                                                                                 f"{channel.mention} as chat! "
                                                                                 f"Created webhook for that "
                                                                                 f"channel for monetization module."
                                                                                 f" Type >setup if you want to know "
                                                                                 f"more! "
                                        )
                        await channel.send(embed=embed)

            if len(webhook_list) <= 0: webhook_list.append(None)
            guildSettings = {"_id": guild.id, "prefix": ">", "muterole": "Muted", "maxwarns": 3,
                             "language": "en",
                             "currency": "$", "logs": "disable", "logsChannel": None, "autorole": "disable",
                             "autoroleRole": None, "leave_messages": "disable", "join_messages": "disable",
                             "leave_messages_channel": None, "join_messages_channel": None,
                             "leave_messages_content": None, "join_messages_content": None,
                             "leave_messages_type": None, "join_messages_type": None, "monetization": "disable",
                             "linkvertise": None, "links_information": "disable", "webhook": webhook_list[0]}
            self.settings.insert_one(guildSettings)
            print(f"Successfully added {guild.name} | {guild.id} guild to database!")

        else:
            print(f"{guild.name} | {guild.id} guild already in database, skipped!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user: return
        if len(message.mentions) != 1: return
        if message.mentions[0] == self.client.user:
            settings = self.settings.find_one({"_id": message.guild.id})
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = humanize.precisedelta(datetime.timedelta(seconds=difference))
            memory = psutil.virtual_memory().used
            memorystr = str(memory)
            pyversion = sys.version
            mongo_db_ping = cluster.settings.command('ping')
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Prefix", value=settings["prefix"])
            embed.add_field(name="Discord.py version", value=discord.__version__, inline=False)
            embed.add_field(name="Python version", value=pyversion[:5], inline=False)
            embed.add_field(name="Uptime", value=text, inline=False)
            embed.add_field(name="Bot ping", value=f'{round(self.client.latency * 1000)}ms', inline=False)
            embed.add_field(name="MongoDB ping", value=f'{mongo_db_ping["ok"]}ms', inline=False)
            embed.add_field(name="CPU", value=f'{psutil.cpu_percent()}%', inline=False)
            embed.add_field(name="Ram (whole vps)", value=f"{memorystr[:1]}GB ({psutil.virtual_memory().percent}%)",
                            inline=False)
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            logger.info(f"Command on cooldown! Command used in {ctx.guild.name} | {ctx.guild.id} "
                        f"guild by {ctx.message.author} | {ctx.message.author.id}!")
            cooldown = error.retry_after
            str_cooldown = str(cooldown)
            short_cooldown = str_cooldown.split(".")
            int_cooldown = int(short_cooldown[0])
            hour_cooldown = int_cooldown / 3600
            str_hour_cooldown = str(hour_cooldown)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error",
                            value=f"This command is still on cooldown, try again in the {int_cooldown} seconds\n(about {str_hour_cooldown[:4]} hour/s)",
                            inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            r = error.missing_perms
            perms = r[0]
            logger.info(f"Missing permissions to use command! Command used in {ctx.guild.name} | {ctx.guild.id} "
                        f"guild by {ctx.message.author} | {ctx.message.author.id}!")
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error",
                            value=f"You are missing permissions to use this command! (**{perms}**)",
                            inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("❌")

        elif isinstance(error, commands.MissingRequiredArgument):
            logger.info(f"Missing command argument(s)! Command used in {ctx.guild.name} | {ctx.guild.id} "
                        f"guild by {ctx.message.author} | {ctx.message.author.id}!")
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error",
                            value=f"Argument <**{error.param}**> cannot be empty!",
                            inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            logger.info(f"Member not found! Command used in {ctx.guild.name} | {ctx.guild.id} "
                        f"guild by {ctx.message.author} | {ctx.message.author.id}!")
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error",
                            value=f"Member <**{error.argument}**> has been not found!",
                            inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NSFWChannelRequired):
            logger.info(f"Not nsfw channel! Command used in {ctx.guild.name} | {ctx.guild.id} "
                        f"guild by {ctx.message.author} | {ctx.message.author.id}!")
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error", value="This channel is not nsfw, i can't send it here!")
            await ctx.send(embed=embed)

        else:
            logger.info(error)
            print(error)


def setup(client):
    client.add_cog(EventHandlerCog(client))
