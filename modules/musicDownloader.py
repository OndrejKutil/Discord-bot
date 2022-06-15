import nextcord
from nextcord.ext import commands
import os
import youtube_dl
import passwords

class MusicDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Downloads .mp3 file from youtube url")
    async def download(self, interaction : nextcord.Interaction, link : str = nextcord.SlashOption(description="Link", required=True)):
        channel_id = interaction.channel_id
        channel = self.bot.get_channel(channel_id)
        
        video_info = youtube_dl.YoutubeDL().extract_info(url = link, download=False)
        filename = f"{video_info['title']}.mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
        }

        await interaction.response.send_message(f"Downloading - **{filename[:-4]}**")

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        await channel.send(f"**✅ Enjoy your music!**", files=[nextcord.File(f"{filename}")])

        os.remove(f"./{filename}")


def setup(bot):
    bot.add_cog(MusicDownloader(bot))
