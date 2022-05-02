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

bot = commands.Bot(command_prefix="!", intents=intents, activity=nextcord.Activity(name="!Help", type=3), status=nextcord.Status.online)

@bot.event
async def on_ready():
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


@bot.command()
@commands.is_owner()
async def chpr(ctx, type : int, text : str = None, type_type : int = None):
    if type == 0 and text == None and type_type == None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name="!Help", type=3))
    if type == 0 and text == None and type_type != None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name="!Help", type=type_type))
    elif type == 0 and text != None and type_type == None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name=f"{text}", type=3))
    elif type == 0 and text != None and type_type != None:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(name=f"{text}", type=type_type))
    elif type == 1 and text == None:
        await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(name="Working on bot", type=0))
    elif type == 1 and text != None:
        await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(name=f"{text}", type=0))
    elif type == 2 and text == None:
        await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name="Maintenance", type=0))
    elif type == 2 and text != None:
        await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name=f"{text}", type=0))
    elif type == 3:
        await bot.change_presence(status=nextcord.Status.invisible)
    elif type == 4:
        await bot.change_presence(status=nextcord.Status.offline)

    await ctx.send(f"Changed presence to [{type} - with text ({text}) - and type {type_type}]")


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
