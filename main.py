from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup


import requests
import discord
import random
import re
import os
import time
import errno

# Program initial configuration
global_database = {}
if not os.path.exists('error.log'):
    with open('error.log', 'w') as file:
        file.write('')


# Discord initial configuration
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


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
async def crawl(ctx, *urls):
    """
    Does a crawl in a website and store its content.
    """
    embed = discord.Embed(title="Crawler - Processing...", color=0x00ff00)
    await ctx.send(embed=embed)

    # Get the last message sent by the bot
    async for message in ctx.channel.history(limit=100):
        if message.author == bot.user:
            break

    # Check if there is any url
    if urls:
        for url in urls:
            # Check if the url is valid
            try:
                crawl_request = requests.get(url)
            except requests.exceptions.MissingSchema:
                try:
                    crawl_request = requests.get(f'https://{url}')
                    url = f'https://{url}'
                except Exception as e:
                    embed.add_field(name=url, value=f"Website {url} not found!", inline=False)
                    await message.edit(embed=embed)
                    continue
            except Exception as e:
                embed.add_field(name=url, value=f"Website {url} not found!", inline=False)
                await message.edit(embed=embed)
                continue

            # Check if the url is already in the database
            if url in global_database:
                title = global_database[url]["title"]
                if title:
                    embed.add_field(name=url, value=f"{title} already crawled", inline=False)
                else:
                    embed.add_field(name=url, value=f"{url} already crawled", inline=False)
                await message.edit(embed=embed)
                continue

            # Check if the url was crawled successfully and store its content
            if crawl_request.status_code == 200:
                soup = BeautifulSoup(crawl_request.text, 'html.parser')
                title = soup.title
                crawl_data_content = soup.body.text
                inverted_index = {}

                # Create the inverted index
                for word in crawl_data_content.split():
                    if word in inverted_index:
                        inverted_index[word] += 1
                    else:
                        inverted_index[word] = 1

                if title:
                    global_database[url] = {"title": title.text, "content": crawl_data_content, "inverted_index": inverted_index}
                    embed.add_field(name=url, value=f"{title.text} was crawled successfully", inline=False)
                else:
                    global_database[url] = {"title": None, "content": crawl_data_content, "inverted_index": inverted_index}
                    embed.add_field(name=url, value=f"{url} was crawled successfully", inline=False)

                await message.edit(embed=embed)
                continue

            # If the url was not crawled successfully
            else:
                print(f'Error {crawl_request.status_code} - {crawl_request.reason} - {url}')
                error_code = crawl_request.status_code
                embed.add_field(name=url, value=f"Error {error_code} - {crawl_request.reason}", inline=False)
                await message.edit(embed=embed)

    # If no url was passed as argument
    else:
        embed.add_field(name="Error", value="No url passed as argument!", inline=False)
        await message.edit(embed=embed)

    embed.title = "Crawler - Finished!"
    await message.edit(embed=embed)

@bot.command()
async def search(ctx, *keywords):
    """
    Search for websites that contain the keywords.
    """
    embed = discord.Embed(title="Search - Processing...", color=0x00ff00)
    await ctx.send(embed=embed)

    # Get the last message sent by the bot
    async for message in ctx.channel.history(limit=100):
        if message.author == bot.user:
            break

    # Check if there is any keyword
    if keywords:
        # starts the search using inverted index
        for keyword in keywords:
            # Check if the keyword is in the database
            for url, content in global_database.items():
                if keyword in content["inverted_index"]:
                    title = content["title"]
                    times = content["inverted_index"][keyword]
                    if title:
                        embed.add_field(name=url, value=f"{title} contains the keyword **{keyword}** {times} times", inline=False)
                    else:
                        embed.add_field(name=url, value=f"{url} contains the keyword **{keyword}** {times} times", inline=False)
                    await message.edit(embed=embed)
                    continue
        
        # TODO: SEE THAT
        if not embed.fields:
            embed.add_field(name="Search", value="No results found!", inline=False)
            await message.edit(embed=embed)
    
    # If no keyword was passed as argument
    else:
        embed.add_field(name="Error", value="No keyword passed as argument!", inline=False)
        await message.edit(embed=embed)
    
    embed.title = "Search - Finished!"
    await message.edit(embed=embed)


@bot.command()
async def help(message):
    """
    Shows a list of commands.
    """
    embed = discord.Embed(title="Help", color=0x00ff00)
    title = ['!source', '!author', '!run', '!run <pokemon_name>', '!crawl <url>', '!search <keyword>']
    content = [
        'Show the source code of this bot', 
        'Show the author of this bot', 
        'Shows a random pokemon and its type', 
        'Shows the selected pokemon and its type',
        'Crawl a website and store its content',
        'Search for websites that contains the keyword'
        ]
    for index, value in enumerate(title):
        embed.add_field(name=value, value=content[index], inline=False)
    
    await message.send(embed=embed)

bot.run(TOKEN)