import discord
from discord.ext import commands

class Tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # This is so you can access Bot instance in your cog

# You must have this function for `bot.load_extension` to call
def setup(bot):
    bot.add_cog(Tracking(bot))


import aiohttp
from bs4 import BeautifulSoup

async def crawl_url(session, url):
    # Check if the url is valid
    try:
        async with session.get(url) as crawl_request:
            if crawl_request.status == 200:
                crawl_data = await crawl_request.text()
                soup = BeautifulSoup(crawl_data, 'html.parser')
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
                    return {"title": title.text, "content": crawl_data_content, "inverted_index": inverted_index}
                else:
                    return {"title": url, "content": crawl_data_content, "inverted_index": inverted_index}
            else:
                return None
    except Exception as e:
        return None

@bot.command()
async def crawl(ctx, *urls):
    """
    Does a crawl in a website and store its content.
    """
    embed = discord.Embed(title="Crawler - Processing...", color=0x00ff00)
    message = await ctx.send(embed=embed)

    # If no url was passed as argument
    if not urls:
        embed.add_field(name="No URL", value="Please, pass at least one URL as argument", inline=False)
        embed.title = "Crawler - Finished!"
        await message.edit(embed=embed)
        return

    async with aiohttp.ClientSession() as session:
        for url in urls:
            crawl_data = await crawl_url(session, url)
            if crawl_data is not None:
                # Process and store crawl data
                global_database[url] = crawl_data
                embed.add_field(name=f"**{crawl_data['title']}**", value=f"[{crawl_data['title']}]({url}) crawled successfully", inline=False)
            else:
                embed.add_field(name=f"**{url}**", value=f"Website not found!", inline=False)
            await message.edit(embed=embed)

    embed.title = "Crawler - Finished!"
    await message.edit(embed=embed)