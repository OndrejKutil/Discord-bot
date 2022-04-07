import nextcord
from nextcord.ext import commands
import requests

class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def color(self, ctx, r:str, g:str, b:str):
        rgb = f"{r}, {g}, {b}"

        url = f"https://www.thecolorapi.com/id?rgb={r},{g},{b}&format=json"
        response = requests.get(url=url)
        data = response.json()
        
        hex = data["hex"]["value"]
        hsl = data["hsl"]["value"]
        hsv = data["hsv"]["value"]
        name = data["name"]["value"]
        cmyk = data["cmyk"]["value"]
        xyz = data["XYZ"]["value"]

        emb = nextcord.Embed(
            title= f"{name}",
            colour=nextcord.Colour.from_rgb(int(r), int(g), int(b))
        )
        
        emb.add_field(name="Hex", value=f"{hex}")
        emb.add_field(name="RGB", value=f"{rgb}")
        emb.add_field(name="HSL", value=f"{hsl}")
        emb.add_field(name="HSV", value=f"{hsv}")
        emb.add_field(name="CMYK", value=f"{cmyk}")
        emb.add_field(name="XYZ", value=f"{xyz}")

        await ctx.send(embed=emb)
        print("Command -- colour.py -- color")





def setup(bot):
    bot.add_cog(Colour(bot))