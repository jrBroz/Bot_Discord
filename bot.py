import discord
import os
import asyncio
import yt_dlp # permite baixar audio e video de varios sites
from dotenv import load_dotenv
from discord.ext import commands

def run_bot():

    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.all() # quais eventos o bot aceita 'ouvir' (mensagem, presenca de user em canal de voz, etc)

    CLIENT = discord.Client(intents=intents) 
   
    voice_clients = {}
    yt_dlp_options = {"format": "bestaudio/best"} # Pro yt_dlp pegar a melhor qualidade de audio possivel
    ytdl = yt_dlp.YoutubeDL(yt_dlp_options) 

    ffmpeg_options = {"options": "-vn"} # faz o ffmpeg tocar so o audio, ignorando o video

    @CLIENT.event
    async def on_ready():
        print(f"{CLIENT.user} O Bot está operando corretamente e pronto para ser usado.")

    
    @CLIENT.event 
    async def on_message(message):  # eventos de mensagem

        if message.content.startswith("!play"):
            try:
                voice_client = await message.author.voice.channel.connect() # Caso nao tenha ninguem no voice chat, ele nao vai entrar.
                voice_clients[voice_client.guild.id] = voice_client 

            except Exception as e:
                await channel.send('É preciso que alguém entre no canal de voz para o bot entrar.')
                print(e) 

            try:

                url = message.content.split()[1] # pega o link da mensagem,
                loop = asyncio.get_event_loop() 
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options) # bota o audio no formato PCM, que o discord exige

                voice_clients[message.guild.id].play(player)

            except Exception as e:
                print(e)

        # Para de tocar a musica
        if message.content.startswith("!stop"):
            try: 
                voice_clients[message.guild.id].stop()
            
            except Exception as e:
                print(e)

        # Tirar bot do VoiceChat
        if message.content.startswith("!exit"):
            try: 
                await voice_clients[message.guild.id].disconnect()
            
            except Exception as e:
                print(e)
            
        if message.content.startswith("!comandos"):

            channel = message.channel
            try:
                await channel.send('[1] !play => Toca musica \n [2] !stop => para a musica \n [3] !exit Tira o bot do VoiceChat')

            except Exception as e:
                print(e)                

    CLIENT.run(TOKEN)
