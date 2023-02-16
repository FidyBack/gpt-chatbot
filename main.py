import discord
import random

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em mensagem privada!')
    else:
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em um canal público!')

    # brooklyn_99_quotes = [
    #     'I\'m the human form of the 💯 emoji.',
    #     'Bingpot!',
    #     (
    #         'Cool. Cool cool cool cool cool cool cool, '
    #         'no doubt no doubt no doubt no doubt.'
    #     ),
    # ]

    # if message.content == '99!':
    #     response = random.choice(brooklyn_99_quotes)
    #     await message.channel.send(response)


client.run('MTA3NTIyNDE1NDM4ODgzMjI4OA.GI5FfB.rMEGGaB3sR1g4pkiG02YEclG22WH8Tm1h-eBvA')