import nextcord
from nextcord.ext import commands
import random
import requests


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="random choice from two arguments")
    async def coinflip(self, ctx, *a):
        embed14 = nextcord.Embed(
            title = "Coin flip",
            colour = ctx.author.colour
        )   
        result = random.choice(a)
        print(a)
        
        embed14.set_thumbnail(url="https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")
        embed14.add_field(name="Flip result", value=result)
        await ctx.send(embed=embed14)
        print("Command -- Fun.py -- coinflip")

    
    @commands.command(description="sends users avatar")
    async def avatar(self, ctx, user: nextcord.Member=None):
        if not user:
            user = ctx.message.author
        embed = nextcord.Embed(

        )
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"{user}s avatar")
        await ctx.send(embed=embed)
        print("Command -- Fun.py -- avatar")



    @commands.command(description="Sends dm to tagged user")
    async def dm(self, ctx, user: nextcord.User, *, message=None):
        message = message or "No message provided"
        from_user = ctx.author
        
        final = f"[{message}] from {from_user}"
        await user.send(final)
        print("Command -- Fun.py -- dm")


    @commands.command()
    async def urban(self, ctx, *word: str):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querystring = {"term":f"{word}"}

        headers = {
            'x-rapidapi-host': "DONT HAVE TO KNOW THIS",
            'x-rapidapi-key': "AND THIS TOO"
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
        print(f"Command -- Fun.py -- urban -- {word0}")

   

def setup(bot):
    bot.add_cog(Fun(bot))
