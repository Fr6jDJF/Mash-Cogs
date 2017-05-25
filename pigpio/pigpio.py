import discord
from discord.ext import commands
import RPi.GPIO as GPIO
import asyncio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)        #LED output pin


# UNTESTED #
class MentionAlarm:
    """Mention alerm"""

    def __init__(self, bot):
        self.bot = bot
        self.alarm_check_interval = 5
        # serverid/channelid/userid
        self.notificate = {"54646161561891984" : {
                                        "196481694161616" : ["75787865786786"]
                                    },
                                }

    def get_channel_object(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        if channel and \
                channel.permissions_for(channel.server.me).send_messages:
            return channel
        return None
        
    def get_user_object(self, user_id):
        all_members = self.bot.get_all_members()
        for member in all_members:
            if member.id == user_id:
            return member
        return None        

    async def check_alarm(self):   
        await self.bot.wait_until_ready()
        while self == self.bot.get_cog('MentionAlarm:'):
            i = GPIO.input(11)
            if i == 0:# When output from Alarm is LOW
                GPIO.output(3, 0)  #Turn OFF LED
                await asyncio.sleep(0.1)
            elif i == 1:# When output from Alarm is HIGH
                for server in self.notificate
                    for chan_id in servers[server]:
                        for user_id in servers[server][chan_id]:
                            channel = self.get_channel_object(chan_id)
                            user = get_user_object(user_id)
                            if channel is None:
                                print("response channel not found, continuing")
                                continue
                            msg = "{} Intruder detected {}".format(user.mention, i)
                            if msg is not None:
                                await self.bot.send_message(channel, msg)
                                #await send_file(channel, fp, filename="./Intruder20170525.mp4")# Video must be less than 8MB
                GPIO.output(3, 1)# Turn ON LED
                await asyncio.sleep(0.1)
            await asyncio.sleep(self.alarm_check_interval)# Spare some time for other tasks :)

def setup(bot):
    n = MentionAlarm(bot)
    bot.add_cog(n)
    bot.loop.create_task(n.check_alarm())

    
