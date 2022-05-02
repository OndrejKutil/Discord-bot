from nextcord import Interaction, SlashOption
import nextcord
from nextcord.ext import commands
import random
import requests
import passwords


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="random choice from two arguments")
    async def coinflip(
        self,
        interaction : Interaction, 
        first : str = SlashOption(description="First argument", required=True),
        second : str = SlashOption(description="Second argument", required=True)
        ):
        embed14 = nextcord.Embed(
            title = "Coin flip",
            colour = nextcord.Colour.blurple()
        )
        result_list = [first, second]
        result = random.choice(result_list)

        embed14.set_thumbnail(url="https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")
        embed14.add_field(name="Flip result", value=result)
        await interaction.response.send_message(embed=embed14)

    
    @commands.command(description="sends users avatar")
    async def avatar(self, ctx, user: nextcord.Member=None):
        if not user:
            user = ctx.message.author
        embed = nextcord.Embed(

        )
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"{user}s avatar")
        await ctx.send(embed=embed)


    @commands.command(description="Sends dm to tagged user")
    async def dm(self, ctx, user: nextcord.User, *, message=None):
        message = message or "No message provided"
        from_user = ctx.author
        
        final = f"[{message}] from {from_user}"
        await user.send(final)


    @commands.command()
    async def urban(self, ctx, *word: str):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querystring = {"term":f"{word}"}

        headers = {
            'x-rapidapi-host': f"{passwords.x-rapidapi-host_urban}",
            'x-rapidapi-key': f"{passwords.x-rapidapi-key_urban}"
            }

        data = requests.get(url=url, headers=headers, params=querystring).json()
        
        definition = data["list"][0]["definition"]
        example = data["list"][0]["example"]
        word0 = data["list"][0]["word"]
        link = data["list"][0]["permalink"]

        emb = nextcord.Embed(
            title="Urban dictionary",
            description=f"word: {word0}",
            colour=nextcord.Colour.blurple()
        )
        emb.add_field(name="Definition", value=definition)
        emb.add_field(name="Example", value=example)
        emb.set_footer(text=link)

        await ctx.send(embed=emb)

   

def setup(bot):
    bot.add_cog(Fun(bot))
