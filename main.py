import nextcord
from nextcord.ext import commands
import os
import logging
import passwords

logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='./nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game("!help"))
    print(f"logged with token and ready!")


@bot.command(name="ping", description="Command for checking ping")
async def ping(ctx):
    embed2 = nextcord.Embed(
        title=f"{round(bot.latency * 1000)}ms",
        colour=nextcord.Colour.green(),
    )
    await ctx.send(embed=embed2)
    

@bot.command(description="Only for owner")
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        print(f"Succusfuelly loaded {extension} extension")
        ctx.send(f"loaded {extension} extensiom")
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, e)
        print("Failed to load extension {}\n{}".format(extensions, exc))
        ctx.send(f"failed to load {extension} extension")


@bot.command(description="Only for owner")
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        print(f"Succusfuelly unloaded {extension} extension")
        ctx.send(f"unloaded {extension} extensiom")
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, e)
        print("Failed to unload extension {}\n{}".format(extensions, exc))
        ctx.send(f"failed to unload {extension} extension")


@bot.command()
@commands.is_owner()
async def extensions(ctx):
    await ctx.send(f"{bot.extensions} \n")

startup_extensions = []

for file in os.listdir("./modules"):
        if file.endswith(".py"):
            startup_extensions.append(f"modules.{file[:-3]}")

if __name__ == "__main__":
    for extensions in startup_extensions:
        try:
            bot.load_extension(extensions)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extensions {}\n{}".format(extensions, exc))

    bot.run(passwords.token)
