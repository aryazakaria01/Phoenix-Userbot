# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for keeping control who PM you."""

import os
import time
import asyncio
import io
from sqlalchemy.exc import IntegrityError
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User
from telethon import events, errors, functions, types

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    COUNT_PM,
    LASTMSG,
    LOGS,
    PM_AUTO_BAN,
    ALIVE_NAME,
    CUSTOM_PMPERMIT_TEXT,
)
from userbot.events import register


PM_PERMIT_PIC = os.environ.get("PM_PERMIT_PIC", None)
if PM_PERMIT_PIC is None:
  WARN_PIC = "resource/logo/LynxUserbot-Button.jpg"
else:
  WARN_PIC = PM_PERMIT_PIC

COUNT_PM = {}
LASTMSG = {}

# ========================= CONSTANTS ============================

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
CUSTOM_MIDDLE_PMP = str(CUSTOM_PMPERMIT_TEXT) if CUSTOM_PMPERMIT_TEXT else f"│ᴋᴀʀᴇɴᴀ sᴀʏᴀ ᴀᴋᴀɴ ᴏᴛᴏᴍᴀᴛɪs ᴍᴇᴍʙʟᴏᴋɪʀ\n│ᴀɴᴅᴀ, ᴛᴜɴɢɢᴜ sᴀᴍᴘᴀɪ {DEFAULTUSER}\n│ᴍᴇɴᴇʀɪᴍᴀ ᴘᴇsᴀɴ ᴀɴᴅᴀ, ᴛᴇʀɪᴍᴀᴋᴀsɪʜ.\n" 
DEF_UNAPPROVED_MSG = (
    "◄┈─╼━━━━━━━━━━━━━━━━━━╾─┈╮\n"
    "ㅤ  “ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇ.”\n"
    "╭┈─╼━━━━━━━━━━━━━━━━━━╾─┈╯\n"
    "│❗ᴅɪʟᴀʀᴀɴɢ ᴍᴇʟᴀᴋᴜᴋᴀɴ sᴘᴀᴍ❗\n│\n"
    f"{CUSTOM_MIDDLE_PMP}│\n"
    "╰┈─────────────────────┈─➤\n"
    "▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n"
    "┣[○› `pesan otomatis`\n"
    f"┣[○› `ᴏʟᴇʜ` © @Badboyanim\n"
    "▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱")

# =================================================================


