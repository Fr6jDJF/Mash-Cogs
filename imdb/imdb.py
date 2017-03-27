from cogs.utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help
from __main__ import settings as bot_settings
# Sys.
import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
import os
import ast

DIR_DATA = "data/imdb"
SETTINGS = DIR_DATA+"/settings.json"
DEFAULT = {"api_key": ""}
#PREFIXES = bot_settings.prefixes~~~~~~

#imdb snippet by BananaWaffles from the early Red, rewritten as cog.

class imdb:
    """Myapifilms.com imdb movie search."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(SETTINGS) 
        if self.settings["api_key"] == "":
            print("Cog error: imdb, No API key found, please configure me!")

    @commands.command(pass_context=True, no_pm=True)
    async def imdb(self, ctx, *title):
        """Search for movies on imdb"""
        if title == ():
            await send_cmd_help(ctx)
            return
        else:
            if self.settings["api_key"] == "":
                getKeyUrl = "http://www.myapifilms.com/token.do"
                await self.bot.say("` This cog wasn't configured properly. If you're the owner, add your API key available from '{}', and use '{}apikey_imdb' to setup`".format(getKeyUrl, ctx.prefix))
                return
            try:
                await self.bot.send_typing(ctx.message.channel)
                movieTitle = "+".join(title)
                search = "http://api.myapifilms.com/imdb/title?format=json&title=" + movieTitle + "&token=" + self.settings["api_key"]
                async with aiohttp.get(search) as r:
                    result = await r.json()
                    title = result['data']['movies'][0]['title']
                    year = result['data']['movies'][0]['year']
                    if year == "": 
                        year = "????"
                    rating = result['data']['movies'][0]['rating']
                    rating = rating.replace("," , ".")
                    if rating == "":
                        rating = "-"
                    else:
                        rating = float(rating)
                    urlz = result['data']['movies'][0]['urlIMDB']
                    urlPoster = result['data']['movies'][0]['urlPoster']
                    if urlPoster == "":
                        urlPoster = "http://instagram.apps.wix.com/bundles/wixinstagram/images/ge/no_media.png"
                    simplePlot = result['data']['movies'][0]['simplePlot']
                    if simplePlot == "":
                        simplePlot = "Everyone died...."


                #data = discord.Embed(colour=discord.Colour.yellow())
                data = discord.Embed(colour=0xE4BA22)
                data.add_field(name="Title:", value=str(title), inline=True)
                data.add_field(name="Released on:", value=year)
                
                if type(rating) is float:
                    emoji = ":poop:"
                    if float(rating) > 3.5:
                        emoji = ":thumbsdown:"
                    if float(rating) > 5.2:
                        emoji = ":thumbsup:"
                    if float(rating) > 7.0:
                        emoji = ":ok_hand:"
                else:
                    emoji = ""
                rating= "{} {}".format(rating, emoji)
                data.add_field(name="IMDB Rating:", value=rating)

                if urlz != "":
                    moreinfo = ("{}\n[Read more...]({})".format(simplePlot, urlz))
                    data.add_field(name="Plot:", value=moreinfo)
                data.set_footer(text="\n\n")
                data.set_thumbnail(url=urlPoster)
                await self.bot.say(embed=data)

                #Big image, will break soon™
                #find = "._V1_";
                #split_pos = urlPoster.find(find)
                #urlPoster = urlPoster[0:split_pos+5]+".jpg"

                #response = await self.bot.wait_for_message(timeout=20, author=ctx.message.author)
                #if response is None:
                #    pass
                #else:
                #    response = response.content.lower().strip()
                #if response.startswith(("bigpic", "cover", "big", ":eyeglasses:")):
                #    await self.bot.say(urlPoster)
            except discord.HTTPException:
                await self.bot.say("I need the `Embed links` permission to send this")
            except Exception as e:
                print(e)
                await self.bot.say("` Error getting a result.`")

    @commands.command(pass_context=True, no_pm=False)
    @checks.admin_or_permissions(manage_server=True)
    async def apikey_imdb(self, ctx, key):
        """Set the imdb API key."""
        user = ctx.message.author
        if self.settings["api_key"] != "":
            await self.bot.say("{} ` imdb API key found, overwrite it? y/n`".format(user.mention))
            response = await self.bot.wait_for_message(author=ctx.message.author)
            if response.content.lower().strip() == "y":
                self.settings["api_key"] = key
                dataIO.save_json(SETTINGS, self.settings)
                await self.bot.say("{} ` imdb API key saved...`".format(user.mention))
            else:
                await self.bot.say("{} `Cancled API key opertation...`".format(user.mention))
        else:
            self.settings["api_key"] = key
            dataIO.save_json(SETTINGS, self.settings)
            await self.bot.say("{} ` imdb API key saved...`".format(user.mention))
        self.settings = dataIO.load_json(SETTINGS)

def check_folders():
    if not os.path.exists(DIR_DATA):
        print("Creating data/imdb folder...")
        os.makedirs(DIR_DATA)

def check_files():
    if not os.path.isfile(SETTINGS):
        print("Creating default imdb settings.json...")
        dataIO.save_json(SETTINGS, DEFAULT)
    else:  # Consistency check
        try:
            current = dataIO.load_json(SETTINGS)
        except JSONDecodeError:
            dataIO.save_json(SETTINGS, DEFAULT)
            current = dataIO.load_json(SETTINGS)

        if current.keys() != DEFAULT.keys():
            for key in DEFAULT.keys():
                if key not in current.keys():
                    current[key] = DEFAULT[key]
                    print( "Adding " + str(key) + " field to imdb settings.json")
            dataIO.save_json(SETTINGS, DEFAULT)

def setup(bot):
    check_folders()
    check_files()
    n = imdb(bot)
    bot.add_cog(n)

