from .utils.dataIO import fileIO
from .utils import checks
from __main__ import send_cmd_help
from __main__ import settings as bot_settings
# Sys.
from operator import itemgetter, attrgetter
import discord
from discord.ext import commands
#from copy import deepcopy
#import aiohttp
#import asyncio
import json
import os

try:
    import ktorrent
    ktorrent_available = True
except:
    ktorrent_available = False


class Torrent:
    """Search for torrents"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False)
    async def torrent(self, ctx, *, text):
        """Search for various torrents"""
        if text == ():
            await send_cmd_help(ctx)
            return
        text = "".join(text)
        #print(text)        
        # Basic Search
        search = ktorrent.search(search=text)
        # Complex Search
        #search = ktorrent.search(search='Linux Shell script', strict=1, category='books', field='age', sorder='desc', page=2)
        #print (search)
        # Top books
        #search = ktorrent.top(category=text)
        # Top movies
        #search = ktorrent.top(category=text, page=2)
        #print (top_books)
        """
        "meta"
            "pageCurrent"
            "pageResult"
            "pageTotal"
            //
			"age"
			"category"
			"files"
			"leech"
			"link"
			"magnet"
			"name"
			"seed"
			"size"
			"verified"
			"web"
        """
        
        #print (search)
        d = json.loads(search)
            
        if len(d) > 1:
            list = "\n"
            index = 0
            for items in range(0, len(d)):
                index += 1
                item = d["torrent"][items]
                name = item["name"][:200] 
                emoij_index = self.replace_text(str(index))
                list = list + "{6}\n       **Name: **{0}\n       **Age: **{1}\n**       Leech/Seed: **{2}/{3}\n**       Size: **{4}\n**       Link: **{5}\n\n".format(name, item["age"], item["seed"], item["leech"], item["size"], item["link"], emoij_index)
            await self.bot.say(list)
        else:      
            await self.bot.say("shrug")
    
    def replace_text(self, val):
            replaceThis = [["1", ":one:"], ["2", ":two:"], ["3", ":three:"], ["4", ":four:"], ["5", ":five:"], ["6", ":six:"], ["7", ":seven:"], ["8", ":eight: "], ["9", ":nine:"], ["10", ":keycap_ten:"]]
            replacedText = val
            for r in range(0, len(replaceThis)):
                replacedText = replacedText.replace(replaceThis[r][0], replaceThis[r][1])                    
            return replacedText
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Set-up
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
class ModuleNotFound(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message        

def setup(bot):
    if not ktorrent_available:
        raise ModuleNotFound("ktorrent is not installed. Do 'pip3 install ktorrent --upgrade' to use this cog.")
        return
    bot.add_cog(Torrent(bot))