@register(incoming=True, disable_edited=True, disable_errors=True)
async def permitpm(event):
    """Prohibits people from PMing you without approval. \
        Will block retarded nibbas automatically."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not (await event.get_sender()).bot
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import is_approved
        except AttributeError:
            return
        apprv = is_approved(event.chat_id)
        notifsoff = gvarstatus("NOTIF_OFF")

        # Use user custom unapproved message
        getmsg = gvarstatus("unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
            WARN_PIC = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG
            WARN_PIC = PM_PERMIT_PIC
        # This part basically is a sanity check
        # If the message that sent before is Unapproved Message
        # then stop sending it again to prevent FloodHit
        if not apprv and event.text != UNAPPROVED_MSG:
            if event.chat_id in LASTMSG:
                prevmsg = LASTMSG[event.chat_id]
                # If the message doesn't same as previous one
                # Send the Unapproved Message again
                if event.text != prevmsg:
                    async for message in event.client.iter_messages(
                        event.chat_id, from_user="me", search=UNAPPROVED_MSG, file=WARN_PIC
                    ):
                        await message.delete()
                    await event.reply(f"{WARN_PIC}\n\n{UNAPPROVED_MSG}")
            else:
                await event.reply(f"{WARN_PIC}\n\n{UNAPPROVED_MSG}")
            LASTMSG.update({event.chat_id: event.text})
            if notifsoff:
                await event.client.send_read_acknowledge(event.chat_id)
            if event.chat_id not in COUNT_PM:
                COUNT_PM.update({event.chat_id: 1})
            else:
                COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

            if COUNT_PM[event.chat_id] > 4:
                await event.respond(
                    "`ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪ ʙʟᴏᴋɪʀ ᴋᴀʀɴᴀ ᴍᴇʟᴀᴋᴜᴋᴀɴ sᴘᴀᴍ ᴘᴇsᴀɴ`\n"
                    "`ᴋᴇ ʀᴏᴏᴍ ᴄʜᴀᴛ sᴀʏᴀ 😼`"
                )

                try:
                    del COUNT_PM[event.chat_id]
                    del LASTMSG[event.chat_id]
                except KeyError:
                    if BOTLOG:
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "ᴍᴏʜᴏɴ ᴍᴀᴀғ, ᴛᴇʟᴀʜ ᴛᴇʀᴊᴀᴅɪ ᴍᴀsᴀʟᴀʜ sᴀᴀᴛ ᴍᴇɴɢʜɪᴛᴜɴɢ ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇ, ᴍᴏʜᴏɴ ʀᴇsᴛᴀʀᴛ sᴀʏᴀ 😿 !",
                        )
                    return LOGS.info("CountPM wen't rarted boi")

                await event.client(BlockRequest(event.chat_id))
                await event.client(ReportSpamRequest(peer=event.chat_id))

                if BOTLOG:
                    name = await event.client.get_entity(event.chat_id)
                    name0 = str(name.first_name)
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "["
                        + name0
                        + "](tg://user?id="
                        + str(event.chat_id)
                        + ")"
                        + " ᴛᴇʟᴀʜ ᴅɪʙʟᴏᴋɪʀ ᴋᴀʀɴᴀ ᴍᴇʟᴀᴋᴜᴋᴀɴ sᴘᴀᴍ ᴋᴇ ʀᴏᴏᴍ ᴄʜᴀᴛ",
                    )


@register(disable_edited=True, outgoing=True, disable_errors=True)
async def auto_accept(event):
    """ᴡɪʟʟ ᴀᴘᴘʀᴏᴠᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɪғ ʏᴏᴜ ᴛᴇxᴛᴇᴅ ᴛʜᴇᴍ ғɪʀsᴛ."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not (await event.get_sender()).bot
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import approve, is_approved
        except AttributeError:
            return

        # Use user custom unapproved message
        get_message = gvarstatus("unapproved_msg")
        if get_message is not None:
            UNAPPROVED_MSG = get_message
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG
        chat = await event.get_chat()
        if isinstance(chat, User):
            if is_approved(event.chat_id) or chat.bot:
                return
            async for message in event.client.iter_messages(
                event.chat_id, reverse=True, limit=1
            ):
                if (
                    message.text is not UNAPPROVED_MSG
                    and message.from_id == self_user.id
                ):
                    try:
                        approve(event.chat_id)
                    except IntegrityError:
                        return

                if is_approved(event.chat_id) and BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇᴅ\n"
                        + "User : "
                        + f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@register(outgoing=True, pattern=r"^\.notifoff$")
async def notifoff(noff_event):
    """For .notifoff command, stop getting notifications from unapproved PMs."""
    try:
        from userbot.modules.sql_helper.globals import addgvar
    except AttributeError:
        return await noff_event.edit("`ʀᴜɴɴɪɴɢ ᴏɴ ɴᴏɴ-sǫʟ ᴍᴏᴅᴇ!`")
    addgvar("NOTIF_OFF", True)
    await noff_event.edit("#ɴᴏᴛɪғ ᴏғғ ❌\n`ɴᴏᴛɪғɪᴋᴀsɪ ᴅᴀʀɪ ᴘᴇsᴀɴ ᴘʀɪʙᴀᴅɪ ᴛᴇʟᴀʜ ᴅɪɴᴏɴᴀᴋᴛɪғᴋᴀɴ.`")


@register(outgoing=True, pattern=r"^\.notifon$")
async def notifon(non_event):
    """For .notifoff command, get notifications from unapproved PMs."""
    try:
        from userbot.modules.sql_helper.globals import delgvar
    except AttributeError:
        return await non_event.edit("`ʀᴜɴɴɪɴɢ ᴏɴ ɴᴏɴ-sǫʟ ᴍᴏᴅᴇ!`")
    delgvar("NOTIF_OFF")
    await non_event.edit("#NOTIF ON ☑️\n`ɴᴏᴛɪғɪᴋᴀsɪ ᴅᴀʀɪ ᴘᴇsᴀɴ ᴘʀɪʙᴀᴅɪ ᴛᴇʟᴀʜ ᴅɪᴀᴋᴛɪғᴋᴀɴ.`")


