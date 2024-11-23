import nextcord  # Discord API wrapper for creating bots
from nextcord.ext import commands  # Extension for creating bot commands
import os  # Provides functions for interacting with the operating system
import logging  # Enables logging of errors and warnings
import json  # Provides functions for working with JSON data
import multiprocessing  # Allows for concurrent execution of processes
import datetime  # Supplies classes for manipulating dates and times
import asyncio  # Provides support for asynchronous programming
import sys  # Provides access to some variables used or maintained by the interpreter
import dotenv  # Reads key-value pairs from a .env file and adds them to the environment
import subprocess  # Allows for running subprocesses

# Load environment variables from .env file
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

# Logging the errors and warnings in the nextcord.log file.
logger = logging.getLogger(__name__)
logging.basicConfig(filename="nextcord.log", encoding="utf-8", level=logging.WARNING, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
# Example usage of logging for debugging:
# logger.warning("This is a warning message")
# logger.error("This is an error message")


def get_prefix(bot: commands.Bot, message: nextcord.Message) -> str:
    """Retrieve the command prefix for the bot based on the guild ID."""
    try:
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)
        return prefixes.get(str(message.guild.id), "!")
    except FileNotFoundError:
        logger.error("prefixes.json file not found.")
        return "!"
    except json.JSONDecodeError:
        logger.error("Error decoding prefixes.json.")
        return "!"



# defines the bot object
bot = commands.Bot(command_prefix=get_prefix, intents=nextcord.Intents().all(), activity=nextcord.Activity(name="/help", type=0), status=nextcord.Status.online)


# what bot does when it gets ready (starts)
@bot.event
async def on_ready() -> None:
    """Event handler for when the bot is ready."""
    print(f"Running \nID - {bot.user.id}\nTime - {datetime.datetime.now()}")    
    proc = multiprocessing.current_process()
    try:
        with open("./pidjson.json", "w") as f:
            data = {"pid": proc.pid}
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to write pidjson.json: {e}")


@bot.event
async def on_member_join(member: nextcord.Member) -> None:
    """Event handler for when a new member joins a guild."""
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'**👋 Welcome {member.mention} to {guild.name}!**'
        await guild.system_channel.send(to_send)
    else:
        logger.warning("No system channel found in the guild.")
        raise commands.CommandError("**No system channel**")


@bot.event
async def on_guild_join(guild: nextcord.Guild) -> None:
    """Event handler for when the bot joins a new guild."""
    try:
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "!"
        with open("./prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to update prefixes.json on guild join: {e}")


@bot.event
async def on_guild_remove(guild: nextcord.Guild) -> None:
    """Event handler for when the bot is removed from a guild."""
    try:
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id), None)
        with open("./prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to update prefixes.json on guild remove: {e}")


