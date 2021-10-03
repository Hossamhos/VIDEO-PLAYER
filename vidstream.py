import os
import re
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pytgcalls import idle as pyidle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityAudio
from pytgcalls.types.input_stream.quality import HighQualityVideo, MediumQualityVideo, LowQualityVideo
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
from time import time

# YTDL
opts = {"format": "best[height=?720]/best", "noplaylist": True}
ydl = YoutubeDL(opts)

# Client and PyTgCalls
API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
SESSION = os.getenv("SESSION")
CHAT = int(os.getenv("CHAT"))
HNDLR = os.getenv("HNDLR", "!")

bot = Client(SESSION, API_ID, API_HASH)
self_or_contact_filter = filters.create(
    lambda _, __, message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)
call_py = PyTgCalls(bot)
GROUP_CALL = []


@bot.on_message(self_or_contact_filter & filters.command("vstream", prefixes=f"{HNDLR}"))
async def stream(client, m: Message):
   if len(m.command) < 2:
      await m.reply("`Give A Link/LiveLink/.m3u8 URL/YTLink to Stream from 🎶`")
   else:
      link = m.text.split(None, 1)[1]
      chat_id = m.chat.id
      huehue = await m.reply("`Trying to Stream 💭`")

      # Filtering out YouTube URL's
      regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
      match = re.match(regex,link)
      if match:
         try:
            meta = ydl.extract_info(link, download=False)
            formats = meta.get('formats', [meta])
            for f in formats:
               ytstreamlink = f['url']
            livelink = ytstreamlink
         except Exception as e:
            huehue.edit(f"**YTDL ERROR** \n{e}")
      else:
         livelink = link

      # Playing
      if chat_id in GROUP_CALL:
         try:
            await call_py.change_stream(
               chat_id,
               AudioVideoPiped(
                  livelink,
                  HighQualityAudio(),
                  HighQualityVideo()
               )
            )
            await huehue.delete()
            await m.reply(f"Started [Streaming]({livelink}) in {chat_id}!", disable_web_page_preview=True)
         except Exception as ep:
            await huehue.edit(f"{ep}")
      else:
         try:
            await call_py.join_group_call(
               chat_id,
               AudioVideoPiped(
                  livelink,
                  HighQualityAudio(),
                  HighQualityVideo()
               )
            )
            GROUP_CALL.append(chat_id)
            await huehue.delete()
            await m.reply(f"Started [Streaming]({livelink}) in {chat_id}!", disable_web_page_preview=True)
         except Exception as ep:
            await huehue.edit(f"{ep}")

@bot.on_message(self_or_contact_filter & filters.command("vplay", prefixes=f"{HNDLR}"))
async def play(client, m: Message):
   replied = m.reply_to_message
   if replied:
      if replied.document or replied.video:
         huehue = await replied.reply("`Downloading 📩`")
         location = await replied.download()
         chat_id = m.chat.id
         if chat_id in GROUP_CALL:
            try:
               await call_py.change_stream(
                  chat_id,
                  AudioVideoPiped(
                     location,
                     HighQualityAudio(),
                     HighQualityVideo()
                  )
               )
               await huehue.delete()
               await replied.reply(f"Started Playing in {chat_id}!", disable_web_page_preview=True)
            except Exception as ep:
               await huehue.edit(f"{ep}")
         else:
            try:
               await call_py.join_group_call(
                  chat_id,
                  AudioVideoPiped(
                     location,
                     HighQualityAudio(),
                     HighQualityVideo()
                  )
               )
               GROUP_CALL.append(chat_id)
               await huehue.delete()
               await replied.reply(f"Started Playing in {chat_id}!", disable_web_page_preview=True)
            except Exception as ep:
               await huehue.edit(f"{ep}")
      else:
         if len(m.command) < 2
            await replied.reply("`Either Reply to a VIDEO or Give me Query/YT Link to Play`")
         else:
            try:
               hmmop = await m.reply("`Searching 🔎`")
               search = VideosSearch(query, limit=1)
               for result in search.result()["result"]:
                  ytid = result['id']
                  url = f"https://www.youtube.com/watch?v={ytid}"
            except Exception as ey:
               await m.reply("`Found Nothing :( Try searching something Else.`")
            try:
               meta = ydl.extract_info(url, download=False)
               formats = meta.get('formats', [meta])
               for f in formats:
                  ytstreamlink = f['url']
               ytlink = ytstreamlink
            except Exception as eu:
               hmmop.edit(f"**YTDL ERROR** \n{eu}")
            # Playing
            if chat_id in GROUP_CALL:
               try:
                  await call_py.change_stream(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        HighQualityVideo()
                     )
                  )
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({ytlink}) in {chat_id}!", disable_web_page_preview=True)
               except Exception as ep:
                  await hmmop.edit(f"{ep}")
            else:
               try:
                  await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        HighQualityVideo()
                     )
                  )
                  GROUP_CALL.append(chat_id)
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({livelink}) in {chat_id}!", disable_web_page_preview=True)
               except Exception as ep:
                  await hmmop.edit(f"{ep}")
   
   else:
         if len(m.command) < 2
            await replied.reply("`Either Reply to a VIDEO or Give me Query/YT Link to Play`")
         else:
            try:
               hmmop = await m.reply("`Searching 🔎`")
               search = VideosSearch(query, limit=1)
               for result in search.result()["result"]:
                  ytid = result['id']
                  url = f"https://www.youtube.com/watch?v={ytid}"
            except Exception as ey:
               await m.reply("`Found Nothing :( Try searching something Else.`")
            try:
               meta = ydl.extract_info(url, download=False)
               formats = meta.get('formats', [meta])
               for f in formats:
                  ytstreamlink = f['url']
               ytlink = ytstreamlink
            except Exception as eu:
               hmmop.edit(f"**YTDL ERROR** \n{eu}")
            # Playing
            if chat_id in GROUP_CALL:
               try:
                  await call_py.change_stream(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        HighQualityVideo()
                     )
                  )
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({ytlink}) in {chat_id}!", disable_web_page_preview=True)
               except Exception as ep:
                  await hmmop.edit(f"{ep}")
            else:
               try:
                  await call_py.join_group_call(
                     chat_id,
                     AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        HighQualityVideo()
                     )
                  )
                  GROUP_CALL.append(chat_id)
                  await hmmop.delete()
                  await m.reply(f"Started [Streaming]({livelink}) in {chat_id}!", disable_web_page_preview=True)
               except Exception as ep:
                  await hmmop.edit(f"{ep}")

@bot.on_message(self_or_contact_filter & filters.command("vstop", prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
   try:
      chat_id = m.chat.id
      if chat_id in GROUP_CALL:
         GROUP_CALL.remove(chat_id)
      else:
         pass
      await call_py.leave_group_call(chat_id)
      await m.reply("`Stopped Streaming 🍦`")
   except Exception as e:
      print(e)

@bot.on_message(self_or_contact_filter & filters.command("ping", prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
   start = time()
   m_reply = await m.reply_text("`...`")
   delta_ping = time() - start
   await m_reply.edit(f"`Pong 🏓!` \n`{delta_ping * 1000:.3f} ms`")


bot.start()
call_py.start()
pyidle()
idle()