@register(outgoing=True, pattern=r"^\.(?:setuju|ok)\s?(.)?")
async def approvepm(apprvpm):
    """For .ok command, give someone the permissions to PM you."""
    try:
        from userbot.modules.sql_helper.globals import gvarstatus
        from userbot.modules.sql_helper.pm_permit_sql import approve
    except AttributeError:
        return await apprvpm.edit("`ʀᴜɴɴɪɴɢ ᴏɴ ɴᴏɴ-sǫʟ ᴍᴏᴅᴇ!`")

    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        replied_user = await apprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id

    else:
        aname = await apprvpm.client.get_entity(apprvpm.chat_id)
        name0 = str(aname.first_name)
        uid = apprvpm.chat_id

    # Get user custom msg
    getmsg = gvarstatus("unapproved_msg")
    if getmsg is not None:
        UNAPPROVED_MSG = getmsg
    else:
        UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

    async for message in apprvpm.client.iter_messages(
        apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG
    ):
        await message.delete()

    try:
        approve(uid)
    except IntegrityError:
        return await apprvpm.edit("⚡")

    await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `ᴘᴇsᴀɴ ᴀɴᴅᴀ sᴜᴅᴀʜ ᴅɪᴛᴇʀɪᴍᴀ` ☑️")
    await apprvpm.delete(getmsg)
    await message.delete()

    if BOTLOG:
        await apprvpm.client.send_message(
            BOTLOG_CHATID,
            "#ᴅɪᴛᴇʀɪᴍᴀ\n" + "User: " + f"[{name0}](tg://user?id={uid})"
        )


@register(outgoing=True, pattern=r"^\.(?:ᴛᴏʟᴀᴋ|ɴᴏᴘᴍ)\s?(.)?")
async def disapprovepm(disapprvpm):
    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove
    except BaseException:
        return await disapprvpm.edit("`ʀᴜɴɴɪɴɢ ᴏɴ ɴᴏɴ-sǫʟ ᴍᴏᴅᴇ!`")

    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        dissprove(aname)
    else:
        dissprove(disapprvpm.chat_id)
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        name0 = str(aname.first_name)

    await disapprvpm.edit(
        f"`ᴍᴀᴀғ` [{name0}](tg://user?id={disapprvpm.chat_id}) `ᴘᴇsᴀɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪᴛᴏʟᴀᴋ, ᴍᴏʜᴏɴ ᴊᴀɴɢᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ sᴘᴀᴍ ᴋᴇ ʀᴏᴏᴍ ᴄʜᴀᴛ!`"
    )

    if BOTLOG:
        await disapprvpm.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={disapprvpm.chat_id})"
            " `ʙᴇʀʜᴀsɪʟ ᴅɪᴛᴏʟᴀᴋ` !",
        )


@register(outgoing=True, pattern=r"^\.block$")
async def blockpm(block):
    """For .block command, block people from PMing you!"""
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        await block.client(BlockRequest(aname))
        await block.edit("`ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪʙʟᴏᴋɪʀ ᴏʟᴇʜ sᴀʏᴀ !`")
        uid = replied_user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        await block.edit("`ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪʙʟᴏᴋɪʀ ᴏʟᴇʜ sᴀʏᴀ !`")
        name0 = str(aname.first_name)
        uid = block.chat_id

    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove

        dissprove(uid)
    except AttributeError:
        pass

    if BOTLOG:
        await block.client.send_message(
            BOTLOG_CHATID,
            "#ʙʟᴏᴋɪʀ\n" + "User : " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern=r"^\.unblock$")
async def unblockpm(unblock):
    """For .unblock command, let people PMing you again!"""
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.from_id)
        name0 = str(replied_user.first_name)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit("`ᴀɴᴅᴀ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴅɪʙʟᴏᴋɪʀ ʟᴀɢɪ.`")

    if BOTLOG:
        await unblock.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={replied_user.id})" "ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʟᴀɢɪ ᴅɪʙʟᴏᴋɪʀ.",
        )


