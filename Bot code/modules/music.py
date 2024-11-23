import asyncio
import nextcord
import yt_dlp
from nextcord.ext import commands
import random

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source: nextcord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5) -> None:
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')


    @classmethod
    async def from_url(cls, url: str, *, loop: asyncio.AbstractEventLoop = None, stream: bool = False) -> 'YTDLSource':
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.queue = []
        self.current_song = None
        self.loop = False
        self.current_volume = 0.5  # Default volume
        self.history = []


    @commands.command(description="joins a voice channel")
    async def join(self, ctx: commands.Context) -> None:
        """Joins a voice channel."""
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.reply("**❌ You need to be in a voice channel to use this command!**")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)


    @commands.command(description="streams music")
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        """Streams music from a URL."""
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.queue.append(player)
            
            if len(self.queue) == 1 and not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await self.play_next(ctx)
            else:
                await ctx.send(f'**Enqueued:** {player.title}')


    @commands.command(description="skips to the next song in queue")
    async def skip(self, ctx: commands.Context) -> None:
        """Skips to the next song in the queue."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.reply("**❌ There is no song currently playing.**")
        
        ctx.voice_client.stop()
        await ctx.reply("**⏭️ Skipped to the next song.**")


    @commands.command(description="clears the current queue")
    async def dump(self, ctx: commands.Context) -> None:
        """Clears the current queue."""
        self.queue.clear()
        await ctx.reply("**🗑️ Cleared the queue.**")


    @commands.command(description="shows the current queue")
    async def queue(self, ctx: commands.Context) -> None:
        """Shows the current queue."""
        if not self.queue:
            return await ctx.reply("**❌ The queue is empty.**")
        
        queue_list = "\n".join([f"{index + 1}. {song.title}" for index, song in enumerate(self.queue)])
        await ctx.reply(f"**🎶 Current queue:**\n{queue_list}")


    @commands.command(description="removes a song from the queue by its index")
    async def remove(self, ctx: commands.Context, index: int) -> None:
        """Removes a song from the queue by its index."""
        if index < 1 or index > len(self.queue):
            return await ctx.reply("**❌ Invalid index.**")
        
        removed_song = self.queue.pop(index - 1)
        await ctx.reply(f"**🗑️ Removed:** {removed_song.title}")


    @commands.command(description="switches two songs in the queue by their indices")
    async def switch(self, ctx: commands.Context, index1: int, index2: int) -> None:
        """Switches two songs in the queue by their indices."""
        if index1 < 1 or index1 > len(self.queue) or index2 < 1 or index2 > len(self.queue):
            return await ctx.reply("**❌ Invalid indices.**")
        
        self.queue[index1 - 1], self.queue[index2 - 1] = self.queue[index2 - 1], self.queue[index1 - 1]
        await ctx.reply(f"**🔄 Switched songs at positions {index1} and {index2}.**")


    @commands.command(description="loops the current song or the entire queue")
    async def loop(self, ctx: commands.Context, mode: str = 'song') -> None:
        """Loops the current song or the entire queue."""
        if mode not in ['song', 'queue']:
            return await ctx.reply("**❌ Invalid mode. Use 'song' or 'queue'.**")
        
        self.loop = mode
        await ctx.reply(f"**🔁 Looping {mode}.**")


    async def play_next(self, ctx: commands.Context) -> None:
        """Plays the next song in the queue."""
        if self.queue:
            if self.loop == 'song' and self.current_song:
                self.queue.insert(0, self.current_song)
            elif self.loop == 'queue':
                self.queue.append(self.current_song)
            self.current_song = self.queue.pop(0)
            self.history.append(self.current_song.title)
            if len(self.history) > 10:
                self.history.pop(0)
            try:
                ctx.voice_client.play(self.current_song, after=lambda e: self.bot.loop.is_running() and self.bot.loop.create_task(self.play_next(ctx) if self.queue else self.on_queue_end(ctx)))
                await ctx.send(f'**Now playing:** {self.current_song.title}')
            except Exception as e:
                await ctx.send(f"**❌ An error occurred while playing the song: {str(e)}**")
                if self.bot.loop.is_running():
                    self.bot.loop.create_task(self.play_next(ctx))
        else:
            self.current_song = None


    @commands.command(description="shuffles the songs in the queue")
    async def shuffle(self, ctx: commands.Context) -> None:
        """Shuffles the songs in the queue."""
        if not self.queue:
            return await ctx.reply("**❌ The queue is empty.**")
        
        random.shuffle(self.queue)
        await ctx.reply("**🔀 Shuffled the queue.**")


    @commands.command(description="seeks to a specific time in the current song")
    async def jump(self, ctx: commands.Context, seconds: int) -> None:
        """Seeks to a specific time in the current song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.reply("**❌ There is no song currently playing.**")
        
        ctx.voice_client.pause()
        new_source = nextcord.FFmpegPCMAudio(self.current_song.url, **ffmpeg_options, before_options=f"-ss {seconds}")
        ctx.voice_client.source = nextcord.PCMVolumeTransformer(new_source, volume=self.current_volume)
        ctx.voice_client.resume()
        await ctx.reply(f"**⏩ Jumped to {seconds} seconds.**")


    @commands.command(description="fetches and displays the lyrics of the current song")
    async def lyrics(self, ctx: commands.Context) -> None:
        """Fetches and displays the lyrics of the current song."""
        if self.current_song is None:
            return await ctx.reply("**❌ No song is currently playing.**")
        

        #! Add your own logic to fetch lyrics
        #? Fetch lyrics using an API or web scraping (this is a placeholder)
        lyrics = "Lyrics of the song..."  # Replace with actual lyrics fetching logic
        await ctx.reply(f"**🎤 Lyrics for {self.current_song.title}:**\n{lyrics}")


    async def on_queue_end(self, ctx: commands.Context) -> None:
        """Handles the end of the queue."""
        self.current_song = None


    @commands.command(description="stops and disconnects the bot from voice")
    async def leave(self, ctx: commands.Context) -> None:
        """Stops and disconnects the bot from voice."""
        await ctx.voice_client.disconnect()
        self.queue.clear()
        self.current_song = None


    @commands.command()
    async def pause(self, ctx: commands.Context) -> None:
        """Pauses the currently playing song."""
        SongPlaying = ctx.voice_client.is_playing()
        
        Paused = ctx.voice_client.is_paused()
        
        if Paused != True:
            ctx.voice_client.pause()
            await ctx.reply("**✅ The music is now paused**")
        else:
            if SongPlaying == True:
                await ctx.reply("**❌ The music is already paused.**")
            else:
                await ctx.reply("**❌ There is no song currently playing.**")


    @commands.command()
    async def resume(self, ctx: commands.Context) -> None:
        """Resumes the currently paused song."""
        Paused = ctx.voice_client.is_paused()
        
        if Paused == True:
            ctx.voice_client.resume()
            await ctx.reply("**✅ Resumed your music**")
        else:
            await ctx.reply("**❌ The music is not paused**")


    @commands.command()
    async def volume(self, ctx: commands.Context, volume: int) -> None:
        """Changes the volume of the currently playing song."""
        if ctx.voice_client is None:
            return await ctx.reply("**❌ Not connected to a voice channel.**")

        self.current_volume = volume / 100
        ctx.voice_client.source.volume = self.current_volume
        await ctx.reply(f"**🔊 Changed volume to {volume}%**")


    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:
        """Stops the currently playing song and clears the queue."""
        ctx.voice_client.stop()
        self.queue.clear()
        self.current_song = None


    @commands.command()
    async def playing(self, ctx: commands.Context) -> None:
        """Shows the currently playing song."""
        if ctx.voice_client is None:
            return await ctx.reply("**❌ Not connected to a voice channel.**")

        if ctx.voice_client.is_playing():
            await ctx.reply(f"**🎶 Now playing: {ctx.voice_client.source.title}**")
        else:
            await ctx.reply("**❌ There is no song currently playing.**")


    @commands.command(description="shows the history of recently played songs")
    async def history(self, ctx: commands.Context) -> None:
        """Shows the history of recently played songs."""
        if not self.history:
            return await ctx.reply("**❌ The history is empty.**")
        
        history_list = "\n".join([f"{index + 1}. {song}" for index, song in enumerate(self.history)])
        await ctx.reply(f"**📜 Recently played songs:**\n{history_list}")


    @commands.command(description="clears the history of recently played songs")
    async def clear_history(self, ctx: commands.Context) -> None:
        """Clears the history of recently played songs."""
        self.history.clear()
        await ctx.reply("**🗑️ Cleared the history.**")


    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context) -> None:
        """Ensures the bot is connected to a voice channel before playing music."""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("**❌ You are not connected to a voice channel.**")
                raise commands.CommandError("❌ Author not connected to a voice channel.")
        elif not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
            ctx.voice_client.stop()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Music(bot))