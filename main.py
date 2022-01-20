from audioop import reverse
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import urllib
from urllib.request import Request, urlopen
import urllib.request 
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents = intents)

@bot.event
async def on_ready():
    print("Initialized bot!")

@bot.command()
async def p(ctx):
    link = str(ctx.message.content).split(' ')[1]

    url : str
    videoId = ""
    if (link.startswith("https://www.youtube.com/")):
       

        curChar = 'a'

        i = len(link) - 1

        while (curChar != '='):
            curChar = link[i]
            i -= 1
            videoId += curChar
    videoId = videoId[::-1]
    videoId = videoId[1:]
    print(videoId)
    
    url = "https://www.yt-download.org/api/button/mp3/" + videoId

    print(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = str(urlopen(req, timeout=10).read())

    index = webpage.rfind('https://www.yt-download.org')
    
    url = ""
    curChar = ' '
    while (curChar != '"'):
        curChar = webpage[index]
        url += curChar
        index += 1

    url = url[:-1]
    
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('music.mp3')
    player = voice.play(source)


def main():
    f = open("token.tok")
    bot.run(f.read())

if __name__ == '__main__':
    main()