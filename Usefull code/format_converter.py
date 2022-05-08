import nextcord
from nextcord.ext import commands
from functions.format_converters_func import FormatConverters


class IntTo(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None


    @nextcord.ui.button(label="BIN", style=nextcord.ButtonStyle.blurple)
    async def send_bin(self, button : nextcord.ui.button, interaction : nextcord.Interaction):
        self.value = 1
        self.stop()


    @nextcord.ui.button(label="HEX", style=nextcord.ButtonStyle.blurple)
    async def send_hex(self, button : nextcord.ui.button, interaction : nextcord.Interaction):
        self.value = 2
        self.stop()

    
    @nextcord.ui.button(label="OCT", style=nextcord.ButtonStyle.blurple)
    async def send_oct(self, button : nextcord.ui.button, interaction : nextcord.Interaction):
        self.value = 3
        self.stop()


class formatConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def numto(self, ctx, number : int):
        emb = nextcord.Embed(
            title="Converting number to?",
            color=nextcord.Color.blurple()
        )
        
        view = IntTo()

        await ctx.send(embed=emb, view=view)

        await view.wait()

        if view.value == 1:
            emb1 = nextcord.Embed(
            title="Number to binary",
            color=nextcord.Color.blurple()
            )
            emb1.add_field(name="Result: ", value=f"**{FormatConverters.int_to_bin(number)}**")
            
            await ctx.reply(embed=emb1)
        elif view.value == 2:
            emb1 = nextcord.Embed(
            title="Number to hexadecimal",
            color=nextcord.Color.blurple()
            )
            emb1.add_field(name="Result: ", value=f"**{FormatConverters.int_to_hex(number)}**")
            
            await ctx.reply(embed=emb1)
        elif view.value == 3:
            emb1 = nextcord.Embed(
            title="Number to oct",
            color=nextcord.Color.blurple()
            )
            emb1.add_field(name="Result: ", value=f"**{FormatConverters.int_to_oct(number)}**")
            
            await ctx.reply(embed=emb1)

        
    

def setup(bot):
    bot.add_cog(formatConverter(bot))