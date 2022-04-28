import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import requests

class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description='Gets color from rgb values')
    async def color(
        self, 
        interaction : Interaction, 
        red: int = SlashOption(description="Red", required=True),
        green: int = SlashOption(description="Green", required=True),
        blue: int = SlashOption(description="Blue", required=True)
        ):
        
        rgb = f"{red}, {green}, {blue}"

        url = f"https://www.thecolorapi.com/id?rgb={red},{green},{blue}&format=json"
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
            colour=nextcord.Colour.from_rgb(int(red), int(green), int(blue))
        )
        
        emb.add_field(name="Hex", value=f"{hex}")
        emb.add_field(name="RGB", value=f"{rgb}")
        emb.add_field(name="HSL", value=f"{hsl}")
        emb.add_field(name="HSV", value=f"{hsv}")
        emb.add_field(name="CMYK", value=f"{cmyk}")
        emb.add_field(name="XYZ", value=f"{xyz}")


        await interaction.response.send_message(embed=emb)


def setup(bot):
    bot.add_cog(Colour(bot))