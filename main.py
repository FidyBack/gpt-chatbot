from dotenv import load_dotenv
from discord.ext import commands
from discord import ClientUser
from bs4 import BeautifulSoup
from aiohttp import client_exceptions
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np
import pandas as pd
import aiohttp
import discord
import random
import re
import os
import time
import errno

# Program initial configuration
global_inverted_index = {}
global_documents = pd.DataFrame(columns=['url', 'title', 'body'])

if not os.path.exists('error.log'):
    with open('error.log', 'w') as file:
        file.write('')
# if not os.path.exists('database'):
#     try:
#         os.makedirs('database')
#     except OSError as e:
#         if e.errno != errno.EEXIST:
#             raise
        
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

# Cogs
# bot.load_extension('cogs.tracking')
# bot.load_extension('cogs.database')  
# bot.load_extension('cogs.search')
# bot.load_extension('cogs.help')

# Functions
async def fetch(session, url):
    """
    Fetches a website content.
    """
    async with session.get(url) as response:
        return await response.text()
    

def update_inverted_index():
    """
    
    """
    global global_inverted_index
    # TF-IDF
    urls = global_documents['url'].tolist()
    body_data = global_documents['body'].tolist()

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(body_data)

    # Inverted Index
    for word in vectorizer.vocabulary_:
        all_documents_tfidf = tfidf.tocsc()[:,vectorizer.vocabulary_.get(word)].toarray().flatten()
        global_inverted_index[word] = {urls[index]: value for index, value in enumerate(all_documents_tfidf) if value > 0.0}

    global_inverted_index = {key: value for key, value in sorted(global_inverted_index.items(), key=lambda item: item[0], reverse=True)} # Ver amanhã
    print(global_inverted_index)

# Events
@bot.event
async def on_ready():
    """
    Shows a message when the bot is ready.
    """
    assert isinstance(bot.user, ClientUser)
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

# Commands
@bot.command()
async def source(ctx):
    """
    Show the source code of this bot.
    """
    embed = discord.Embed(title="Source Code: https://github.com/FidyBack/gpt-chatbot", color=0x00ff00)

    try:
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'An error occurred while sending the message: {e}')

@bot.command()
async def author(ctx):
    """
    Show the author and the email of this bot.
    """
    embed = discord.Embed(title="Author", color=0x00ff00)
    title, content = ['Credits', 'E-mail'], ['Abel Cavalcante', 'abelcan@al.insper.edu.br']
    for index, value in enumerate(title):
        embed.add_field(name=value, value=content[index], inline=False)

    try:
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'An error occurred while sending the message: {e}')

@bot.command()
async def run(ctx, pokemon_name: str = ""):
    """
    Shows a pokemon and some of its characteristics.
    """
    embed = discord.Embed(title="What's your Pokemon?", color=0x00ff00)

    async with aiohttp.ClientSession() as session:
        if pokemon_name:
            pokemon_name = re.sub(r'\W+', '', pokemon_name.lower())
            poke_request = await session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
        else:
            pokemon_id = random.randint(1, 1010)
            poke_request = await session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        
        if poke_request.status == 200:
            pokemon_data = await poke_request.json()
        
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

    try:
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'An error occurred while sending the message: {e}')

