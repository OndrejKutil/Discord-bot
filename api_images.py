import nextcord
from nextcord.ext import commands
import requests


class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Duck picks")
    async def duck(self, ctx):
        embed5 = nextcord.Embed(
            title = "Cute duck picture",
            colour = nextcord.Colour.orange()
        )
        duck_response = requests.get("https://random-d.uk/api/random")
        print(f"duck response: {duck_response}")

        duck = duck_response.json()
        duck_img = (duck["url"])
        embed5.set_image(url=str(duck_img))
        await ctx.send(embed=embed5)
        print("Command -- api_images.py -- duck")
        
        


    @commands.command(description="Fox picks")
    async def fox(self, ctx):
        embed6 = nextcord.Embed(
            title = "cute little fox",
            colour = nextcord.Colour.orange()
        )
        fox_response = requests.get("https://randomfox.ca/floof")
        print(f"fox response: {fox_response}")

        fox = fox_response.json()
        fox_img = (fox["image"])
        embed6.set_image(url=str(fox_img))
        await ctx.send(embed=embed6)
        print("Command -- api_images.py -- fox")
       


    @commands.command()
    async def joke(self, ctx):
        embed8 = nextcord.Embed(
            title = "Joke",
            colour = nextcord.Colour.dark_gray()
        )
        dark_joke_response = requests.get("https://v2.jokeapi.dev/joke/Dark?blacklistFlags=religious,political,explicit&type=single")
        print(f"joke response: {dark_joke_response}")
        
        joke_json = dark_joke_response.json()
        joke_text = joke_json["joke"]
        cathegory = joke_json["category"]

        embed8.add_field(name=cathegory, value=joke_text, inline=False)
        await ctx.send(embed=embed8)
        print("Command -- api_images.py -- joke")

        


    @commands.command(description="Pands picks")
    async def panda(self, ctx):
        embed9 = nextcord.Embed(
            title = "Red panda",
            colour = nextcord.Colour.green()
        )
        panda_response = requests.get("https://some-random-api.ml/img/red_panda")
        print(f"panda response {panda_response}")

        panda_json = panda_response.json()
        panda_img = panda_json["link"]

        embed9.set_image(url=str(panda_img))
        await ctx.send(embed=embed9)
        print("Command -- api_images.py -- panda")



def setup(bot):
    bot.add_cog(Media(bot))
