import discord
import random
import urllib.request
import json
import time
import traceback
from discord.ext import commands

class Starwiki:
    """Starwiki ported from Starbot by Sydney"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def starwiki(self, *, query : str):
        if query == '':
            await self.bot.say('Usage:\nstarwiki [search term]')
        else:
            if query.startswith(" "):
                query = query[1:]
            result = Wikia.wikia_get('starvstheforcesofevil', query)
            if result == None:
                await self.bot.say("No result found for '{}'".format(query))
            else:
                await self.bot.say(embed=result)

    @commands.command()
    async def wikia(self, *, query: str):
        if query == '':
            await self.bot.say('Usage:\nwikia [wikia name] [search term]')
            return

        input_split = query.split(' ', 1)
        print(input_split)

        if len(input_split) != 2:
            await self.bot.say('Usage:\nwikia [wikia name] [search term]')
            return

        result = Wikia.wikia_get(input_split[0], input_split[1])
        if result == None:
            await self.bot.say("No result found for '{}'".format(query))
        else:
            await self.bot.say(embed=result)

def setup(bot):
    bot.add_cog(Starwiki(bot))

class Wikia:
    wiki_name = ""

    cache = {}
    query_cache = {}

    def wikia_get(wiki, search):
        '''Fetch and return data from Wikia'''
        current_milli_time = lambda: round(time.time() * 1000, 3)

        search_start = current_milli_time()
        starwiki = Wikia(wiki)

        title = ""
        body = ""
        url = ""
        img = ""
        cachelevel = 0

        try:
            if search in Wikia.query_cache:
                results = Wikia.query_cache[search]
                search_end = current_milli_time()

                results.set_footer(text="Cache Level: {} | search time: {}ms".format(2, (search_end - search_start)))
                return results
            else:
                results = starwiki.wikia_search(search)
                page = starwiki.wikia_getpage(results[0]['id'])
                section = page[0]

                resultid = results[0]['id']
                if resultid in Wikia.cache:
                    results = Wikia.cache[resultid]
                    search_end = current_milli_time()

                    results.set_footer(text="Cache Level: {} | search time: {}ms".format(1, (search_end - search_start)))
                    return results
                else:
                    details = starwiki.wikia_getdetails(results[0]['id'])

                    # Some really stupid hacks to get the main image
                    img_thumb = details[str(resultid)]['thumbnail']
                    img_stuff = img_thumb.split("window-crop", 1)
                    img_stuff2 = img_stuff[1].split("?")

                    img = img_stuff[0][:-1] + "?" + img_stuff2[1]
                    url = results[0]['url']
                    title = section['title']
                    body = section['content'][0]['text']

                    search_end = current_milli_time()

                    embed = discord.Embed(color=discord.Color.green())
                    embed.set_author(name="Visit the full page here",
                         url=url,
                         icon_url='http://slot1.images.wikia.nocookie.net/__cb1493894030/common/skins/common/images/wiki.png')
                    embed.add_field(name=title, value=body)
                    embed.set_image(url=img)
                    embed.set_footer(text="Cache Level: {} | search time: {}ms".format(cachelevel, (search_end - search_start)))

                    Wikia.cache[results[0]['id']] = embed
                    Wikia.query_cache[search] = Wikia.cache[results[0]['id']]
                    return embed
        except Exception as exc:
            print(exc)
            print(traceback.format_exc())
            return None

    def __init__(self, wiki):
        self.wiki_name = wiki

    def wikia_search(self, term, limit=1):
        '''Search for a page on Wikia'''
        # TODO: make limits over 1 return an array
        search_term = term.replace(" ", "+")
        url = "http://{}.wikia.com/api/v1/Search/List?query={}&limit=1&minArticleQuality=10&batch=1&namespaces=0%2C14".format(self.wiki_name, search_term)

        json_string = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(json_string)

        return json_d['items']

    def wikia_getpage(self, page_id):
        '''Get a page on Wikia based on the page ID'''
        url = "http://{}.wikia.com/api/v1/Articles/AsSimpleJson?id={}".format(self.wiki_name, page_id)

        json_string = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(json_string)

        return json_d['sections']

    def wikia_getdetails(self, page_id):
        '''Get details of a wikia page based on a page ID'''
        url = "http://{}.wikia.com/api/v1/Articles/Details?ids={}&abstract=100&width=200&height=200".format(self.wiki_name, page_id)

        json_string = urllib.request.urlopen(url).read().decode("utf-8")
        json_d = json.loads(json_string)

        return json_d['items']