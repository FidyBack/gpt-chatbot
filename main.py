from dotenv import load_dotenv
import discord
import os


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
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
            await message.channel.send('source code: https://github.com/FidyBack/gpt-chatbot')
        
        if message.content.lower() == '!author':
            await message.channel.send('author: Abel Cavalcante\nemail: abelcan@al.insper.edu.br')



client.run(TOKEN)