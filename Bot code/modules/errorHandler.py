import nextcord
from nextcord.ext import commands
import logging

#? Look into various errors, it trows CommandError most of the time (kinda obvious)

class Error_handler(commands.Cog):
    def __init__(self, bot):
        """Initialize the error handler with the bot instance and predefined error messages."""
        self.bot = bot
        self.error_messages = {
            commands.CommandNotFound: "❌ Sorry, this command does not exist.",
            commands.CommandOnCooldown: "❌ This command is on cooldown.",
            commands.MissingPermissions: "❌ You do not have the permissions to use this command.",
            commands.UserInputError: "❌ You used wrong input, try again.",
            commands.DisabledCommand: "❌ Sorry, {ctx.command} is disabled.",
            commands.MissingRequiredArgument: "❌ You missed some argument, try again.",
            commands.PrivateMessageOnly: "❌ This command only works in DMs.",
            commands.NoPrivateMessage: "❌ This command only works outside of DMs.",
            commands.TooManyArguments: "❌ Looks like you used too many arguments, try again.",
            commands.NotOwner: "❌ You are not the owner, don't try to do this ;).",
            commands.ChannelNotFound: "❌ I am sorry, I can't find the channel you are looking for.",
            commands.ExtensionError: "❌ I am sorry, it looks like there is an error with the extension where this command is located.",
            commands.BotMissingPermissions: "❌ I do not have the required permissions to execute this command.",
            commands.CommandError: "❌ Sorry, something went wrong when executing this command."
        }
        self.error_messages.update({
            commands.BadArgument: "❌ One of the arguments you provided is invalid.",
            commands.BadUnionArgument: "❌ One of the arguments you provided does not match the expected type.",
            commands.CheckFailure: "❌ You do not meet the requirements to use this command.",
            commands.CommandInvokeError: "❌ An error occurred while invoking the command.",
            commands.ConversionError: "❌ There was an error converting one of the arguments.",
            commands.MaxConcurrencyReached: "❌ This command is being used too frequently, please try again later."
        })

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Handle errors raised during command execution and send an appropriate error message."""
        logging.error(f"Error in command {ctx.command}: {error} (type: {type(error).__name__})")

        message = self.error_messages.get(type(error), "❌ Sorry, something unexpected has happened.")
        if isinstance(error, commands.DisabledCommand):
            message = message.format(ctx=ctx)

        # Handle specific errors that require additional context or formatting
        if isinstance(error, commands.CommandInvokeError):
            original = getattr(error, 'original', None)
            if original:
                logging.error(f"Original exception: {original} (type: {type(original).__name__})")

        embed = nextcord.Embed(
                title="**Error**",
                description=message,
                colour=nextcord.Colour.red()
            )

        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)

def setup(bot):
    """Add the error handler cog to the bot."""
    bot.add_cog(Error_handler(bot))
