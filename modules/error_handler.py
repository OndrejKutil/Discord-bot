import nextcord
from nextcord.ext import commands

class Error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        
        if isinstance(error, commands.CommandNotFound):
            message = f"Wrong command"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown."
        elif isinstance(error, commands.MissingPermissions):
            message = "You dont have permision to use this command"
        elif isinstance(error, commands.UserInputError):
            message = "Wrong input"
        elif isinstance(error, commands.DisabledCommand):
            message = f"{ctx.command} is disabled"
        else:
            message = "Something went wrong :("

        embed25 = nextcord.Embed(
                title="Error",
                description=message,
                colour=nextcord.Colour.red()
            )

        await ctx.send(embed=embed25, delete_after=5)
        await ctx.message.delete(delay=2)

def setup(bot):
    bot.add_cog(Error_handler(bot))
