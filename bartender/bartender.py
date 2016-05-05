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


class Bartender:
    """Search for torrents"""
    def __init__(self,bot):
        self.bot = bot
        self.items = [["beer", ":beer:", 2], ["wine", ":wine_glass:", 2], ["racecar", ":race_car:", 120000]]
        self.numbers = ["one", "two", "tree", "four", "five", "six", "seven", "eight", "nine", "ten"]
        self.text= ["one", "two", "tree", "four", "five", "six", "seven", "eight", "nine", "ten"]
        self.bank = fileIO("data/economy/bank.json", "load")

    @commands.command(pass_context=True, no_pm=False)
    async def buy(self, ctx, amount : int, drink):
        """Buy a drink"""
        price = -1
        icon = ""
        available = False
        for i, item in enumerate(self.items):
            print(i)
            print(item)
            if drink == self.items[i][0]:
                icon = self.items[i][1]
                price = self.items[i][2]*amount
                available = True
                break
        if not available:
            await self.bot.say("Im sorry to dissapoint you, we dont serve {}".format(drink))
            return
                
        content = ctx.message.content      
        mentions = ctx.message.mentions       
        author = ctx.message.author
        buy_for = []
        for member in mentions:
            buy_for.append(member.mention)
        buy_for = " ".join(buy_for)
        
        if self.enough_money(author.id, price):
            if self.withdraw_money(author.id, price):
                drinks = ""
                for d in range(0,amount):
                    drinks = drinks+icon
                if buy_for == "":
                    await self.bot.say("{} There you go mate {}".format(buy_for, drinks))
                else:
                    await self.bot.say("{0} Have some {1} from {2}{3}".format(buy_for, drink, author, drinks))
            else:
                await self.bot.say("I don't accept marbles")          
        else:
            try:
                text_num = self.numbers[amount-1]
            except Exception as e:
                text_num = str(amount)
            await self.bot.say("{0} Sorry mate, you don't have enough money for {1} {2}.\n it cost's €{3}".format(author.mention, text_num, drink, price))
           
    def account_check(self, id):
        if id in self.bank:
            return True
        else:
            return False
            
    def enough_money(self, id, amount):
        if self.account_check(id):
            if self.bank[id]["balance"] >= int(amount):
                print("y enough")
                return True
            else:
                print("n enough")            
                return False
        else:
            print("n account")          
            return False
            
    def withdraw_money(self, id, amount):
        if self.account_check(id):
            if self.bank[id]["balance"] >= int(amount):
                self.bank[id]["balance"] = self.bank[id]["balance"] - int(amount)
                fileIO("data/economy/bank.json", "save", self.bank)
                print("paid")                
                return True
            else:
                print("not paid")
                return False
        else:
            print("not paid")
            return False

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Set-up
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
class ModuleNotFound(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message        

def setup(bot):
    bot.add_cog(Bartender(bot))


