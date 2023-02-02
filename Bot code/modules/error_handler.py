import nextcord
from nextcord.ext import commands

class Error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        
        if isinstance(error, commands.CommandNotFound):
            message = f"**❌ Sorry, this command does not exist.**"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"**❌ This command is on cooldown.**"
        elif isinstance(error, commands.MissingPermissions):
            message = "**❌ You do not have the permisions to use this command.**"
        elif isinstance(error, commands.UserInputError):
            message = "**❌ You used wrong input, try again.**"
        elif isinstance(error, commands.DisabledCommand):
            message = f"**❌ Sorry, {ctx.command} is disabled**"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = "**❌ You missed some argument, try again**"
        elif isinstance(error, commands.CommandError):
            message = "**❌ Sorry, something went wrong when executing this command.**"
        elif isinstance(error, commands.PrivateMessageOnly):
            message = "**❌ This command only works in DMs.**"
        elif isinstance(error, commands.NoPrivateMessage):
            message = "**❌ This command only works outside of DMs.**"
        elif isinstance(error, commands.TooManyArguments):
            message = "**❌ Looks like you used too many arguments, try again.**"
        elif isinstance(error, commands.NotOwner):
            message = "**❌ You are not the owner, dont try to do this ;)**"
        elif isinstance(error, commands.ChannelNotFound):
            message = "**❌ I am sorry, i cant find the chanel you are looking for.**"
        elif isinstance(error, commands.ExtensionError):
            message = "**❌ I am sorry, it looks like there is an error with the extension where this command i located.**"  
        else:
            message = "**❌ Sorry, something unexpected has happened.**"

        embed = nextcord.Embed(
                title="**Error**",
                description=message,
                colour=nextcord.Colour.red()
            )

        await ctx.send(embed=embed, delete_after=5)
        await ctx.message.delete(delay=5)

def setup(bot):
    bot.add_cog(Error_handler(bot))
