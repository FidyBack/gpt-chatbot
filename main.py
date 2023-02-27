from dotenv import load_dotenv
import discord
import os


if not os.path.exists('.env'):
    print('Please, create a .env file with the following content:\nTOKEN=your_token')
    exit()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print('Please, create a .env file with the following content:\nTOKEN=your_token')
    exit()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!source':
            await message.channel.send('Source Code: https://github.com/FidyBack/gpt-chatbot')
        
        if message.content.lower() == '!author':
            await message.channel.send('Author: Abel Cavalcante\nE-mail: abelcan@al.insper.edu.br')



client.run(TOKEN)