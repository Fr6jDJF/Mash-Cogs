import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help
# Sys
import asyncio
import aiohttp
import random
import os
import sys

DIR_DATA = "data/oboobs"
SETTINGS = DIR_DATA+"/settings.json"
DEFAULT = {"nsfw_channels": ["133251234164375552"], "nsfw_msg": True, "ama_boobs": 10548, "ama_ass": 4542}# Red's testing chan. nsfw content off by default.

#API info:
#example: "/boobs/10/20/rank/" - get 20 boobs elements, start from 10th ordered by rank; noise: "/noise/{count=1; sql limit}/",
#example: "/noise/50/" - get 50 random noise elements; model search: "/boobs/model/{model; sql ilike}/",
#example: "/boobs/model/something/" - get all boobs elements, where model name contains "something", ordered by id; author search: "/boobs/author/{author; sql ilike}/",
#example: "/boobs/author/something/" - get all boobs elements, where author name contains "something", ordered by id; get boobs by id: "/boobs/get/{id=0}/",
#example: "/boobs/get/6202/" - get boobs element with id 6202; get boobs count: "/boobs/count/"; get noise count: "/noise/count/"; vote for boobs: "/boobs/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/boobs/vote/6202/minus/" - negative vote for boobs with id 6202; vote for noise: "/noise/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/noise/vote/57/minus/" - negative vote for noise with id 57;

#example: "/butts/10/20/rank/" - get 20 butts elements, start from 10th ordered by rank; noise: "/noise/{count=1; sql limit}/",
#example: "/noise/50/" - get 50 random noise elements; model search: "/butts/model/{model; sql ilike}/",
#example: "/butts/model/something/" - get all butts elements, where model name contains "something", ordered by id; author search: "/butts/author/{author; sql ilike}/",
#example: "/butts/author/something/" - get all butts elements, where author name contains "something", ordered by id; get butts by id: "/butts/get/{id=0}/",
#example: "/butts/get/6202/" - get butts element with id 6202; get butts count: "/butts/count/"; get noise count: "/noise/count/"; vote for butts: "/butts/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/butts/vote/6202/minus/" - negative vote for butts with id 6202; vote for noise: "/noise/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/noise/vote/57/minus/" - negative vote for noise with id 57;

