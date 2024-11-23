import nextcord
from nextcord.ext import commands
import requests

class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description='Gets color from rgb values')
    async def color(
        self, 
        interaction: nextcord.Interaction, 
        red: int = nextcord.SlashOption(description="Red", required=True),
        green: int = nextcord.SlashOption(description="Green", required=True),
        blue: int = nextcord.SlashOption(description="Blue", required=True)
    ) -> None:
        # Validate RGB values
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            await interaction.response.send_message("RGB values must be between 0 and 255.", ephemeral=True)
            return

        rgb = f"{red}, {green}, {blue}"
        url = f"https://www.thecolorapi.com/id?rgb={red},{green},{blue}&format=json"

        try:
            response = requests.get(url=url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            await interaction.response.send_message(f"Failed to fetch color data: {e}", ephemeral=True)
            return

        hx = data["hex"]["value"]
        hsl = data["hsl"]["value"]
        hsv = data["hsv"]["value"]
        name = data["name"]["value"]
        cmyk = data["cmyk"]["value"]
        xyz = data["XYZ"]["value"]

        emb = nextcord.Embed(
            title=f"{name}",
            colour=nextcord.Colour.from_rgb(red, green, blue)
        )
        
        emb.add_field(name="Hex", value=f"{hx}")
        emb.add_field(name="RGB", value=f"{rgb}")
        emb.add_field(name="HSL", value=f"{hsl}")
        emb.add_field(name="HSV", value=f"{hsv}")
        emb.add_field(name="CMYK", value=f"{cmyk}")
        emb.add_field(name="XYZ", value=f"{xyz}")

        await interaction.response.send_message(embed=emb)


def setup(bot):
    bot.add_cog(Colour(bot))