@bot.command()
async def crawl(ctx, *urls):
    """
    Does a crawl in a website and store its content.
    """
    global global_documents
    urls_stored = global_documents['url'].tolist()

    embed = discord.Embed(title="Crawler - Processing...", color=0x00ff00)
    message = await ctx.send(embed=embed)

    # If no url was passed as argument
    if not urls:
        embed.add_field(name="No URL", value="Please, pass at least one URL as argument", inline=False)
        embed.title = "Crawler - Finished!"
        await message.edit(embed=embed)
        return

    # URLs request and error handling
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                crawl_request = await fetch(session, url)
            except client_exceptions.InvalidURL:
                try:
                    crawl_request = await fetch(session, f'https://{url}')
                    url = f'https://{url}'
                except client_exceptions.InvalidURL:
                    embed.add_field(name=f"**{url}**", value=f"Website not found!", inline=False)
                    await message.edit(embed=embed)
                    continue
                except Exception as e:
                    embed.add_field(name=f"**{url}**", value=f"Website not found!", inline=False) # TODO: Change this message
                    await message.edit(embed=embed)
                    continue
            except Exception as e:
                embed.add_field(name=f"**{url}**", value=f"Website not found!", inline=False) # TODO: Change this message
                await message.edit(embed=embed)
                continue

            # Check if the url is already in the database
            if url in urls_stored:
                title = global_documents[global_documents['url'] == url]['title'].values[0]
                if title:
                    embed.add_field(name=f"**{title}**", value=f"[{title}]({url}) already crawled", inline=False)
                else:
                    embed.add_field(name=f"**{url}**", value=f"{url} already crawled", inline=False)
                await message.edit(embed=embed)
                continue

            # Check if the url was crawled successfully and store its content in both global_documents and global_inverted_index
            if crawl_request:
                soup = BeautifulSoup(crawl_request, 'html.parser')
                page_title = soup.title.text if soup.title else None
                page_body = soup.body.text if soup.body else None

                if not page_body:
                    embed.add_field(name=f"**{url}**", value=f"{url} crawled successfully, but it has no content", inline=False)
                    await message.edit(embed=embed)
                    continue

                global_documents = pd.concat([global_documents, pd.DataFrame({'url': [url], 'title': [page_title], 'body': [page_body]})], ignore_index=True)
                embed.add_field(name=f"**{page_title}**", value=f"[{page_title}]({url}) crawled successfully", inline=False)

                await message.edit(embed=embed)
                continue

            # If the url was not crawled successfully
            else:
                embed.add_field(name=f"**{url}**", value=f"{url} not crawled successfully: {crawl_request}", inline=False)
                await message.edit(embed=embed)
                continue

    # Check if there's any new url in global_documents and update the inverted index
    if set(global_documents['url'].tolist()) != set(urls_stored):
        update_inverted_index()

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

    # If no keyword was passed as argument
    if not keywords:
        embed.add_field(name="Error", value="No keyword passed as argument!", inline=False)
        embed.title = "Search - Finished!"
        await message.edit(embed=embed)
        return

    # Starts the search using inverted index
    for keyword in keywords:
        links_titles_times = []
        for url, content in global_database.items():
            if keyword in content["inverted_index"]:
                links_titles_times.append((url, content["title"], content["inverted_index"][keyword]))

        # Sort the results by the number of times the keyword appears in the website
        links_titles_times.sort(key=lambda x: x[2], reverse=True)

        # Add the results to the embed
        if links_titles_times:
            embed.add_field(
                name=f"Keyword: **{keyword}**",
                value="\n".join([f"[{title}]({url}) - {times} times" for url, title, times in links_titles_times]),
                inline=False
                )
        else:
            embed.add_field(name=f"Keyword: **{keyword}**", value="No results", inline=False)
    
    embed.title = "Search - Finished!"
    await message.edit(embed=embed)

@bot.command()
async def wn_search(ctx, *keywords):
    """
    Search for websites that contain the keywords and words that are similar to the keywords using wordnet.
    """
    embed = discord.Embed(title="Wordnet Search - Processing...", color=0x00ff00)
    await ctx.send(embed=embed)

    # Get the last message sent by the bot
    async for message in ctx.channel.history(limit=100):
        if message.author == bot.user:
            break

    # If no keyword was passed as argument
    if not keywords:
        embed.add_field(name="Error", value="No keyword passed as argument!", inline=False)
        embed.title = "Wordnet Search - Finished!"
        await message.edit(embed=embed)
        return

@bot.command()
async def reload(ctx):
    bot.reload_extension("cogs.tracking")

@bot.command()
async def help(message):
    """
    Shows a list of commands.
    """
    embed = discord.Embed(title="Help", color=0x00ff00)
    title = ['!source', '!author', '!run', '!run <pokemon_name>', '!crawl <url>', '!search <keyword>', '!wn_search <keyword>']
    content = [
        'Shows the source code of the bot.',
        'Shows the author of the bot.',
        'Shows information about a pokemon.',
        'Shows information about a specific pokemon.',
        'Crawls one or more websites.',
        'Search and shows websites that contain the keywords. It also shows the number of times the keyword appears in the website. Can be used with multiple keywords.',
        'Search and shows websites that contain the keywords and words that are similar to the keywords using wordnet. Can be used with multiple keywords.'
        ]
    for index, value in enumerate(title):
        embed.add_field(name=value, value=content[index], inline=False)
    
    await message.send(embed=embed)

bot.run(TOKEN)