class oboobs:
    """The oboobs/obutts.ru NSFW pictures of nature cog.
    https://github.com/Canule/Mash-Cogs
    """

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(SETTINGS)

    @commands.group(name="oboobs", pass_context=True)
    async def _oboobs(self, ctx):
        """The oboobs/obutts.ru pictures of nature cog."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    # Boobs
    @commands.command(pass_context=True, no_pm=False)
    async def boobs(self, ctx):
        """Shows some boobs."""
        author = ctx.message.author
        nsfwChan = False
        for a in self.settings["nsfw_channels"]:
            if a == ctx.message.channel.id:
                nsfwChan = True
                break
        try:
            rdm = random.randint(0, self.settings["ama_boobs"])
            search = ("http://api.oboobs.ru/boobs/{}".format(rdm))
            async with aiohttp.get(search) as r:
                result = await r.json()
                boob = random.choice(result)
                boob = "http://media.oboobs.ru/{}".format(boob["preview"])
        except Exception as e:
            await self.bot.say("{} ` Error getting results.`".format(author.mention))
            return
        if not nsfwChan:
            await self.bot.say("{}".format(boob))
        else:
            await self.bot.send_message(ctx.message.author, "{}".format(boob))
            if self.settings["nsfw_msg"]:
                await self.bot.say("{}` nsfw content is not allowed in this channel, instead I have send you a DM.`".format(author.mention))

    # Ass
    @commands.command(pass_context=True, no_pm=False)
    async def ass(self, ctx):
        """Shows some ass."""
        author = ctx.message.author
        nsfwChan = False
        for a in self.settings["nsfw_channels"]:
            if a == ctx.message.channel.id:
                nsfwChan = True
                break
        try:
            rdm = random.randint(0, self.settings["ama_ass"])
            search = ("http://api.obutts.ru/butts/{}".format(rdm))
            async with aiohttp.get(search) as r:
                result = await r.json()
                ass = random.choice(result)
                ass = "http://media.obutts.ru/{}".format(ass["preview"])
        except Exception as e:
            await self.bot.say("{} ` Error getting results.`".format(author.mention))
            return
        if not nsfwChan:
            await self.bot.say("{}".format(ass))
        else:
            await self.bot.send_message(ctx.message.author, "{}".format(ass))
            if self.settings["nsfw_msg"]:
                await self.bot.say("{}` nsfw content is not allowed in this channel, instead I have send you a DM.`".format(author.mention))

    @checks.admin_or_permissions(manage_server=True)
    @_oboobs.command(pass_context=True, no_pm=False)
    async def nsfw(self, ctx):
        """Toggle oboobs nswf for this channel on/off.
        Admin/owner restricted."""
        user= ctx.message.author
        nsfwChan = None
        # Reset nsfw.
        for a in self.settings["nsfw_channels"]:
            if a == ctx.message.channel.id:
                nsfwChan = True
                self.settings["nsfw_channels"].remove(a)
                await self.bot.say("{} ` nsfw ON`".format(user.mention))
                break
        # Set nsfw.
        if not nsfwChan:
            if ctx.message.channel not in self.settings["nsfw_channels"]:
                self.settings["nsfw_channels"].append(ctx.message.channel.id)
                await self.bot.say("{} ` nsfw OFF`".format(user.mention))
        dataIO.save_json(SETTINGS, self.settings)

    @checks.admin_or_permissions(manage_server=True)
    @_oboobs.command(pass_context=True, no_pm=False)
    async def togglemsg(self, ctx):
        """Enable/Disable the oboobs nswf not allowed message
        Admin/owner restricted."""
        user= ctx.message.author
        # Toggle
        if self.settings["nsfw_msg"]:
            self.settings["nsfw_msg"] = False
            await self.bot.say("{} ` DM nsfw channel msg is now: Disabled.`".format(user.mention))
        elif not self.settings["nsfw_msg"]:
            self.settings["nsfw_msg"] = True
            await self.bot.say("{} ` DM nsfw channel msg is now: Enabled.`".format(user.mention))
        dataIO.save_json(SETTINGS, self.settings)

    async def boob_knowlegde():
        # KISS
        settings = dataIO.load_json(SETTINGS)
        async def search(url, curr):
            search = ("{}{}".format(url, curr))
            async with aiohttp.get(search) as r:
                result = await r.json()
                return result

        # Upadate boobs len
        print("Collect boobs...")
        curr_boobs = settings["ama_boobs"]
        url = "http://api.oboobs.ru/boobs/"
        done = False
        reachable = curr_boobs
        step = 50
        while not done:
            q = reachable+step
            #print("Searching for boobs:", q)
            res = await search(url, q)
            if res != []:
                reachable = q
                res_dc = await search(url, q+1)
                if res_dc == []:
                    settings["ama_boobs"] = reachable
                    dataIO.save_json(SETTINGS, settings)
                    break
                else:
                    await asyncio.sleep(2.5) # Trying to be a bit gentle for the api.
                    continue
            elif res == []:
                step = round(step/2)
                if step <= 1:
                    settings["ama_boobs"] = curr_boobs
                    done = True
            await asyncio.sleep(2.5)
        print("Total amount of boobs:", settings["ama_boobs"])

        # Upadate ass len
        print("Collect ass...")
        curr_ass = settings["ama_ass"]
        url = "http://api.obutts.ru/butts/"
        done = False
        reachable = curr_ass
        step = 50
        while not done:
            q = reachable+step
            #print("Searching for ass:", q)
            res = await search(url, q)
            if res != []:
                reachable = q
                res_dc = await search(url, q+1)
                if res_dc == []:
                    settings["ama_ass"] = reachable
                    dataIO.save_json(SETTINGS, settings)
                    break
                else:
                    await asyncio.sleep(2.5)
                    continue
            elif res == []:
                step = round(step/2)
                if step <= 1:
                    settings["ama_ass"] = curr_ass
                    done = True
            await asyncio.sleep(2.5)
        print("Total amount of ass:", settings["ama_ass"])

def check_folders():
    if not os.path.exists(DIR_DATA):
        print("Creating data/oboobs folder...")
        os.makedirs(DIR_DATA)

def check_files():
    if not os.path.isfile(SETTINGS):
        print("Creating default boobs ass settings.json...")
        dataIO.save_json(SETTINGS, DEFAULT)
    else:  # Key consistency check
        try:
            current = dataIO.load_json(SETTINGS)
        except JSONDecodeError:
            dataIO.save_json(SETTINGS, DEFAULT)
            current = dataIO.load_json(SETTINGS)

        if current.keys() != DEFAULT.keys():
            for key in DEFAULT.keys():
                if key not in current.keys():
                    current[key] = DEFAULT[key]
                    print( "Adding " + str(key) + " field to boobs settings.json")
            dataIO.save_json(SETTINGS, DEFAULT)

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(oboobs(bot))
    bot.loop.create_task(oboobs.boob_knowlegde())

