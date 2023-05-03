from dotenv import load_dotenv
from discord.ext import commands

import requests
import discord
import random
import re
import os

# Program initial configuration
global_database = {}

# Discord initial configuration
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# Environment configuration
if not os.path.exists('.env'):
    print('Please, create a .env file with the following content:\nTOKEN=your_token')
    exit()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print('Please, create a .env file with the following content:\nTOKEN=your_token')
    exit()


# Start message
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


# Commands
@bot.command()
async def source(message):
    """
    Show the source code of this bot.
    """
    embed = discord.Embed(title="Source Code: https://github.com/FidyBack/gpt-chatbot", color=0x00ff00)
    await message.send(embed=embed)

@bot.command()
async def author(message):
    """
    Show the author and the email of this bot.
    """
    embed = discord.Embed(title="Author", color=0x00ff00)
    title, content = ['Credits', 'E-mail'], ['Abel Cavalcante', 'abelcan@al.insper.edu.br']
    for index, value in enumerate(title):
        embed.add_field(name=value, value=content[index], inline=False)
    await message.send(embed=embed)

@bot.command()
async def run(message, pokemon_name: str = None):
    """
    Shows a pokemon and some of its characteristics.
    """
    embed = discord.Embed(title="What's your Pokemon?", color=0x00ff00)

    if pokemon_name:
        pokemon_name = re.sub(r'\W+', '', pokemon_name.lower())
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

    await message.send(embed=embed)

@bot.command()
async def help(message):
    """
    Shows a list of commands.
    """
    embed = discord.Embed(title="Help", color=0x00ff00)
    title = ['!source', '!author', '!run', '!run <pokemon_name>']
    content = [
        'Show the source code of this bot', 
        'Show the author of this bot', 
        'Shows a random pokemon and its type', 
        'Shows the selected pokemon and its type'
        ]
    for index, value in enumerate(title):
        embed.add_field(name=value, value=content[index], inline=False)
    
    await message.send(embed=embed)

@bot.command()
async def crawl(message, *urls):
    """
    Does a crawl in a website and store its content.
    """
    embed = discord.Embed(title="Crawler", color=0x00ff00)

    if urls:
        for url in urls:
            # Check if the url is valid
            try:
                crawl_request = requests.get(url)
            except requests.exceptions.MissingSchema:
                try:
                    crawl_request = requests.get(f'https://{url}')
                    url = f'https://{url}'
                except requests.exceptions.MissingSchema:
                    embed.add_field(name=url, value=f"Website {url} not found!", inline=False)
                    await message.send(embed=embed)
                    continue
                except requests.exceptions.ConnectionError:
                    embed.add_field(name=url, value=f"Website {url} not found!", inline=False)
                    await message.send(embed=embed)
                    continue
            except requests.exceptions.ConnectionError:
                embed.add_field(name=url, value=f"Website {url} not found!", inline=False)
                await message.send(embed=embed)
                continue

            # Check if the url is already in the database
            if url in global_database:
                title = re.search(r'<title>(.*?)</title>', global_database[url])
                if title:
                    embed.add_field(name=url, value=f"{title.group(1)} already crawled", inline=False)
                else:
                    embed.add_field(name=url, value=f"{url} already crawled", inline=False)
                await message.send(embed=embed)
                continue

            # Check if the url was crawled successfully and store its content
            if crawl_request.status_code == 200:
                crawl_data = crawl_request.text
                title = re.search(r'<title>(.*?)</title>', crawl_data)
                if title:
                    embed.add_field(name=url, value=f"{title.group(1)} was crawled successfully", inline=False)
                else:
                    embed.add_field(name=url, value=f"{url} was crawled successfully", inline=False)

                global_database[url] = crawl_data
                await message.send(embed=embed)
                continue

            # If the url was not crawled successfully
            else:
                embed.add_field(name=url, value=f"Website {url} not found!", inline=False)
                await message.send(embed=embed)
                continue

    # If no url was passed as argument
    else:
        embed.add_field(name="No url passed as argument", value="Please, pass a url as argument", inline=False)
        await message.send(embed=embed)

## VERIFICAR 7
@bot.command()
async def search(message, *keywords):
    """
    Search for a keyword in the crawled websites.
    """
    embed = discord.Embed(title="Search", color=0x00ff00)

    if keywords:
        for keyword in keywords:
            keyword = keyword.lower()
            # Check if the keyword is in the database
            if keyword in global_database:
                embed.add_field(name=keyword, value=f"{keyword} was found in {len(global_database[keyword])} websites", inline=False)
                await message.send(embed=embed)
                continue

            # If the keyword is not in the database
            else:
                embed.add_field(name=keyword, value=f"{keyword} was not found in any website", inline=False)
                await message.send(embed=embed)
                continue

    # If no keyword was passed as argument
    else:
        embed.add_field(name="No keyword passed as argument", value="Please, pass a keyword as argument", inline=False)
        await message.send(embed=embed)

bot.run(TOKEN)