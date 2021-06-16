# This is a troll indeed ffs *facepalm*
# Ported from xtra-telegram by @heyworld
import asyncio
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins
#from userbot.utils import admin_cmd
from userbot.events import register
from userbot import ALIVE_NAME, CMD_HELP, bot

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.fgban(?: |$)(.*)")
async def gbun(event):
    if event.fwd_from:
        return
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = f"`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By` {DEFAULTUSER}\n"
    no_reason = "No Reason Given "
    await event.edit("**Summoning out the mighty gban hammer ☠️**")
    asyncio.sleep(3.5)
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.from_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.from_id
        # make meself invulnerable cuz why not xD
        if idd == 1036951071:
            await reply_message.reply("`Wait a second, This is my master!`\n**How dare you threaten to ban my master nigger!**\n\n__Your account has been hacked! Pay 6969$ to my master__ [Heyworld](tg://user?id=1036951071) __to release your account__😏")
        else:
            jnl = ("`Warning!!`"
                   "[{}](tg://user?id={})"
                   f"` 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By` {DEFAULTUSER}\n\n"
                   "**Name: ** __{}__\n"
                   "**ID : ** `{}`\n"
                   ).format(firstname, idd, firstname, idd)
            if usname is None:
                jnl += "**Username: ** `Doesn't own a username!`\n"
            elif usname != "None":
                jnl += "**Username** : @{}\n".format(usname)
            if len(gbunVar) > 0:
                gbunm = "`{}`".format(gbunVar)
                gbunr = "**Reason: **" + gbunm
                jnl += gbunr
            else:
                jnl += no_reason
            await reply_message.reply(jnl)
    else:
        mention = (
            f"Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By {DEFAULTUSER} \nReason: No Reason Given. ")
        await event.reply(mention)
    await event.delete()

# Port by @VckyouuBitch (GeezProject)
# Language en to id from King-Userbot
# Installing in Lynx-Userbot
@register(outgoing=True, pattern="^.ftyping(?: |$)(.*)")
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Perintah salah`")
    await event.edit(f"`Memulai Pengetikan Palsu Untuk {t} Detik.`")
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(t)


@register(outgoing=True, pattern="^.faudio(?: |$)(.*)")
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Perintah salah`")
    await event.edit(f"`Memulai rekaman audio palsu Untuk {t} detik.`")
    async with event.client.action(event.chat_id, "record-audio"):
        await asyncio.sleep(t)


@register(outgoing=True, pattern="^.fvideo(?: |$)(.*)")
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Perintah salah`")
    await event.edit(f"`Memulai Perekaman Video Palsu Untuk {t} Detik.`")
    async with event.client.action(event.chat_id, "record-video"):
        await asyncio.sleep(t)


@register(outgoing=True, pattern="^.fgame(?: |$)(.*)")
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Perintah Salah.`")
    await event.edit(f"`Mulai Bermain Game Palsu Untuk {t} Detik.`")
    async with event.client.action(event.chat_id, "game"):
        await asyncio.sleep(t)


CMD_HELP.update({
    "fakeaction": "✘ Pʟᴜɢɪɴ : Fake Action\
    \n\n⚡𝘾𝙈𝘿⚡: `.fgban` <Reply> & <Alasan/Reason>\
    \n↳ : Melakukan Fake Global Banned.\
    \n\n⚡𝘾𝙈𝘿⚡: `.ftyping`\
    \n↳ : Seolah-olah Anda Sedang Mengetik Di Dalam Group, Padahal Tidak.\
    \n\n⚡𝘾𝙈𝘿⚡: `.faudio`\
    \n↳ : Seolah-olah Anda Sedang Mengirim Audio Di Dalam Group, Padahal Tidak.\
    \n\n⚡𝘾𝙈𝘿⚡: `.fvideo`\
    \n↳ : Seolah-olah Anda Sedang Mengirim Video Di Dalam Group, Padahal Tidak.\
    \n\n⚡𝘾𝙈𝘿⚡: `.fgame`\
    \n↳ : Seolah-olah Anda Sedang Memainkan Game Di Dalam Group, Padahal Tidak."})
