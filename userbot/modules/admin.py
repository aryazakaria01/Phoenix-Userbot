# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChannelParticipantsBots,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
    PeerChat,
)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Gambar Terlalu Kecil`"
PP_ERROR = "`Terjadi Kesalahan, Gagal Memprosess Gambar.`"
NO_ADMIN = "`Mohon Maaf, Anda Bukan Admin.`"
NO_PERM = "`Anda Tidak Mempunyai Izin!`"
NO_SQL = "`Berjalan Pada Mode Non-SQL`"

CHAT_PP_CHANGED = "`Berhasil Mengubah Profil Grup`"
CHAT_PP_ERROR = (
    "`Terjadi Kesalahan Saat Memperbarui Foto,`"
    "`Mungkin Anda Bukan Admin,`"
    "`Atau Tidak Mempunyai Izin.`"
)
INVALID_MEDIA = "`Media Tidak Valid.`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@register(outgoing=True, pattern=r"^\.setgpic$")
async def set_group_photo(gpic):
    if not gpic.is_group:
        await gpic.edit("`Mohon Maaf, Lakukan Perintah Ini Di Group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        return await gpic.edit(NO_ADMIN)

    if replymsg and replymsg.media:
        await gpic.edit("`Mengubah Profile Group.`")
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern=r"^\.promote(?: |$)(.*)")
async def promote(promt):
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        return await promt.edit(NO_ADMIN)

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    await promt.edit("`Sedang Mempromosikan Pengguna Ini Sebagai Admin.\nMohon Tunggu...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Admin"  # Just in case.
    if not user:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Berhasil Mempromosikan Pengguna Ini Sebagai Admin. ☑️`")
        await sleep(5)
        await promt.delete()

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        return await promt.edit(NO_PERM)

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOSI\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {promt.chat.title}(`{promt.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.demote(?: |$)(.*)")
async def demote(dmod):
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await dmod.edit(NO_ADMIN)

    # If passing, declare that we're going to demote
    await dmod.edit("`Melakukan Pelepasan Admin.\nMohon Tunggu...`")
    rank = "Admin"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        return await dmod.edit(NO_PERM)
    await dmod.edit("`Behasil, Pengguna Ini Sudah Dilepas Sebagai Admin. ☑️`")
    await sleep(5)
    await dmod.delete()

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#MENURUNKAN\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.ban(?: |$)(.*)")
async def ban(bon):
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await bon.edit(NO_ADMIN)

    user, reason = await get_user_from_event(bon)
    if not user:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Sedang Melakukan Banned!\nMohon Tunggu...`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await bon.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await bon.edit(
            "`Saya Tidak Memiliki Hak Pesan Nuking! Tapi Tetap Saja Dia di Banned!`"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.edit(
            f"`PENGGUNA:` [{user.first_name}](tg://user?id={user.id})\n`ID:` `{str(user.id)}` Telah Di Banned !!\n`Alasan:` {reason}"
        )
    else:
        await bon.edit(
            f"`PENGGUNA:` [{user.first_name}](tg://user?id={user.id})\n`ID:` `{str(user.id)}` Telah Di Banned !"
        )
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {bon.chat.title}(`{bon.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.unban(?: |$)(.*)")
async def nothanos(unbon):
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await unbon.edit(NO_ADMIN)

    # If everything goes well...
    await unbon.edit("`Sedang Melakukan Unbanned!\nMohon Tunggu...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return

    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Unbanned Berhasil. ☑️```")
        await sleep(3)
        await unbon.delete()

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await unbon.edit("`Sepertinya Terjadi Kesalahan!`")


@register(outgoing=True, pattern=r"^\.mute(?: |$)(.*)")
async def spider(spdr):
    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await spdr.edit(NO_SQL)

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await spdr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(spdr)
    if not user:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        return await spdr.edit(
            "`Tangan Terlalu Pendek, Tidak Bisa Membisukan Diri Sendiri...\n(ヘ･_･)ヘ┳━┳`"
        )

    # If everything goes well, do announcing and mute
    await spdr.edit("`Telah Dibisukan!`")
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit("`Error! Pengguna Sudah Dibisukan.`")
    else:
        try:
            await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await spdr.edit(f"#MUTE\n• **Alasan:** `{reason}`")
            else:
                await spdr.edit("`Telah Dibisukan!`")

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID,
                    "#MUTE\n"
                    f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                    f"GRUP: {spdr.chat.title}(`{spdr.chat_id}`)",
                )
        except UserIdInvalidError:
            return await spdr.edit("`Terjadi Kesalahan!`")


@register(outgoing=True, pattern=r"^\.unmute(?: |$)(.*)")
async def unmoot(unmot):
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await unmot.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await unmot.edit(NO_SQL)

    # If admin or creator, inform the user and start unmuting
    await unmot.edit("```Melakukan Unmute!```")
    user = await get_user_from_event(unmot)
    user = user[0]
    if not user:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`Kesalahan! Pengguna Sudah Tidak Dibisukan.`")
    else:

        try:
            await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit("```Berhasil Melakukan Unmute! Pengguna Sudah Tidak Lagi Dibisukan```")
            await sleep(3)
            await unmot.delete()
        except UserIdInvalidError:
            return await unmot.edit("`Terjadi Kesalahan!`")

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unmot.chat.title}(`{unmot.chat_id}`)",
            )


@register(incoming=True)
async def muter(moot):
    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(
                    EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                )
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@register(outgoing=True, pattern=r"^\.zombies(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Tidak Menemukan Akun Terhapus, Group Sudah Bersih.`"

    if con != "clean":
        await show.edit("`Mencari Akun Hantu/Terhapus/Zombie...`")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"Menemukan **{del_u}** Akun Hantu/Terhapus/Zombie Dalam Group Ini,"
                "\nGunakan Perintah `.zombies clean` Untuk Membersihkan Group.")
        return await show.edit(del_status)

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await show.edit("`Mohon Maaf, Anda Bukan Admin Disini.`")

    await show.edit("`Menghapus Akun Terhapus...\nMohon Menunggu, Sedang Dalam Prosess.`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit("`Lord Tidak Memiliki Izin Banned Dalam Grup Ini`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Membersihkan **{del_u}** `Akun Terhapus`"

    if del_a > 0:
        del_status = (
            f"Membersihkan **{del_u}** Akun Terhapus"
            f"\n**{del_a}** `Admin Akun Terhapus Tidak Bisa Dihapus.`"
        )
    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#MEMBERSIHKAN\n"
            f"Membersihkan **{del_u}** Akun Terhapus!"
            f"\nGRUP: {show.chat.title}(`{show.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.admins$")
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = f"<b>{title}\nList of Admins In This Group :</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n╰> {link}"
            else:
                mentions += f"\nAkun Terhapus <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern=r"^\.pin(?: |$)(.*)")
async def pin(msg):
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await msg.edit(NO_ADMIN)

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        return await msg.edit("`Mohon Reply Ke Pesan Untuk Melakukan Pin.`")

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        return await msg.edit(NO_PERM)

    await msg.edit("`Berhasil Melakukan Pin.`")
    await sleep(2)
    await msg.delete()

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"NOTIF: {not is_silent}",
        )


@register(outgoing=True, pattern=r"^\.kick(?: |$)(.*)")
async def kick(usr):
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await usr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(usr)
    if not user:
        return await usr.edit("`Tidak Dapat Menemukan Pengguna.`")

    await usr.edit("`Sedang Melakukan Kick...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        return await usr.edit(NO_PERM + f"\n{str(e)}")

    if reason:
        await usr.edit(
            f"#KickOut\n**Pengguna :** [{user.first_name}](tg://user?id={user.id})\n**Alasan :** `{reason}`"
        )
    else:
        await usr.edit(f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**")
        await sleep(5)
        await usr.delete()

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KickOut\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GROUP: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@register(outgoing=True, pattern=r"^\.users ?(.*)")
async def get_users(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = "Pengguna Di {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nAkun Terhapus `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nAkun Terhapus `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit("Yang Mulia, Grup Ini Terlalu Besar Mengunggah Daftar Pengguna Sebagai File.")
        file = open("daftarpengguna.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "daftarpengguna.txt",
            caption="Pengguna Dalam Grup {}".format(title),
            reply_to=show.id,
        )
        remove("daftarpengguna.txt")


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("`Ketik Username Atau Reply Ke Pesan Pengguna.`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@register(outgoing=True, pattern=r"^\.usersdel ?(.*)")
async def get_usersdel(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = "Akun Terhapus Di {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        #       else:
        #                mentions += f"\nAkun Terhapus `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        #       else:
    #              mentions += f"\nAkun Terhapus `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Yang Mulia, Group Ini Terlalu Besar, Mengunggah Daftar Akun Terhapus Sebagai File."
        )
        file = open("daftarpengguna.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "daftarpengguna.txt",
            caption="Daftar Pengguna {}".format(title),
            reply_to=show.id,
        )
        remove("daftarpengguna.txt")


async def get_userdel_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("`Ketik username Atau Reply Ke Pengguna!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@register(outgoing=True, pattern=r"^\.bots$", groups_only=True)
async def get_bots(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = f"<b>Daftar Bot Di {title}:</b>\n"
    try:
        if isinstance(show.to_id, PeerChat):
            return await show.edit("`Saya Mendengar, Bahwa Hanya Supergrup Yang Dapat Memiliki Bot.`")
        else:
            async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots
            ):
                if not user.deleted:
                    link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nBot Terhapus <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit("Mohon Maaf, Terlalu Banyak Bot Di Group Ini, Mengunggah Daftar Bot Sebagai File.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption="Daftar Bot Di {}".format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")


@register(outgoing=True, pattern="^.allkick(?: |$)(.*)")
async def allkick(event):
    lynxuser = await event.get_chat()
    lynxget = await event.client.get_me()
    admin = lynxuser.admin_rights
    creator = lynxuser.creator
    if not admin and not creator:
        await event.edit("`Terjadi Kesalahan, Plugin ini Khusus Untuk Owner.`")
        return
    await event.edit("`Sedang Mengeluarkan Semua Member Dalam Group Ini...`")

    everyone = await event.client.get_participants(event.chat_id)
    for user in everyone:
        if user.id == lynxget.id:
            pass
        try:
            await event.client(EditBannedRequest(event.chat_id, int(user.id), ChatBannedRights(until_date=None, view_messages=True)))
        except Exception as e:
            await event.edit(str(e))
        await sleep(.5)
    await event.edit("☑️Berhasil, Anda Telah Menendang Semua Member Disini.")


@register(outgoing=True, pattern=r"^\.allunban(?: |$)(.*)", groups_only=True)
async def _(event):
    await event.edit("Sedang Mencari List Banning...")
    p = 0
    (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except BaseException:
            pass
    await event.edit("Success, List Semua Ban Didalam Group ini Telah Dihapus.")


CMD_HELP.update(
    {
        "admin": "✘ Pʟᴜɢɪɴ : Administrator Group"\
        "\n\n⚡𝘾𝙈𝘿⚡: `.promote` <Username/Reply> <Nama Title (Optional)>"
        "\n↳ : Mempromosikan Member Sebagai Admin. (u/Owner)"
        "\n\n⚡𝘾𝙈𝘿⚡: `.demote` <Username/Reply>"
        "\n↳ : Menurunkan Posisi Admin Sebagai Member. (u/Owner)"
        "\n\n⚡𝘾𝙈𝘿⚡: `.ban` <Username/Reply> <Alasan(Optional)>"
        "\n↳ : Memblokir Seseorang, Secara Pribadi Maupun Group."
        "\n\n⚡𝘾𝙈𝘿⚡: `.unban <Username/Reply>`"
        "\n↳ : Menghapus Blokir."
        "\n\n⚡𝘾𝙈𝘿⚡: `.mute` <Username/Reply> <Alasan(Optional)>"
        "\n↳ : Membisukan Seseorang Di Group, Bisa Ke Admin Juga. :v"
        "\n\n⚡𝘾𝙈𝘿⚡: `.unmute` <Username/Reply>"
        "\n↳ : Membuka bisu orang yang dibisukan."
        "\n\n⚡𝘾𝙈𝘿⚡: `.zombies`"
        "\n↳ : Untuk Mencari Akun Terhapus di Dalam Group."
        "Gunakan `.zombies clean` Untuk Membersihkan Akun Terhapus di Group."
        "\n\n⚡𝘾𝙈𝘿⚡: `.all`"
        "\n↳ : Tag Semua Member Dalam Group, Membutuhkan Bot @MentionBot."
        "\n\n⚡𝘾𝙈𝘿⚡: `.admins`"
        "\n↳ : Melihat Daftar Admin di Group."
        "\n\n⚡𝘾𝙈𝘿⚡: `.bots`"
        "\n↳ : Melihat Daftar Bot Dalam Group."
        "\n\n⚡𝘾𝙈𝘿⚡: `.users` Atau >`.users` <Nama Member>"
        "\n↳ : Mendapatkan Daftar Pengguna Dalamm Group."
        "\n\n⚡𝘾𝙈𝘿⚡: `.setgpic` <Reply ke Gambar>"
        "\n↳ : Mengganti Photo Profile Group."
        "\n\n⚡𝘾𝙈𝘿⚡: `.allkick`"
        "\n↳ : Mengeluarkan Semua Member Di Dalam Group. (Only Owner)"
        "\n\n⚡𝘾𝙈𝘿⚡: `.allunban`"
        "\n↳ : Menghapus/Membatalkan Semua Orang Yang Telah Di Ban Di Dalam Group."})
