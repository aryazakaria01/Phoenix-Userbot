"""
   Heroku manager for your userbot
"""

import codecs
import heroku3
import aiohttp
import math
import os
import requests
import asyncio
import redis

from userbot import (
    HEROKU_APP_NAME,
    HEROKU_API_KEY,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    ALIVE_NAME)
from userbot.events import register

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


"""
   ConfigVars setting, get current var, set var or delete var...
"""


@register(outgoing=True,
          pattern=r"^.(get|del) var(?: |$)(\w*)")
async def variable(var):
    exe = var.pattern_match.group(1)
    if app is None:
        await var.edit("`[HEROKU]"
                       "\nHarap Siapkan`  **HEROKU_APP_NAME**.")
        return False
    if exe == "get":
        await var.edit("`ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ɪɴғᴏʀᴍᴀsɪ...`")
        variable = var.pattern_match.group(2)
        if variable != '':
            if variable in heroku_var:
                if BOTLOG:
                    await var.client.send_message(
                        BOTLOG_CHATID, "#ConfigVars\n\n"
                        "**Config Vars**:\n"
                        f"`{variable}` **=** `{heroku_var[variable]}`\n"
                    )
                    await var.edit("`ᴅɪᴛᴇʀɪᴍᴀ ᴋᴇ BOTLOG_CHATID...`")
                    return True
                else:
                    await var.edit("`ᴍᴏʜᴏɴ ᴜʙᴀʜ BOTLOG ᴋᴇ ᴛʀᴜᴇ...`")
                    return False
            else:
                await var.edit("`ɪɴғᴏʀᴍᴀsɪ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ...`")
                return True
        else:
            configvars = heroku_var.to_dict()
            msg = ''
            if BOTLOG:
                for item in configvars:
                    msg += f"`{item}` = `{configvars[item]}`\n"
                await var.client.send_message(
                    BOTLOG_CHATID, "#CONFIGVARS\n\n"
                    "**Config Vars**:\n"
                    f"{msg}"
                )
                await var.edit("`ᴅɪᴛᴇʀɪᴍᴀ ᴋᴇ BOTLOG_CHATID`")
                return True
            else:
                await var.edit("`ᴍᴏʜᴏɴ ᴜʙᴀʜ BOTLOG ᴋᴇ ᴛʀᴜᴇ`")
                return False
    elif exe == "del":
        await var.edit("`ᴍᴇɴɢʜᴀᴘᴜs ᴄᴏɴғɪɢ ᴠᴀʀs... 😼`")
        variable = var.pattern_match.group(2)
        if variable == '':
            await var.edit("`ᴍᴏʜᴏɴ ᴛᴇɴᴛᴜᴋᴀɴ ᴄᴏɴғɪɢ ᴠᴀʀs ʏᴀɴɢ ᴍᴀᴜ ᴀɴᴅᴀ ʜᴀᴘᴜs`")
            return False
        if variable in heroku_var:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID, "#ᴍᴇɴɢʜᴀᴘᴜsᴄᴏɴғɪɢᴠᴀʀs\n\n"
                    "**ᴍᴇɴɢʜᴀᴘᴜs ᴄᴏɴғɪɢ ᴠᴀʀs**:\n"
                    f"`{variable}`"
                )
            await var.edit("`ᴄᴏɴғɪɢ ᴠᴀʀs ᴛᴇʟᴀʜ ᴅɪʜᴀᴘᴜs`")
            del heroku_var[variable]
        else:
            await var.edit("`ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴄᴏɴғɪɢ ᴠᴀʀs, ᴋᴇᴍᴜɴɢᴋɪɴᴀɴ ᴛᴇʟᴀʜ ᴀɴᴅᴀ ʜᴀᴘᴜs.`")
            return True


@register(outgoing=True, pattern=r'^.set var (\w*) ([\s\S]*)')
async def set_var(var):
    await var.edit("`sᴇᴅᴀɴɢ ᴍᴇɴʏᴇᴛᴇʟ ᴄᴏɴғɪɢ ᴠᴀʀs ヅ`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    if variable in heroku_var:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#sᴇᴛᴇʟᴄᴏɴғɪɢᴠᴀʀs\n\n"
                "**ᴍᴇɴɢɢᴀɴᴛɪ ᴄᴏɴғɪɢ ᴠᴀʀs**:\n"
                f"`{variable}` = `{value}`"
            )
        await var.edit("`sᴇᴅᴀɴɢ ᴅɪ ᴘʀᴏsᴇs ʏᴀɴɢ ᴍᴜʟɪᴀ, ᴍᴏʜᴏɴ ᴍᴇɴᴜɴɢɢᴜ ᴅᴀʟᴀᴍ ʙᴇʙᴇʀᴀᴘᴀ ᴅᴇᴛɪᴋ 😼`")
    else:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴᴄᴏɴғɪɢᴠᴀʀ\n\n"
                "**ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴄᴏɴғɪɢ ᴠᴀʀs**:\n"
                f"`{variable}` **=** `{value}`"
            )
        await var.edit("`ʏᴀɴɢ ᴍᴜʟɪᴀ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴄᴏɴғɪɢ ᴠᴀʀs...`")
    heroku_var[variable] = value


