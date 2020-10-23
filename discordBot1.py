import discord
import asyncio
import time

TOKEN = '' #deleted for security purposes
GUILD = ''

client = discord.Client()
kickList = []
cussVariants = ['fuck', 'shit', 'bitch', 'ass']#can add other cuss words


@client.event
async def on_member_join(member):
    #finds general text channel
    textChannels = member.guild.text_channels
    for channel in textChannels:
        if channel.name == 'general':
            targetChannel = channel

    #make sure bot isn't replying to itself, and welcmes a new member
    if member != client.user:
        joinMsg = member.display_name + ' has joined'
        await targetChannel.send(joinMsg)
        welcomeMsg = 'Welcome!'
        await targetChannel.send(welcomeMsg)        



@client.event
async def on_message(message):
    #checks for the reactions to a message
    def check(reaction, user):
        emoji1 = discord.utils.get(message.author.guild.emojis, name='one')
        emoji2 = discord.utils.get(message.author.guild.emojis, name='two')
        return user == message.author and str(reaction.emoji) == emoji1 or emoji2

    if message.author == client.user: #don't want bot replying to itself
        return

    inVoice = False
    # if author is in a voice channel, then conect toa  voice client so that it can play audio
    if message.author.voice:
        currentChannel = message.author.voice.channel
        inVoice = True
        #following code might be useful later but not currently used
        membersInVoiceChannels = []
        for channel in message.author.guild.voice_channels:
            for member in channel.members:
                membersInVoiceChannels.append(member)
        allMembers = message.author.guild.members        


    # if message contains apology to bot then forgive user
    if ('sorry' or 'apologi') and 'lster' in message.content.lower():
        if message.author in kickList:
            kickList.remove(message.author)
        await message.channel.send("Don't repeat it!")
        if inVoice: #if author in a voice channel
            voiceClient = await currentChannel.connect()
            audioSourceGood = discord.FFmpegPCMAudio(source='someAudioThatForgivesUser.mp3')
            voiceClient.play(audioSourceGood)
            while voiceClient.is_playing():
                pass
            await voiceClient.disconnect(force=True)


    #user cusses
    elif any(variant in message.content.lower() for variant in cussVariants):
        if len(message.author.roles) == 1:#no roles
            if message.author in kickList:
                await message.author.kick()
                msg = str(message.author) + ' has been kicked from this server for cussing too many times.'
                await message.channel.send(msg)
                if inVoice:#if author in a voice channel
                    voiceClient = await currentChannel.connect()
                    audioSourceBad = discord.FFmpegPCMAudio(source='someAudioThatTellsUsersNotToCuss.mp3')
                    voiceClient.play(audioSourceBad)
                    while voiceClient.is_playing():
                        pass
                    await voiceClient.disconnect(force=True)
                kickList.remove(message.author)#if user is added back, their chance gets reset
            else:
                kickList.append(message.author)
                msg = str(message.author) + ", don't cuss!"
                await message.channel.send(msg)
                if inVoice:#if author in a voice channel
                    voiceClient = await currentChannel.connect()
                    audioSourceBad = discord.FFmpegPCMAudio(source='someAudioThatTellsUsersNotToCuss.mp3')
                    voiceClient.play(audioSourceBad)
                    while voiceClient.is_playing():
                        pass
                    await voiceClient.disconnect(force=True)


        else:#user has at least one role, can't kick out of server
            if message.author in kickList and inVoice:
                await message.author.move_to(None)
                msg = str(message.author) + ' has been kicked from the voice channel ' + str(currentChannel) + ' for cussing too many times.'
                await message.channel.send(msg)
                if inVoice:#if author in a voice channel
                    voiceClient = await currentChannel.connect()
                    audioSourceBad = discord.FFmpegPCMAudio(source='someAudioThatTellsUsersNotToCuss.mp3')
                    voiceClient.play(audioSourceBad)
                    while voiceClient.is_playing():
                        pass
                    await voiceClient.disconnect(force=True)
                kickList.remove(message.author)
            elif inVoice:
                kickList.append(message.author)
                msg = str(message.author) + ", don't cuss!"
                await message.channel.send(msg)
                if inVoice:#if author in a voice channel
                    voiceClient = await currentChannel.connect()
                    audioSourceBad = discord.FFmpegPCMAudio(source='someAudioThatTellsUsersNotToCuss.mp3')
                    voiceClient.play(audioSourceBad)
                    while voiceClient.is_playing():
                        pass
                    await voiceClient.disconnect(force=True)
            else:
                msg = str(message.author) + ", don't cuss!"
                await message.channel.send(msg)


    elif message.content.lower() == 'hello' or 'hi':
        msg = 'Hi there!'
        await message.channel.send(msg)
        if inVoice:#if author in a voice channel
            voiceClient = await currentChannel.connect()
            audioSourceGreet = discord.FFmpegPCMAudio(source='someAudioThatGreetsUser.mp3')
            voiceClient.play(audioSourceGreet)
            while voiceClient.is_playing():
                await message.channel.send('\nSend "bye" to disconnect me from voice channel')
                try:
                    msg = await client.wait_for('message', check=lambda message: message.content == 'leave', timeout=None)#edit this line to change the parameter, 'timeout', to equal the length of the audio
                except asyncio.TimeoutError:
                    pass
                if msg:
                    await voiceClient.disconnect(force=True)
            await voiceClient.disconnect(force=True)
   

    elif message.content.lower() == 'kick user':
        oneReactions = 0
        twoReactions = 0
        t_end = time.time() + 30
        msg = 'Which user would you like to vote on kicking? Enter either the nickname or the username + #. For example, "john#0000".'
        await message.channel.send(msg)
        try:
            msg1 = await client.wait_for('message', timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send('You took too long to respond')    
        userToKick = msg1.content
        memberToKick = message.author.guild.get_member_named(userToKick)#user and member aren't the same thing, kick() needs member
        if memberToKick not in allMembers:
            await message.channel.send("User doesn't exist")
            return
        await message.channel.send('Vote on kicking ' + userToKick + ' by reacting with the corresponding emoji:' + "\n\n:one:  Kick (5 votes needed)\n:two:  Don't Kick\n\nVoting will end in 30 seconds")

        while time.time() < t_end:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=35.0, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                emoji1 = discord.utils.get(message.author.guild.emojis, name='one')
                emoji2 = discord.utils.get(message.author.guild.emojis, name='two')
                if str(reaction.emoji) == emoji1:
                    oneReactions += 1
                elif str(reaction.emoji) == emoji2:
                    twoReactions += 1    
       
        await message.channel.send('Voting has ended')
        if oneReactions > twoReactions and oneReactions > 4:
            await memberToKick.kick()
            await message.channel.send('User ' + userToKick + ' has been kicked out of the server.')
            if inVoice:#if author in a voice channel
                voiceClient = await currentChannel.connect()
                audioSourceBad1 = discord.FFmpegPCMAudio(source='lB.mp3')
                voiceClient.play(audioSourceBad1)
                while voiceClient.is_playing():
                    pass
                await voiceClient.disconnect(force=True)

        else:
            await message.channel.send('User ' + userToKick + ' will not be kicked out of the server.')

       
    elif message.content == 'is lster admin':#check if bot has admin privelages
        bot = message.author.guild.get_member_named('lster#8890')
        perm = bot.guild_permissions
        if perm.administrator == True:
            await message.channel.send('Yes')
        else:
            await message.channel.send('No')



       
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(client.user, 'connected to guild ', guild.name, '#', guild.id)

client.run(TOKEN)
