import random
import re

import aiohttp
from discord.ext import commands
from discordwebhook import Discord

from database import guildsett

regex = re.compile(
    r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b')


class MonetizeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        r = guildsett.find_one({"_id": message.guild.id})
        setting = r["monetization"]
        hook = Discord(url=r["webhook"])
        if setting == "on" or setting == "enable" or setting == "True":
            random_data = ["User", "Bot Owner"]
            random_data = random.choice(random_data)

            mess = message.content
            urls = re.findall(regex, mess)
            if len(urls) >= 1:
                if random_data == "Bot Owner":
                    await message.delete()
                    async with aiohttp.ClientSession(headers={'User-ID': '252446', 'URL': urls[0]}) as session:
                        async with session.get('http://127.0.0.1/api/monetize/') as response:
                            text = await response.json()
                            new_url = text['url']
                            new_mess = mess.replace(urls[0], new_url)
                            hook.post(
                                content=str(new_mess),
                                username=str(message.author.name),
                                avatar_url=str(message.author.avatar_url)
                            )
                            return
                elif random_data == "User":
                    await message.delete()
                    async with aiohttp.ClientSession(headers={'User-ID': r["linkvertise"], 'URL': urls[0]}) as session:
                        async with session.get('http://127.0.0.1/api/monetize/') as response:
                            text = await response.json()
                            new_url = text['url']
                            new_mess = mess.replace(urls[0], new_url)
                            hook.post(
                                content=str(new_mess),
                                username=str(message.author.name),
                                avatar_url=str(message.author.avatar_url)
                            )
                            return

        else:
            return

    @commands.command()
    async def setup(self, ctx):
        await ctx.send("**How to setup monetization?** \n1. __Enabling monetization module:__ \nRemember that you must have administrator permissions! \nType >settings monetization on  \n2. __Linkvertise account id:__ \n Create account on https://publisher.linkvertise.com \n Dashboard ---> Full script api ---> https://i.imgur.com/7waeIPA.png \nType >settings linkvertise <id> \n3. __Discord Webhook Url:__ \nClick 'Edit channel' on channel where you want to create webhook \nIntegrations ---> Webhooks ---> New Webhook ---> https://i.imgur.com/QhcVg8K.png \nType >settings webhook <url>")


def setup(client):
    client.add_cog(MonetizeCog(client))