@register(outgoing=True, pattern=r"^.(sᴇᴛ|ɢᴇᴛ|ʀᴇsᴇᴛ) pm_msg(?: |$)(\w*)")
async def add_pmsg(cust_msg):
    """Set your own Unapproved message"""
    if not PM_AUTO_BAN:
        return await cust_msg.edit("**ᴍᴏʜᴏɴ ᴍᴀᴀғ, ᴀɴᴅᴀ ʜᴀʀᴜs ᴍᴇɴʏᴇᴛᴇʟ** `PM_AUTO_BAN` **ᴋᴇ** `True`\n sɪʟᴀʜᴋᴀɴ ʟᴀᴋᴜᴋᴀɴ sᴇᴛ ᴠᴀʀ.\nUsage : `.set var PM_AUTO_BAN True`")
    try:
        import userbot.modules.sql_helper.globals as sql
    except AttributeError:
        await cust_msg.edit("`ʀᴜɴɴɪɴɢ ᴏɴ ɴᴏɴ-sǫʟ ᴍᴏᴅᴇ!`")
        return

    await cust_msg.edit("`sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...`")
    conf = cust_msg.pattern_match.group(1)

    custom_message = sql.gvarstatus("unapproved_msg")

    if conf.lower() == "set":
        message = await cust_msg.get_reply_message()
        status = "Pesan"

        # check and clear user unapproved message first
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            status = "Pesan"

        if message:
            msg = message.message  # get the plain text
            sql.addgvar("unapproved_msg", msg)
        else:
            return await cust_msg.edit("`ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ`")

        await cust_msg.edit("#sᴇᴛᴛɪɴɢs ☑️\n`ᴘᴇsᴀɴ ʙᴇʀʜᴀsɪʟ ᴅɪsɪᴍᴘᴀɴ ᴋᴇ ʀᴏᴏᴍ ᴄʜᴀᴛ.`")

        if BOTLOG:
            await cust_msg.client.send_message(
                BOTLOG_CHATID, f"**{status} ᴘᴍ ʏᴀɴɢ ᴛᴇʀsɪᴍᴘᴀɴ ᴅᴀʟᴀᴍ ʀᴏᴏᴍ ᴄʜᴀᴛ ᴀɴᴅᴀ :** \n\n{msg}"
            )

    if conf.lower() == "reset":
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            await cust_msg.edit("#ᴅᴇʟᴇᴛᴇ ☑️\n`ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇsᴀɴ ᴄᴜsᴛᴏᴍ ᴘᴍ ᴋᴇ ᴅᴇғᴀᴜʟᴛ.`")
        else:

            await cust_msg.edit("`ᴘᴇsᴀɴ ᴘᴍ ᴀɴᴅᴀ sᴜᴅᴀʜ ᴅᴇғᴀᴜʟᴛ sᴇᴊᴀᴋ ᴀᴡᴀʟ.`")

    if conf.lower() == "get":
        if custom_message is not None:
            await cust_msg.edit(
                f"**ɪɴɪ ᴀᴅᴀʟᴀʜ ᴘᴇsᴀɴ ᴘᴍ ʏᴀɴɢ sᴇᴋᴀʀᴀɴɢ ᴅɪᴋɪʀɪᴍᴋᴀɴ ᴋᴇ ʀᴏᴏᴍ ᴄʜᴀᴛ ᴀɴᴅᴀ :**\n\n{custom_message}"
            )
        else:
            await cust_msg.edit(
                "*ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇɴʏᴇᴛᴇʟ ᴘᴇsᴀɴ ᴘᴍ*\n"
                f"ᴍᴀsɪʜ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴘᴇsᴀɴ ᴘᴍ ᴅᴇғᴀᴜʟᴛ : \n\n`{DEF_UNAPPROVED_MSG}`"
            )



CMD_HELP.update(
    {
        "pmpermit": "✘ Pʟᴜɢɪɴ : Private Message Permite"
        "\n\n⚡𝘾𝙈𝘿⚡: `.setuju | .ok`"
        "\n↳ : Menerima Pesan Seseorang Dengan Cara Balas Pesannya Atau Tag dan Juga Untuk Dilakukan Di PM."
        "\n\n⚡𝘾𝙈𝘿⚡: `.tolak | .nopm`"
        "\n↳ : Menolak Pesan Seseorang Dengan Cara Balas Pesannya Atau Tag dan Juga Untuk Dilakukan Di PM."
        "\n\n⚡𝘾𝙈𝘿⚡: `.block`"
        "\n↳ : Memblokir Orang Di PM."
        "\n\n⚡𝘾𝙈𝘿⚡: `.unblock`"
        "\n↳ : Membuka Blokir."
        "\n\n⚡𝘾𝙈𝘿⚡: `.notifoff`"
        "\n↳ : Menonaktifkan Notifikasi Pesan Yang Belum Diterima."
        "\n\n⚡𝘾𝙈𝘿⚡: `.notifon`"
        "\n↳ : Mengaktifkan Notifikasi Pesan Yang Belum Diterima."
        "\n\n⚡𝘾𝙈𝘿⚡: `.set pm_msg` <Reply Message>"
        "\n↳ : Menyetel Pesan Pribadimu Untuk Orang Yang Pesannya Belum Diterima."
        "\n\n⚡𝘾𝙈𝘿⚡: `.get pm_msg`"
        "\n↳ : Mendapatkan Custom Pesan PM-Mu."
        "\n\n⚡𝘾𝙈𝘿⚡: `.reset pm_msg`"
        "\n↳ : Menghapus Pesan PM ke Default."
        "\n\nPesan Pribadi Yang Belum Diterima Saat Ini Tidak Dapat Disetel"
        "\nke Teks Format. Seperti : Bold, Underline, Link, dll."
        "\nPesan Akan Terkirim Normal Saja."})
