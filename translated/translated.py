from .utils.dataIO import fileIO
from .utils import checks
from __main__ import send_cmd_help
from __main__ import settings as bot_settings
# Sys.
import discord
from discord.ext import commands
from operator import itemgetter, attrgetter
#from copy import deepcopy
import random
import os
import sys
import time
import re
import urllib.parse as up
#import logging
import aiohttp


__author__ = "Mash"
__version__ = "0.0.2"


# ToDo:

# bot output replacement. (exclude translation of commands in help output or alias commands to translated lang).
# Channel language
# Submit corrected system translations to repo. lang. db or translated.net(requires translated.net account).
# Selfbot
# ...



"""MyMemory: API usage limits
    Get:
        Searches MyMemory for matches against a segment.
        MyMemory tracks it usage in words. This means that it doesn't matter how many requests you submit to consult the archive, but the weight of each request.
        Free, anonymous usage is limited to 1000 words/day.
        Provide a valid email ('de' parameter), where we can reach you in case of troubles, and enjoy 10000 words/day.
"""


DIR_DATA = "data/translated"
CACHE = DIR_DATA+"/cache.json"
CH_LANG = DIR_DATA+"/chlang.json"
SETTINGS = DIR_DATA+"/settings.json"

class Translated:
    """Translate text with use of translated.net API.
    Machine Translation provided by Google, Microsoft, Worldlingo or MyMemory customized engine.
    """

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO(SETTINGS, "load")
        self.cache = fileIO(CACHE, "load")
        # These should be supported by translated.net (RFC3066)
        self.ISO_LANG = [["Abkhazian", "AB"], ["Afar", "AA"], ["Afrikaans", "AF"], ["Albanian", "SQ"], ["Amharic", "AM"], ["Arabic", "AR"], ["Armenian", "HY"], ["Assamese", "AS"], ["Aymara", "AY"],
                                ["Azerbaijani", "AZ"], ["Bashkir", "BA"], ["Basque", "EU"], ["Bengali, Bangla", "BN"], ["Bhutani", "DZ"], ["Bihari", "BH"], ["Bislama", "BI"], ["Breton", "BR"], ["Bulgarian", "BG"],
                                ["Burmese", "MY"], ["Byelorussian", "BE"], ["Cambodian", "KM"], ["Catalan", "CA"], ["Chinese", "ZH"], ["Corsican", "CO"], ["Croatian", "HR"], ["Czech", "CS"], ["Danish", "DA"],
                                ["Dutch", "NL"], ["English, American", "EN"], ["Esperanto", "EO"], ["Estonian", "ET"], ["Faeroese", "FO"], ["Fiji", "FJ"], ["Finnish", "FI"], ["French", "FR"], ["Frisian", "FY"],
                                ["Gaelic (Scots Gaelic)", "GD"], ["Galician", "GL"], ["Georgian", "KA"], ["German", "DE"], ["Greek", "EL"], ["Greenlandic", "KL"], ["Guarani", "GN"], ["Gujarati", "GU"],
                                ["Hausa", "HA"], ["Hebrew", "IW"], ["Hindi", "HI"], ["Hungarian", "HU"], ["Icelandic", "IS"], ["Indonesian", "IN"], ["Interlingua", "IA"], ["Interlingue", "IE"], ["Inupiak", "IK"],
                                ["Irish", "GA"], ["Italian", "IT"], ["Japanese", "JA"], ["Javanese", "JW"], ["Kannada", "KN"], ["Kashmiri", "KS"], ["Kazakh", "KK"], ["Kinyarwanda", "RW"], ["Kirghiz", "KY"],
                                ["Kirundi", "RN"], ["Korean", "KO"], ["Kurdish", "KU"], ["Laothian", "LO"], ["Latin", "LA"], ["Latvian, Lettish", "LV"], ["Lingala", "LN"], ["Lithuanian", "LT"], ["Macedonian", "MK"],
                                ["Malagasy", "MG"], ["Malay", "MS"], ["Malayalam", "ML"], ["Maltese", "MT"], ["Maori", "MI"], ["Marathi", "MR"], ["Moldavian", "MO"], ["Mongolian", "MN"], ["Nauru", "NA"],
                                ["Nepali", "NE"], ["Norwegian", "NO"], ["Occitan", "OC"], ["Oriya", "OR"], ["Oromo, Afan", "OM"], ["Pashto, Pushto", "PS"], ["Persian", "FA"], ["Polish", "PL"], ["Portuguese", "PT"],
                                ["Punjabi", "PA"], ["Quechua", "QU"], ["Rhaeto-Romance", "RM"], ["Romanian", "RO"], ["Russian", "RU"], ["Samoan", "SM"], ["Sangro", "SG"], ["Sanskrit", "SA"], ["Serbian", "SR"],
                                ["Serbo-Croatian", "SH"], ["Sesotho", "ST"], ["Setswana", "TN"], ["Shona", "SN"], ["Sindhi", "SD"], ["Singhalese", "SI"], ["Siswati", "SS"], ["Slovak", "SK"], ["Slovenian", "SL"],
                                ["Somali", "SO"], ["Spanish", "ES"], ["Sudanese", "SU"], ["Swahili", "SW"], ["Swedish", "SV"], ["Tagalog", "TL"], ["Tajik", "TG"], ["Tamil", "TA"], ["Tatar", "TT"], ["Tegulu", "TE"],
                                ["Thai", "TH"], ["Tibetan", "BO"], ["Tigrinya", "TI"], ["Tonga", "TO"], ["Tsonga", "TS"], ["Turkish", "TR"], ["Turkmen", "TK"], ["Twi", "TW"], ["Ukrainian", "UK"], ["Urdu", "UR"],
                                ["Uzbek", "UZ"], ["Vietnamese", "VI"], ["Volapuk", "VO"], ["Welsh", "CY"], ["Wolof", "WO"], ["Xhosa", "XH"], ["Yiddish", "JI"], ["Yoruba", "YO"], ["Zulu", "ZU"]]


    @commands.command(pass_context=True, no_pm=False)
    async def translate(self, ctx, languageFrom, languageTo,  *text):
        """Translate text with use of translated.net \n *[lang1 lang2] + [Text to translate]"""
        author = ctx.message.author
        #channel = ctx.channel.id

        if text == ():
            await send_cmd_help(ctx)
            return

        lfr_valid, lang_from = self.check_language(self.ISO_LANG, languageFrom)
        lto_valid, lang_to = self.check_language(self.ISO_LANG, languageTo)

        if not (lfr_valid and lto_valid):
            if self.settings["SELFBOT"]:
                await self.bot.say("Error Translating: language pair, wrong format or invalid language.".format(author.mention))
                return
            else:
                await self.bot.say("{} Error Translating: language pair, wrong format or invalid language. Check DM".format(author.mention))
                lenLang = len(self.ISO_LANG)
                done = 0
                msg = ""
                while (done < lenLang-1):
                    w=done+4
                    while (w > done):
                        msg = msg + "{} = {}, ".format(self.ISO_LANG[done][0], self.ISO_LANG[done][1])
                        done += 1
                    msg = msg + "\n"
                    if len(msg) > 1500:
                        msg = "\n```ISO language abbreviations:\n\n{}\n```".format(msg)
                        await self.bot.send_message(ctx.message.author, msg)
                        msg = ""
                    done += 1
        else:
            text = " ".join(text)
            result = await self.translate_text(lang_from, lang_to, text)

            if result == False:
                await self.bot.say("{} Error Translating...".format(author.mention))
            elif result != "":
                if self.settings["SELFBOT"]:
                    await self.bot.say("{}".format(result))
                else:
                    await self.bot.say("**» {}({}) **{}".format(author, lang_to.lower(), result))


    #@commands.command(pass_context=True, no_pm=True, hidden=True)
    async def systranslate(self, lang_from, lang_to, text, cachResult=True):
        #channel = ctx.channel.id
        #print(channel)
        #print(lang_from)
        #print(lang_to)
        #print(text)

        lang_from = lang_from.upper()
        lang_to = lang_to.upper()
        print(lang_from)
        print(lang_to)

        if text == "":
            return
        cached = None
        if lang_from == lang_to:
            return text

        langPair =  lang_from+lang_to
        if not langPair in self.cache:
            self.cache[langPair] = {}
        if langPair in self.cache:
            if text in self.cache[langPair]:
                cached = True
                # print("cached")
                return self.cache[langPair][text]
            else:
                cached = False
                # print("Not cached")

        print("\nSYSTRANSLATE")
        result = await self.translate_text(lang_from, lang_to, text)
        if result is False:
            # print("systranslate fail")
            return False
        #result = result.decode('utf8')
        replaceThis = [["** ", "**"], [" **", "**"], ["* ", "*"], [" *", "*"], ["~~ ", "~~"], [" ~~", "~~"], ["__ ", "__"], [" __", "__"], ["``` ", "```"], [" ```", "```"], ["` ", "`"], [" `", "`"], ["&#39;", "'"]]
        replacedResult = result
        for r in range(0, len(replaceThis)):
            replacedResult = replacedResult.replace(replaceThis[r][0], replaceThis[r][1])

        if cachResult and not cached:
            self.cache[langPair][text] = (replacedResult)
        fileIO(CACHE, "save", self.cache)
        return replacedResult


    async def translate_text(self, lang_from, lang_to, text):
        if text == ():
            return "empty"
        else:
            text = {"q":text}
            #print(text["q"])

            text = up.urlencode(text)
            #print(text)
            lang_from = lang_from.upper()
            lang_to = lang_to.upper()
            email = self.settings.get("EMAIL", None)

            if email is not None:
                search = ("http://api.mymemory.translated.net/get?{}&langpair={}|{}&de={}".format(text, lang_from, lang_to, email))
            else:
                search = ("http://api.mymemory.translated.net/get?{}&langpair={}|{}".format(text, lang_from, lang_to))

            translated = ""
            try:
                #print(search)
                async with aiohttp.get(search) as r:
                    result = await r.json()
                    # print("\nRESULT\n")
                    # print(result)
                    translated = result["matches"][0]["translation"]
            except Exception as e:
                print(e)
                return False
                translated = ""

            if translated != "":
                if self.settings["DEL_MSG"]:# Input replacement.
                    try:
                        await self.bot.delete_message(ctx.message)
                    except Exception as e:
                        # print("get")
                        if self.settings["NO_ERR"]:# Disables notification of permission denied 403
                            print("Translated: Missing permissions (403) @ {}({}).{}({})".format(ctx.message.server, ctx.message.server.id, ctx.message.channel, ctx.message.channel.id))
                return translated
            else:
                return False


    def check_language(self, lang_available, lang_check):
        availl_lang = len(lang_available)
        lang_check = lang_check.upper()
        for m in range(availl_lang):
            if lang_available[m][1] == lang_check:
                # print("RFC3066", True, lang_available[m][1])
                return True, lang_available[m][1]
            else:
                if lang_available[m][0].upper() == lang_check:
                    # print("Fullname", True, lang_available[m][1])
                    return True, lang_available[m][1]
                elif  ", " in lang_available[m][0]: # Deal with alliases
                    alias = lang_available[m][0].split(", ")
                    for a in alias:
                        if a.upper() == lang_check:
                            # print("Aliassed Fullname", True, lang_available[m][1])
                            return True, lang_available[m][1]
        return False, None


    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Moderator cmd
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @checks.admin_or_permissions(manage_server=True)
    @commands.group(pass_context=True)
    async def settr(self, ctx):
        """Magic OP commands for translated"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)


    @settr.command(pass_context=True, name="email", hidden=True)
    async def _set_email(self, ctx, email):
        """Free, anonymous 1000 words/day, Provide valid email and enjoy 10000 words/day."""
        if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
            self.settings["EMAIL"] = email
            fileIO(SETTINGS, "save", self.settings)
            await self.bot.say("Done..")
        else:
            await self.bot.say("Invalid")


    @settr.command(pass_context=True, name="cl", hidden=True)
    async def _set_cl(self, ctx, languageTo):
        """Set channel language"""
        await self.bot.say("placehlolder set channel language")


    @settr.command(pass_context=True, name="update")
    async def _update(self, ctx, languageTo):
        """Update a system translation."""
        lang_to = languageTo.upper()
        lang_pair =  "EN"+lang_to
        text_from = ""
        text_to = ""

        if not lang_pair in self.cache:
            await self.bot.say("langpar: {} does not exist, create? (y/n)".format(lang_pair))
            response = await self.bot.wait_for_message(author=ctx.message.author)
            response = response.content.lower().strip()
            if response == "y":
                self.cache[lang_pair] = {}
                fileIO(CACHE, "save", self.cache)
            else:
                await self.bot.say("Failed translation update.")
                return

        await self.bot.say("Please enter the static system value. (== to cancel).")
        response = await self.bot.wait_for_message(author=ctx.message.author)
        response = response.content.strip()
        if response == "==":
            await self.bot.say("Cancled translation update.")
            return
        elif response != "":
            text_from = response
        else:
            await self.bot.say("Failed translation update.")
            return

        await self.bot.say("Please enter the static system value (translated) (== to cancel).")
        response = await self.bot.wait_for_message(author=ctx.message.author)
        response = response.content.strip()
        if response == "==":
            await self.bot.say("cancled translation update.")
            return
        elif response != "":
            text_to = response
        else:
            await self.bot.say("Failed translation update.")
            return

        fromTo = text_from+" : "+text_to
        await self.bot.say("Please confirm the new static system translation value. (y/n).".format(fromTo))
        response = await self.bot.wait_for_message(author=ctx.message.author)
        response = response.content.lower().strip()
        if response == "y":
            self.cache[lang_pair][text_from] = (text_to)
            fileIO(CACHE, "save", self.cache)
            await self.bot.say("Done.")
            return
        elif response != "":
            text_to = response
        else:
            await self.bot.say("Failed translation update.")
            return


    @settr.command(pass_context=True, no_pm=False)
    async def _replace(self, ctx):
        """Toggle replace input for this channel on/off(req. bot permissions).
        Admin/owner restricted."""
        user = ctx.message.author
        chid = ctx.channel.id
        dmesf = None
        # Reset DEL_MSG.
        if chid not in self.settings["CHANNELS"]:
            self.settings["CHANNELS"].append(chid)
            self.settings["CHANNELS"][chid]["DEL_MSG"] = False
            if chid["DEL_MSG"] == False:
                dmesf = True
                self.settings[chid]["DEL_MSG"] = False
                #self.settings["DEL_MSG"].remove(a)
                await self.bot.say("{} ` DEL_MSG ON`".format(user.mention))
                return
        # Set DEL_MSG.
        if not dmesf:
            if ctx.message.channel not in self.settings["CHANNELS"]:
                self.settings["DEL_MSG"].append(ctx.message.channel.id)
                await self.bot.say("{} ` DEL_MSG OFF`".format(user.mention))
        fileIO(SETTINGS, "save", self.settings)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Set-up
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_folders():
    if not os.path.exists(DIR_DATA):
        print("Creating {} folder...".format(DIR_DATA))
        os.makedirs(DIR_DATA)


def check_files():
    settings = {"EMAIL": None, "CHANNELS": {}, "DEL_MSG" : False, "NO_ERR": False, "SELFBOT" : False}

    f = SETTINGS
    if not fileIO(f, "check"):
        print("Creating default translated settings.json...")
        fileIO(f, "save", settings)

    cache = {}

    f = CACHE
    if not fileIO(f, "check"):
        print("Creating translated cache.json...")
        fileIO(f, "save", cache)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Translated(bot))

