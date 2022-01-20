from audioop import reverse
from fileinput import filename
import discord
import os
import re
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

    url = ""
    
    if (link.startswith("https")):
        videoId = ""

        regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

        match = regex.match(link)

        videoId = match.group('id')

        print("id: " + videoId)
    
        url = "https://www.yt-download.org/api/button/mp3/" + videoId
    else:
        url = link

    print("url: " + url)
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
    
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0')
    filename, headers = opener.retrieve(url, 'music.mp3')


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
    
    #os.remove("music.mp3")

def main():
    f = open("token.tok")
    bot.run(f.read())

if __name__ == '__main__':
    main()