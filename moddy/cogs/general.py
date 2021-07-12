# -*- coding: utf-8 -*-


from discord.ext import commands
from moddy.embeds import ModdyEmbed, command_not_allowed, reload_embed
from moddy.utils import benchmark, log, reloadr, timer

reloadr()


class General(commands.Cog):
    """The description for General goes here."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    #  @commands.command(name="clear")
    #  @commands.is_owner()
    #  async def clear_messages(self, ctx: commands.Context, amount: int = 0):
    #     await ctx.channel.purge(limit=amount + 1)

    @commands.command(name="clear")
    async def clear_messages(self, ctx: commands.Context, amount: int = 0):
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.channel.purge(limit=amount)

        else:
            await ctx.send(embed=command_not_allowed("clear", "Manage messages"))
            log(ctx.guild.id)

    @commands.command(name="reload")
    async def reload_cogs(self, ctx: commands.Context):
        print("pong")
        if await self.bot.is_owner(ctx.author):
            self.bot.load_cogs(reload=True)
            await ctx.send(embed=reload_embed)
            log("[bold green]Cogs successfully reloaded")

        else:
            await ctx.send(
                embed=ModdyEmbed(
                    "Please don't embarass your self",
                    "this command is limited to my owner",
                )
            )

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        (message, duration) = timer(ctx.send("Testing Ping..."))
        print(message)
        await message.edit(
            content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round(duration * 1000)}ms"
        )


def setup(bot):
    bot.add_cog(General(bot))
