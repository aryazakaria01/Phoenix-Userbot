# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Lynx Userbot
"""Userbot module containing commands related to the \
    Information Superhighway (yes, Internet)."""

import asyncio
import time
import redis

from datetime import datetime
from telethon import functions

from speedtest import Speedtest
from userbot import CMD_HELP, StartTime, ALIVE_NAME
from userbot.events import register
from userbot.utils import humanbytes 


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern="^.sping$")
async def redis(pong):
    """ For .ping command, ping the userbot from any chat.  """
    await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Connecting to server.__")
    await pong.edit("__Connecting to server..__")
    await pong.edit("__Connecting to server...__")
    await pong.edit("__Connecting to server.__")
    await pong.edit("__Connecting to server..__")
    await pong.edit("__Connecting to server...__")
    await pong.edit("__Connecting to server.__")
    await pong.edit("__Connecting to server..__")
    await pong.edit("__Connecting to server...__")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**╭━━━━━━━━━━━━━━━━━╮** \n"
                    f"**          - 𝐍 𝐄 𝐓 𝐖 𝐎 𝐑 𝐊 -** \n"
                    f"**   ▰▱▰▱▰▱▰▱▰▱▰▱** \n"
                    f"**        • ꜱɪɢɴᴀʟ  :** `%sms` \n"
                    f"**        • ᴏᴡɴᴇʀ   :** `{ALIVE_NAME}` \n"
                    f"**╰━━━━━━━━━━━━━━━━━╯** \n" % (duration))


@register(outgoing=True, pattern="^.lping$")
async def redis(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`Connecting to server...`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**`{ALIVE_NAME}`**\n"
                    f"✧ **-ꜱɪɢɴᴀʟ- :** "
                    f"`%sms` \n"
                    f"✧ **-ᴜᴘᴛɪᴍᴇ- :** "
                    f"`{uptime}` \n" % (duration))


@register(outgoing=True, pattern="^.xping$")
async def redis(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡**\n"
                    f"➾ __Signal__    __:__ "
                    f"`%sms` \n"
                    f"➾ __Uptime__ __:__ "
                    f"`{uptime}` \n" % (duration))


@register(outgoing=True, pattern="^.ping$")
async def redis(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("⚡")
    await asyncio.sleep(2)
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**╭─━━━━━━━━━━━━━━━─╮** \n"
                    f"**       ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡** \n"
                    f"**╭─━━━━━━━━━━━━━━━─╯** \n"
                    f"**│⊙  Sɪɢɴᴀʟ   :** "
                    f"`%sms` \n"
                    f"**│⊙  Uᴘᴛɪᴍᴇ  :** "
                    f"`{uptime}` \n"
                    f"**│⊙  Oᴡɴᴇʀ   :** `{ALIVE_NAME}` \n"
                    f"**╰━━━━━━━━━━━━━━━━━╯**" % (duration))


# Port WeebProject
@register(outgoing=True, pattern=r"^\.speedtest$")
async def speedtst(spd):
    """For .speed command, use SpeedTest to check server speeds."""
    await spd.edit("`Running speed test...`")

    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    msg = (
        f"**Started at {result['timestamp']}**\n\n"
        "**Client**\n"
        f"**ISP :** `{result['client']['isp']}`\n"
        f"**Country :** `{result['client']['country']}`\n\n"
        "**Server**\n"
        f"**Name :** `{result['server']['name']}`\n"
        f"**Country :** `{result['server']['country']}`\n"
        f"**Sponsor :** `{result['server']['sponsor']}`\n\n"
        f"**Ping :** `{result['ping']}`\n"
        f"**Upload :** `{humanbytes(result['upload'])}/s`\n"
        f"**Download :** `{humanbytes(result['download'])}/s`"
    )

    await spd.delete()
    await spd.client.send_file(
        spd.chat_id,
        result["share"],
        caption=msg,
        force_document=False,
    )


@register(outgoing=True, pattern=r"^\.dc$")
async def neardc(event):
    """For .dc command, get the nearest datacenter information."""
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(
        f"Country : `{result.country}`\n"
        f"Nearest Datacenter : `{result.nearest_dc}`\n"
        f"This Datacenter : `{result.this_dc}`"
    )


@register(outgoing=True, pattern="^.pong$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("⚡")
    await asyncio.sleep(1)
    await pong.edit("😼")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit(f"**🙅 Oᴡɴᴇʀ : {ALIVE_NAME}**\n`%sms`" % (duration))


CMD_HELP.update({
        "speedtest": "✘ Pʟᴜɢɪɴ : `Speed Test`\
         \n\n⚡𝘾𝙈𝘿⚡: `.ping` | `.lping` | `.xping` | `.sping`\
         \n↳ : Untuk Menunjukkan Ping Bot Anda.\
         \n\n⚡𝘾𝙈𝘿⚡: `.pong`\
         \n↳ : Sama Seperti Perintah Ping.\
         \n\n⚡𝘾𝙈𝘿⚡: `.speedtest`\
         \n↳ : Untuk Menunjukkan Kecepatan Jaringan Anda.\
         \n\n⚡𝘾𝙈𝘿⚡: `.dc`\
         \n↳ : Menemukan Server Dari Datacenter Kamu."})
