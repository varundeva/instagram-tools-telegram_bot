from pyrogram import Client, filters
from instaloader import Instaloader, Post
import requests
import re
import os
import helper as vh
from . import dpdownload
from pyrogram.errors import BadRequest
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


help_keyboard = [[InlineKeyboardButton(
    "Join Channel", url="https://t.me/helpingbots")]]
help_reply_markup = InlineKeyboardMarkup(help_keyboard)


def sendPhoto(url, message):
    message.reply_chat_action("upload_photo")
    message.reply_photo(url)


def sendVideo(url, thumbnailUrl, context):
    r = requests.get(url, allow_redirects=True)
    size = r.headers.get('content-length', -1)
    if int(size) > 20971520:
        extension = r.headers.get('Content-Type').split('/')
        fileName = (size+'.'+extension[1])
        open(fileName, 'wb').write(r.content)
        res = requests.get(thumbnailUrl, allow_redirects=True)
        thumbnailSize = res.headers.get('content-length', -1)
        thumbnailExtension = res.headers.get('Content-Type').split('/')
        thumbnailName = (thumbnailSize+'.'+thumbnailExtension[1])
        open(thumbnailName, 'wb').write(res.content)
        try:
            context.reply_chat_action("upload_video")
            context.reply_video(fileName, duration=vh.getVideoDuration(
                fileName), thumb=thumbnailName, supports_streaming=True)
        finally:
            if os.path.exists(fileName):
                os.remove(fileName)
            if os.path.exists(thumbnailName):
                os.remove(thumbnailName)

    else:
        context.reply_chat_action("upload_video")
        context.reply_video(url)


def sendSidecar(data, context):
    for x in data:
        if x.is_video:
            sendVideo(x.video_url, post.url, context)
        elif not x.is_video:
            sendPhoto(x.display_url, context)


L = Instaloader()


@Client.on_message(filters.command("post") | filters.text)
def post(client, message):
    try:
        channel_member = client.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"),
                                                user_id=message.chat.id)
        try:
            query = message.text
            vh.addToLog(message, client, query)
            if "instagram.com/p/" in query or "instagram.com/reel/" in query or "instagram.com/tv/" in query:
                splittedUrl = re.split(r'[/? ]', query)
                splittedUrl = list(filter(None, splittedUrl))
                if "post" in splittedUrl:
                    query = splittedUrl[4]
                else:
                    query = splittedUrl[3]
            else:
                dpdownload.dp(client, message)
            post = Post.from_shortcode(L.context, query)

            if post.typename == 'GraphImage':
                sendPhoto(post.url, message)

            if post.typename == 'GraphVideo':
                sendVideo(post.video_url, post.url, message)

            if post.typename == 'GraphSidecar':
                sendSidecar(post.get_sidecar_nodes(start=0, end=-1), message)

        except Exception as e:
            print(e)
            vh.addToLog(message, client, e)
    except BadRequest as e:
        print(e)
        message.reply(
            text=f"Hi {message.from_user.first_name}\n\nTo use me you have to be a member of the updates channel in order to stay updated with the latest developments.\n\n<b>Please click below button to join and /start the bot again.</b>", reply_markup=help_reply_markup)
        return