"""
    ᴄʜᴇᴄᴋ ᴀᴄᴄᴏᴜɴᴛ ǫᴜᴏᴛᴀ, ʀᴇᴍᴀɪɴɪɴɢ ǫᴜᴏᴛᴀ, ᴜsᴇᴅ ǫᴜᴏᴛᴀ, ᴜsᴇᴅ ᴀᴘᴘ ǫᴜᴏᴛᴀ
"""


@register(outgoing=True, pattern=r"^.kuota(?: |$)")
async def dyno_usage(dyno):
    """
        ɢᴇᴛ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴅʏɴᴏ ᴜsᴀɢᴇ
    """
    await dyno.edit("⚡")
    await asyncio.sleep(1)
    useragent = (
        'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/81.0.4044.117 Mobile Safari/537.36'
    )
    user_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_API_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session:
        async with session.get(heroku_api + path, headers=headers) as r:
            if r.status != 200:
                await dyno.client.send_message(
                    dyno.chat_id,
                    f"`{r.reason}`",
                    reply_to=dyno.id
                )
                await dyno.edit("`ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ɪɴғᴏʀᴍᴀsɪ ᴅʏɴᴏ ᴀɴᴅᴀ 😿`")
                return False
            result = await r.json()
            quota = result['account_quota']
            quota_used = result['quota_used']

            """ - ᴜsᴇʀ ǫᴜᴏᴛᴀ ʟɪᴍɪᴛ ᴀɴᴅ ᴜsᴇᴅ - """
            remaining_quota = quota - quota_used
            percentage = math.floor(remaining_quota / quota * 100)
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)

            """ - ᴜsᴇʀ ᴀᴘᴘ ᴜsᴇᴅ ǫᴜᴏᴛᴀ - """
            Apps = result['apps']
            for apps in Apps:
                if apps.get('app_uuid') == app.id:
                    AppQuotaUsed = apps.get('quota_used') / 60
                    AppPercentage = math.floor(
                        apps.get('quota_used') * 100 / quota)
                    break
            else:
                AppQuotaUsed = 0
                AppPercentage = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)

            await dyno.edit(
                "╭┈─╼━━━━━━━━━━━━━━━╾─┈╮ \n"
                "│      ⇱ ⚡ᴘʜᴏᴇɴɪx-ᴜsᴇʀʙᴏᴛ⚡ ⇲ \n"
                "╭┈─╼━━━━━━━━━━━━━━━╾─┈╮ \n"
                "│📱◈ ᴘᴇɴɢɢᴜɴᴀᴀɴ ᴋᴜᴏᴛᴀ ᴀɴᴅᴀ : \n"
                f"│⏳◈ {AppHours} Jam - {AppMinutes} Menit. \n"
                f"│⚡◈ 𝐏𝐞𝐫𝐬𝐞𝐧𝐭𝐚𝐬𝐞 : {AppPercentage}% \n"
                "╰┈───────────────────┈╮ \n"
                "│📱◈ sɪsᴀ ᴋᴜᴏᴛᴀ ʙᴜʟᴀɴ ɪɴɪ : \n"
                f"│⏳◈ {hours} Jam - {minutes} Menit. \n"
                f"│⚡◈ ᴘʀᴇsᴇɴᴛᴀsᴇ : {percentage}% Lagi. \n"
                "╰┈───────────────────┈╯ \n"
                f"• Oᴡɴᴇʀ  : {ALIVE_NAME} \n"
            )
            await asyncio.sleep(20)
            await event.delete()
            return True


@register(outgoing=True, pattern=r"^\.logs")
async def _(dyno):
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await dyno.reply(
            "`Please make sure your Heroku API Key, Your App name are configured correctly in the heroku var.`"
        )
    await dyno.edit("`Sedang Mengambil Logs Anda Yang Mulia 😼`")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    fd = codecs.open("logs.txt", "r", encoding="utf-8")
    data = fd.read()
    key = (requests.post("https://nekobin.com/api/documents",
                         json={"content": data}) .json() .get("result") .get("key"))
    url = f"https://nekobin.com/raw/{key}"
    await dyno.edit(f"`Ini Logs Heroku Anda Yang Mulia :`\n\nPaste Ke: [Nekobin]({url})")
    return os.remove("logs.txt")


CMD_HELP.update({"herokuapp": "✘ Pʟᴜɢɪɴ : Heroku App"
                 "\n\n⚡𝘾𝙈𝘿⚡: `.kuota`"
                 "\n↳ : Check Quota Dyno Heroku"
                 "\n\n⚡𝘾𝙈𝘿⚡: `.set var <NEW VAR> <VALUE>`"
                 "\n↳ : Tambahkan Variabel Baru Atau Memperbarui Variabel"
                 "\nSetelah Menyetel Variabel Tersebut, Lynx-Userbot Akan Di Restart."
                 "\n\n⚡𝘾𝙈𝘿⚡: `.get var atau .get var <VAR>`"
                 "\n↳ : Dapatkan Variabel Yang Ada, !!PERINGATAN!! Gunakanlah Di Group Privasi Anda."
                 "\nIni Mengembalikan Semua Informasi Pribadi Anda, Harap berhati-hati."
                 "\n\n⚡𝘾𝙈𝘿⚡: `.del var <VAR>`"
                 "\n↳ : Menghapus Variabel Yang Ada"
                 "\nSetelah Menghapus Variabel, Bot Akan Di Restart."})
