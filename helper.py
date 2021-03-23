import cv2
import requests
from pyrogram import Client, client
from pyrogram.errors import BadRequest
import os


def getVideoDuration(vidFile):
    data = cv2.VideoCapture(vidFile)
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    # calculate duration of the video
    seconds = int(frames / fps)
    # print("duration in seconds:", seconds)
    return int(seconds)


def getVideoSize():
    r = requests.get(url, allow_redirects=True)
    size = r.headers.get('content-length', -1)
    return int(size)


def addToLog(message, client, query):
    template = f'''New Query in Instagram Tools Bot\n
User ID - {message.from_user.id}
UserName - @{message.from_user.username}
User Name - {message.from_user.first_name} {message.from_user.last_name}
Date Time - {message.date}
Raw Text - {message.text}
Query - {query}
'''

    client.send_message(chat_id=os.environ.get("LOG_CHANNEL_ID"),
                        text=template, disable_web_page_preview=True)


def checkMemberStatus(client, message):
    try:
        channel_member = client.get_chat_member(
            chat_id=os.environ.get("CHANNEL_ID"), user_id=message.chat.id)
        return True
    except BadRequest as e:
        print(e)
        message.reply(
            text=f"Hi {message.from_user.first_name}\n\nTo use me you have to be a member of the updates channel in order to stay updated with the latest developments.\n\n<b>Please click below button to join and /start the bot again.</b>", reply_markup=help_reply_markup)
        return False
