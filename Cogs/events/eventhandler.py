import discord
from discord.ext import commands


class EventHandlerCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
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
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error",
                            value=f"Argument <**{error.param}**> cannot be empty!",
                            inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                colour=discord.Color.from_rgb(244, 182, 89)
            )
            embed.add_field(name="Error",
                            value=f"Member <**{error.argument}**> has been not found!",
                            inline=False)
            await ctx.send(embed=embed)

        else:
            print(error)
            await ctx.send(error)


def setup(client):
    client.add_cog(EventHandlerCog(client))