@bot.command()
async def prefix(ctx: commands.Context, new_prefix: str = None) -> None:
    """Command to get or set the command prefix for the bot."""
    try:
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)
        if new_prefix:
            prefixes[str(ctx.guild.id)] = new_prefix
            with open("./prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)
            await ctx.send(f"✅ Changed prefix to **'{new_prefix}'**")
        else:
            await ctx.send(f"Current prefix is: **'{prefixes.get(str(ctx.guild.id), '!')}'**")
    except Exception as e:
        logger.error(f"Failed to update or read prefixes.json: {e}")
        await ctx.send("❌ An error occurred while updating the prefix.")


@bot.command(name="ping", description="Command for checking ping")
async def ping(ctx: commands.Context) -> None:
    """Command to check the bot's latency."""
    embed2 = nextcord.Embed(
        title=f"{round(bot.latency * 1000)}ms",
        colour=nextcord.Colour.green(),
    )
    await ctx.send(embed=embed2)


@bot.command(description="Only for owner")
@commands.is_owner()
async def load(ctx: commands.Context, extension: str) -> None:
    """Command to load a bot extension."""
    extension = "modules." + extension
    try:
        bot.load_extension(extension)
        await ctx.send(f"**✅ loaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        await ctx.send(exc)


@bot.command(description="Only for owner")
@commands.is_owner()
async def unload(ctx: commands.Context, extension: str) -> None:
    """Command to unload a bot extension."""
    extension = "modules." + extension
    try:
        bot.unload_extension(extension)
        await ctx.send(f"**✅ unloaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        await ctx.send(exc)
        

@bot.command(description="Only for owner")
@commands.is_owner()
async def reload(ctx: commands.Context, extension: str) -> None:
    """Command to reload a bot extension."""
    extension = "modules." + extension
    try:
        bot.unload_extension(extension)
        await asyncio.sleep(1)
        bot.load_extension(extension)
        await ctx.send(f"**✅ reloaded {extension} extension**")
    except Exception as e:
        exc = f"{type(e).__name__}"
        await ctx.send(exc)


@bot.command()
@commands.is_owner()
async def extensions(ctx: commands.Context) -> None:
    """Command to list all loaded bot extensions."""
    exten = ""
    for ex in bot.extensions:
        ex = ex[8:]
        exten = exten + ex + "\n"
    
    await ctx.send(exten)


@bot.command()
@commands.is_owner()
async def servers(ctx: commands.Context) -> None:
    """Command to list all servers the bot is in."""
    servers = ""
    for guildName in bot.guilds:
        servers = servers + guildName + "\n"

    await ctx.send(servers) 


@bot.command()
async def log(ctx: commands.Context) -> None:
    """Command to send the bot's log file."""
    try:
        await ctx.send(files=[nextcord.File(fp='nextcord.log', filename='nextcord.log', description="log file from bot", force_close=True)])
    except Exception as e:
        logger.error(f"Failed to send log file: {e}")
        await ctx.send("❌ An error occurred while sending the log file.")


@bot.command()
@commands.is_owner()
async def chpr(ctx: commands.Context, status: int, text: str = "/help", activity_type: int = 0) -> None:
    """Command to change the bot's presence."""
    """
    Changes the bot's presence.

    Parameters
    ----------
    status : int
        0 = online, 1 = idle, 2 = dnd, 3 = invisible
    text : str
        The text that will be displayed in the activity
    activity_type : int
        0 = Playing, 1 = Streaming, 2 = Listening, 3 = Watching, 5 = Competing in
    """
    statuses = [nextcord.Status.online, nextcord.Status.idle, nextcord.Status.dnd, nextcord.Status.invisible]
    status_texts = ["online", "idle", "do not disturb", "invisible"]

    if status in range(4):
        await bot.change_presence(status=statuses[status], activity=nextcord.Activity(name=text, type=activity_type))
        msg = await ctx.send(f"✅ Changed presence to **{status_texts[status]} - with text ({text}) - and type {activity_type}**")
        await ctx.message.delete()
        await msg.delete()
    else:
        await ctx.send("❌ Invalid status type. Use 0 for online, 1 for idle, 2 for dnd, 3 for invisible.")


# Command to view bot uptime
@bot.command()
async def uptime(ctx: commands.Context) -> None:
    """Command to view the bot's uptime."""
    current_time = datetime.datetime.now()
    uptime_duration = current_time - bot.start_time
    await ctx.send(f"🕒 Bot has been up for {uptime_duration}")


# Command to shutdown the bot
@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context) -> None:
    """Command to shutdown the bot."""
    await ctx.send("Shutting down...")
    await bot.close()


# Loading all the extensions in the modules folder.
startup_extensions = []

# Load all extensions in the modules folder
for file in os.listdir("modules"):
        if file.endswith(".py"):
            startup_extensions.append(f"modules.{file[:-3]}")

# Running the bot
if __name__ == "__main__":
    bot.start_time = datetime.datetime.now()  # Track bot start time
    for extensions in startup_extensions:
        try:
            bot.load_extension(extensions)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            logger.error(f"Failed to load extension {extensions}: {exc}")
            print(f"Failed to load extensions {extensions}\n{exc}")

    # authenticate the bot with the token
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f"Failed to run the bot: {e}")
        sys.exit(1)
