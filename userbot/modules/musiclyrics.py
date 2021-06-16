# © Copyright 2021 Lynx-Userbot LLC Company. (Axel Alexius Latukolan)
# GPL-3.0 License (General Public License) From Github
# WARNING !! Don't Delete This Hashtag if u Kang it !!
# Ported for Lynx-Userbot by @Vckyuouu (piki)
# Credits : @Ultroid



import json
import os
import random
import base64
from lyrics_extractor import SongLyrics as sl
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from youtubesearchpython import SearchVideos

from userbot.events import register
from userbot import CMD_HELP, ALIVE_NAME


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

# Fixes Bug by @Spidy
a1 = base64.b64decode("QUl6YVN5QXlEQnNZM1dSdEI1WVBDNmFCX3c4SkF5NlpkWE5jNkZV").decode("ascii")
a2 = base64.b64decode("QUl6YVN5QkYwenhMbFlsUE1wOXh3TVFxVktDUVJxOERnZHJMWHNn").decode("ascii")
a3 = base64.b64decode("QUl6YVN5RGRPS253blB3VklRX2xiSDVzWUU0Rm9YakFLSVFWMERR").decode("ascii")

@register(outgoing=True, pattern=r"^\.music (.*)")
async def download_video(event):
    a = event.text
    if a[5] == "s":
        return
    await event.edit("`Sedang Memproses Music, Mohon Tunggu Sebentar...`")
    url = event.pattern_match.group(1)
    if not url:
        return await event.edit("**List Error**\nCara Penggunaan : -`.music <Judul Lagu>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await event.edit("`Tidak Dapat Menemukan Music...`")
    type = "audio"
    await event.edit(f"`Persiapan Mendownload {url}...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await event.edit("`Mendapatkan Info Music...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await event.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await event.edit("`Video is not available from your geographic location due to"
                         + " geographic restrictions imposed by a website.`"
                         )
        return
    except MaxDownloadsReached:
        await event.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await event.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await event.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        return await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await event.edit("`There was an error during info extraction.`")
    except Exception as e:
        return await event.edit(f"{str(type(e)): {str(e)}}")
    dir = os.listdir()
    if f"{rip_data['id']}.mp3.jpg" in dir:
        thumb = f"{rip_data['id']}.mp3.jpg"
    elif f"{rip_data['id']}.mp3.webp" in dir:
        thumb = f"{rip_data['id']}.mp3.webp"
    else:
        thumb = None
    upteload = """
Connected to server...
• {}
• By - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await event.edit(f"`{upteload}`")
    CAPT = f"╭┈────────────────┈\n➥ {rip_data['title']}\n➥ Uploader - {rip_data['uploader']}\n╭┈────────────────┈╯\n➥ By : {DEFAULTUSER}\n╰┈────────────────┈➤"
    await event.client.send_file(
        event.chat_id,
        f"{rip_data['id']}.mp3",
        thumb=thumb,
        supports_streaming=True,
        caption=CAPT,
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    await event.delete()
    os.remove(f"{rip_data['id']}.mp3")
    try:
        os.remove(thumb)
    except BaseException:
        pass


@register(outgoing=True, pattern=r"^\.lyrics (.*)")
async def original(event):
    if not event.pattern_match.group(1):
        return await event.edit("Beri Saya Sebuah Judul Lagu Untuk Mencari Lirik.\n**Contoh** : `.lyrics` <Judul Lagu>")
    kenzo = event.pattern_match.group(1)
    event = await event.edit("`Sedang Mencari Lirik Lagu...`")
    dc = random.randrange(1, 3)    
    if dc == 1:
        lynx = a1
    if dc == 2:
        lynx = a2
    if dc == 3:
        lynx = a3
    extract_lyrics = sl(f"{lynx}", "15b9fb6193efd5d90")
    sh1vm = extract_lyrics.get_lyrics(f"{kenzo}")
    a7ul = sh1vm["lyrics"]
    await event.client.send_message(event.chat_id, a7ul, reply_to=event.reply_to_msg_id)
    await event.delete()

# For Lynx-Userbot by @Vckyouuu
CMD_HELP.update(
    {
        "music&lyrics": "✘ Pʟᴜɢɪɴ : Music & Lyrics\
         \n\n⚡𝘾𝙈𝘿⚡: `.music` <Penyanyi/Band - Judul Lagu>\
         \n↳ : Mengunduh Sebuah Lagu Yang Anda Inginkan.\
         \n⚡𝘾𝙈𝘿⚡: `.lirik` <Penyanyi/Band - Judul Lagu>\
         \n↳ : Mencari Lirik Lagu Yang Anda Inginkan."
    }
)
