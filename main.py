from dotenv import load_dotenv
import requests
import discord
import random
import re
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
        mensage_content = message.content.split(' ')
        command = mensage_content[0].lower()

        if command == '!source':
            embed = discord.Embed(title="Source Code: https://github.com/FidyBack/gpt-chatbot", color=0x00ff00)
            await message.channel.send(embed=embed)
        
        if command == '!author':
            embed = discord.Embed(title="Author", color=0x00ff00)
            title, content = ['Credits', 'E-mail'], ['Abel Cavalcante', 'abelcan@al.insper.edu.br']
            for index, value in enumerate(title):
                embed.add_field(name=value, value=content[index], inline=False)
            
            await message.channel.send(embed=embed)

        if command == '!run':
            embed = discord.Embed(title="What's your Pokemon?", color=0x00ff00)

            if len(mensage_content) > 1:
                pokemon_name = re.sub(r'\W+', '', mensage_content[1].lower())
                poke_request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
            else:
                pokemon_id = random.randint(1, 1010)
                poke_request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
            
            if poke_request.status_code == 200:
                pokemon_data = poke_request.json()
            
                title = ['', 'Type', 'Photo']
                types = [type['type']['name'].capitalize() for type in pokemon_data['types']]
                content = [pokemon_data['name'].capitalize(), ', '.join(types), pokemon_data['sprites']['front_default']]
                for index, value in enumerate(title):
                    if value != 'Photo':
                        embed.add_field(name=value, value=content[index], inline=False)
                    else:
                        embed.set_image(url=content[index])
            else:
                embed = discord.Embed(title="Pokemon not found!", color=0x00ff00)

            await message.channel.send(embed=embed)


        if message.content.lower() == '!help':
            embed = discord.Embed(title="Help", color=0x00ff00)
            title = ['!source', '!author', '!run', '!run <pokemon_name>']
            content = ['Show the source code of this bot', 'Show the author of this bot', 'Shows a random pokemon and its type', 'Shows the pokemon and its type']
            for index, value in enumerate(title):
                embed.add_field(name=value, value=content[index], inline=False)
            
            await message.channel.send(embed=embed)


client.run(TOKEN)