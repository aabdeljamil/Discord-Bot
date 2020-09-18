import discord
import asyncio

TOKEN = 'NzU2Mjg4ODYyOTEyNzc0Mjk1.X2Pq5A.i1eXmxtaU22gUzPTmmiWVM0RHOA'
GUILD = 'Sustenance'

client = discord.Client()
kickList = []
israelVariants = ['death to israel', 'fuck israel']


@client.event
async def on_message(message):
    if message.author == client.user: #don't want bot replying to itself
        return

    kickRocks = False
    inVoice = False
    # if author is in a voice channel, then conect toa  voice client so that it can play audio
    if message.author.voice:
        currentChannel = message.author.voice.channel
        inVoice = True
        '''membersInVoiceChannels = []
        for channel in message.author.guild.voice_channels:
            for member in channel.members:
                membersInVoiceChannels.append(member)'''


    # if message contains israel slander, then say the following
    if any(variant in message.content.lower() for variant in israelVariants):
            await message.channel.send('Islam will prevail!')
            if inVoice: #if author in a voice channel
                voiceClient = await currentChannel.connect()
                audioSourceGood = discord.FFmpegPCMAudio(executable="C:/Users/Abdallah/Downloads/ffmpeg-4.3.1-essentials_build/ffmpeg-4.3.1-essentials_build/bin/ffmpeg.exe", source="C:/Users/Abdallah/Downloads/ttsMP3.com_VoiceText_2020-9-18_9_33_43.mp3")
                voiceClient.play(audioSourceGood)
                while voiceClient.is_playing():
                    kickRocks = True
                await voiceClient.disconnect(force=True)

    elif 'israel' in message.content.lower():
        if len(message.author.roles) == 1:
            if message.author in kickList:
                #await message.author.kick()
                msg = str(message.author) + ' has been kicked from this server for mentioning "israel" too many times.'
                await message.channel.send(msg)
                if inVoice:
                    voiceClient = await currentChannel.connect()
                    audioSourceBad1 = discord.FFmpegPCMAudio(executable="C:/Users/Abdallah/Downloads/ffmpeg-4.3.1-essentials_build/ffmpeg-4.3.1-essentials_build/bin/ffmpeg.exe", source="C:/Users/Abdallah/Downloads/ttsMP3.com_VoiceText_2020-9-18_10_0_11.mp3")
                    voiceClient.play(audioSourceBad1)
                    while voiceClient.is_playing():
                        kickRocks = True
                    await voiceClient.disconnect(force=True)
                kickList.remove(message.author)
            else:
                kickList.append(message.author)
                msg = str(message.author) + ', do not mention that piece of garbage again. Next time you will be kicked from this server.'
                await message.channel.send(msg)
                if inVoice:
                    voiceClient = await currentChannel.connect()
                    audioSourceBad = discord.FFmpegPCMAudio(executable="C:/Users/Abdallah/Downloads/ffmpeg-4.3.1-essentials_build/ffmpeg-4.3.1-essentials_build/bin/ffmpeg.exe", source="C:/Users/Abdallah/Downloads/ttsMP3.com_VoiceText_2020-9-18_9_36_8.mp3")
                    voiceClient.play(audioSourceBad)
                    while voiceClient.is_playing():
                        kickRocks = True
                    await voiceClient.disconnect(force=True)

        else:
            if message.author in kickList:
                await message.author.move_to(None)
                msg = str(message.author) + ' has been kicked from the voice channel ' + str(currentChannel) + ' for mentioning "israel" too many times.'
                await message.channel.send(msg)
                if inVoice:
                    voiceClient = await currentChannel.connect()
                    audioSourceBad1 = discord.FFmpegPCMAudio(executable="C:/Users/Abdallah/Downloads/ffmpeg-4.3.1-essentials_build/ffmpeg-4.3.1-essentials_build/bin/ffmpeg.exe", source="C:/Users/Abdallah/Downloads/ttsMP3.com_VoiceText_2020-9-18_10_0_11.mp3")
                    voiceClient.play(audioSourceBad1)
                    while voiceClient.is_playing():
                        kickRocks = True
                    await voiceClient.disconnect(force=True)
                kickList.remove(message.author)
            else:
                kickList.append(message.author)
                msg = str(message.author) + ', do not mention that piece of garbage again. Next time you will be kicked from the voice channel.' 
                await message.channel.send(msg)
                if inVoice:
                    voiceClient = await currentChannel.connect()
                    audioSourceBad = discord.FFmpegPCMAudio(executable="C:/Users/Abdallah/Downloads/ffmpeg-4.3.1-essentials_build/ffmpeg-4.3.1-essentials_build/bin/ffmpeg.exe", source="C:/Users/Abdallah/Downloads/ttsMP3.com_VoiceText_2020-9-18_9_36_8.mp3")
                    voiceClient.play(audioSourceBad)
                    while voiceClient.is_playing():
                        kickRocks = True
                    await voiceClient.disconnect(force=True)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


client.run(TOKEN)