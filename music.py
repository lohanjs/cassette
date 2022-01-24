import asyncio
import os
import discord
from discord.ext import commands
from discord.ext.commands.core import command
from pytube import *
from random import shuffle

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.shuffled = False
        self.now_playing = ""
        self.music_queue = []
        self.vc = ""
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.id == self.bot.user.id:
            return
        elif before.channel is None:
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if self.is_playing:
                    time = 0
                if time == 300:
                    await self.vc.disconnect()
                if not self.vc.is_connected():
                    break

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            source = self.music_queue[0][0]
            self.now_playing = self.music_queue[0][1]
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            source = self.music_queue[0][0]
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][2].connect()
            else:
                await self.vc.move_to(self.music_queue[0][2])
            self.now_playing = self.music_queue[0][1]
            await ctx.send(f"Now Playing: {self.music_queue[0][1]}")
            self.vc.play(discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
            self.music_queue.pop(0)
        else:
            self.is_playing = False

    @commands.command(name = "play", help = "Searches or plays link")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a Voice Channel")
        else:
            if "youtube.com/playlist" in query:
                playlist = Playlist(query)
                furl = playlist.video_urls[0]
                fytobject = YouTube(furl)
                fytsource = fytobject.streams.get_audio_only().url
                fyttitle = fytobject.title
                self.music_queue.append([fytsource, fyttitle, voice_channel]) 
                message = await ctx.send(f"{fyttitle} Added to the Queue, Added 1/{len(playlist.video_urls)}")
                if self.is_playing == False:
                    await self.play_music(ctx)
                for i in range(1, len(playlist.video_urls)):
                    url = playlist.video_urls[i]
                    ytobject = YouTube(url)
                    ytsource = ytobject.streams.get_audio_only().url
                    yttitle = ytobject.title
                    self.music_queue.append([ytsource, yttitle, voice_channel])
                    await message.edit(content = f"{fyttitle} Added to the Queue, Added {i+1}/{len(playlist.video_urls)}")
            elif ("youtube.com/watch" in query) or ("youtu.be/" in query) or ("youtube.com/shorts" in query):
                ytobject = YouTube(str(query))
                ytsource = ytobject.streams.get_audio_only().url
                yttitle = ytobject.title
                await ctx.send(f"{yttitle} Added to the Queue")
                self.music_queue.append([ytsource, yttitle, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)
            else:
                searchobject = Search(query)
                searchresults = ""
                for i in range(0, 10):
                    searchresults += f"{i+1}  -  {searchobject.results[i].title}\n"
                message = await ctx.send(searchresults)
                def check(reply):
                    return reply.content.startswith("!") and reply.author == ctx.author and reply.channel == ctx.channel
                rchoice = await bot.wait_for("message", check = check, timeout = 15)
                choice = int(rchoice.content[1:])
                ytsource = searchobject.results[choice-1].streams.get_audio_only().url
                yttitle = searchobject.results[choice-1].title
                self.music_queue.append([ytsource, yttitle, voice_channel])
                await message.edit(content = f"{yttitle} Added to the Queue")
                if self.is_playing == False:
                    await self.play_music(ctx)
            if self.shuffled == True:
                shuffle(self.music_queue)
    
    @commands.command(name = "stream", help = "Streams audio from live stream URL")
    async def stream(self, ctx, url):
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a Voice Channel")
        else:
            await ctx.send(f"{url} Added to the Queue")
            self.music_queue.append([url, url, voice_channel])
            if self.is_playing == False:
                await self.play_music(ctx)
        if self.shuffled == True:
                shuffle(self.music_queue)
    
    @commands.command(name = "shuffle", help = "Shuffles queue until disabled")
    async def shuffle(self, ctx):
        if self.shuffled == False:
            shuffle(self.music_queue)
            self.shuffled = True
            await ctx.send("Shuffle Enabled")
        else:
            self.shuffled = False
            await ctx.send("Shuffle Disabled")

    @commands.command(name = "now", help = "Shows current song")
    async def now(self, ctx):
        if self.is_playing == False:
            await ctx.send(f"Not Playing")
        else:
            await ctx.send(f"Now Playing: {self.now_playing}")
    
    @commands.command(name = "queue", help = "Shows queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"{i+1}  -  {self.music_queue[i][1]}\n"
        if retval != "":
            await ctx.send(f"Now Playing: {self.now_playing}\n{retval}")
        else:
            if self.is_playing == True:
                await ctx.send(f"Now Playing: {self.now_playing}\nQueue Empty")
            elif self.is_playing == False:
                await ctx.send("Not Playing and Queue Empty")

    @commands.command(name = "skip", help = "Skips current song")
    async def skip(self, ctx):
        await ctx.send("Current Song Skipped")
        self.vc.stop()
        await self.play_music(ctx)    

    @commands.command(name = "skipto", help = "Skips to selected index in queue")
    async def skipto(self, ctx, *args):
        num = "".join(*args)
        if self.vc != "" and self.vc:
            if int(num) == 1:
                await ctx.send("Current Song Skipped")
                self.vc.stop()
                await self.play_music(ctx)
            elif int(num) >= 1:
                await ctx.send(f"Skipped {num} Songs")
                self.vc.stop()
                del self.music_queue[0:(int(num)-1)]
                await self.play_music(ctx)
            else:
                await ctx.send("Current Song Skipped")
                self.vc.stop()
                await self.play_music(ctx)                
   
    @commands.command(name = "remove", help = "Removes song from queue at selected index")
    async def remove(self, ctx, *args):
        i = "".join(*args)
        await ctx.send(f"{self.music_queue[i][1]} Removed from the Queue")
        self.music_queue.pop(i)
    
    @commands.command(name = "pause", help = "Pauses music")
    async def pause(self, ctx):       
        self.vc.pause()
        await ctx.send("Paused Music")
                 
    @commands.command(name = "resume", help = "Resumes music")
    async def resume(self, ctx):
        self.vc.resume()
        await ctx.send("Resumed Music")
        
    @commands.command(name = "stop", help = "Stops music and clears queue")
    async def stop(self, ctx):
        self.vc.stop()
        self.music_queue = []
        self.shuffled = False
        await ctx.send("Music Stopped and Queue Cleared")

    @commands.command(name = "leave", help = "Stops music, clears queue and leaves")
    async def leave(self, ctx):
        if self.vc.is_connected():
            self.vc.stop()
            self.music_queue = []
            await ctx.send("Leaving Voice Channel")
            await self.vc.disconnect(force=True)

bot = commands.Bot(command_prefix = "!", case_insensitive=True)
bot.add_cog(Music(bot))

@bot.command(name = "ping", help = "Shows bot latency")
async def ping(ctx):
    await ctx.send(f"Latency: {round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
    print("Bot Online")
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "Music | !help"))

bot.run(os.getenv("TOKEN"))
