from .oboobs import oboobs
import asyncio
import aiohttp
import time
import random
import os
import sys


def setup(bot):
    if sys.version_info < (3, 5, 0):
        raise RuntimeError("Requires python >= 3.5")
    else:
bot.add_cog(oboobs(bot))
