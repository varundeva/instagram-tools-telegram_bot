import cv2
import requests
from pyrogram import Client, client
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
