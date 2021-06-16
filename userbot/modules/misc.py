# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

from random import randint
from time import sleep
from os import execl
import asyncio
import sys
import os
import io
import sys
from userbot import ALIVE_NAME, UPSTREAM_REPO_URL, BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.utils import time_formatter
import urllib
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image


# Ported for Lynx-Userbot by @SyndicateTwenty4
# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# REPOLINK = str(UPSTREAM_REPO_URL) if UPSTREAM_REPO_URL else "https://github.com/KENZO-404/Lynx-Userbot"
# ============================================

opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.70 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """For .random command, get a random item from the list of items."""
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep ([0-9]+)$")
async def sleepybot(time):
    """For .sleep command, let the userbot snooze for a few second."""
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(event):
    """For .shutdown command, shut the bot down."""
    await event.edit("`Mematikan Lynx-Userbot....`")
    await asyncio.sleep(7)
    await event.delete()
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "`Lynx-Userbot Telah Dimatikan`")
    await bot.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def killdabot(event):
    await event.edit("`Restarting Lynx-Userbot...`")
    await asyncio.sleep(3)
    await event.delete()
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTARTBOT\n"
                                        "`Lynx-Userbot Reconnecting...`")
    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit(
        "Here's Something for You to Read :\n"
        "\n[⚡Lynx-Userbot⚡ Repo](https://github.com/KENZO-404/Lynx-Userbot/blob/Lynx-Userbot/README.md)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)")


@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """For .repo command, just returns the repo URL."""
    await wannasee.edit(
        "╭─━━━━━━━━━━━━━─╮\n"
        "                  ʀᴇᴘᴏ\n"
        "    [⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](https://kenzo-404.github.io/Lynx-Userbot)\n"
        "╭─━━━━━━━━━━━━━─╯\n"
        "│⊙ **Dᴇᴠᴇʟᴏᴘᴇʀ :** [ᴀxᴇʟ](https://github.com/KENZO-404)\n"
        "╰━━━━━━━━━━━━━━━╯\n"
        "  𝗟𝗶𝗰𝗲𝗻𝘀𝗲 : [GPL-3.0 License](https://github.com/KENZO-404/Lynx-Userbot/blob/Lynx-Userbot/LICENSE)"
    )


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`")



CMD_HELP.update({
    "random":
    "⚡𝘾𝙈𝘿⚡: `.random <item1> <item2> ... <itemN>`\
    \n↳ : Get a random item from the list of items.",
    "sleep":
    "⚡𝘾𝙈𝘿⚡: `.sleep <seconds>`\
    \n↳ : Let yours snooze for a few seconds.",
    "shutdown":
    "⚡𝘾𝙈𝘿⚡: `.shutdown`\
    \n↳ : Shutdown bot",
    "repo":
    "⚡𝘾𝙈𝘿⚡: `.repo`\
    \n↳ : Github Repo of this bot",
    "readme":
    "⚡𝘾𝙈𝘿⚡: `.readme`\
    \n↳ : Provide links to setup the userbot and it's modules.",
    "repeat":
    "⚡𝘾𝙈𝘿⚡: `.repeat <no> <text>`\
    \n↳ : Repeats the text for a number of times. Don't confuse this with spam tho.",
    "restart":
    "⚡𝘾𝙈𝘿⚡: `.restart`\
    \n↳ : Restarts the bot !!",
    "raw":
    "⚡𝘾𝙈𝘿⚡: `.raw`\
    \n↳ : Get detailed JSON-like formatted data about replied message."
})
