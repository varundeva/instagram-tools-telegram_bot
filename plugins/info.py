from pyrogram import Client, filters
from instaloader import Instaloader, Profile
import re
from pyrogram.errors import BadRequest
import helper as vh
import os

L = Instaloader()
L.login(os.environ.get("IG_USERNAME"), os.environ.get("IG_PASSWORD"))
# L.load_session_from_file("freesvofficial")


def acc_type(val):
    if(val):
        return "Private"
    else:
        return "Public"


@Client.on_message(filters.command("info"))
def info(client, message):
    try:
        channel_member = client.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"),
                                                user_id=message.chat.id)

        query = ""
        if message.text[:5] == "/info":
            query = message.text[6:].lstrip()
        else:
            query = message.text
            originalQuery = query

        # To Check given username starts from '/'
        if query[0] == "/":
            message.reply_text(
                "Username Should Not Start from '/'\nEnter a Valid Instagram User Name")
            return

        # To check given username starts from '@' if it's true then remove the @ from beginning
        if query[0] == '@':
            query = query[1:]

        # To check given username in url format. if its true extract username from url
        if "instagram.com" in query:
            splittedUrl = re.split(r'[/?]', query)
            query = splittedUrl[3]

        try:
            message.reply_chat_action("typing")
            user = Profile.from_username(L.context, query)
            infoMsg = f'''
<b>Account Information</b>\n
Name - {user.full_name}
UserName - {user.username}
Bio  - {user.biography}
Bio Url - {user.external_url}
Followers - {user.followers}
Following - {user.followees}
Posts - {user.mediacount}
IGTV Videos - {user.igtvcount}
Account Type - {acc_type(user.is_private)}
    '''
            message.reply_photo(
                photo=user.profile_pic_url, caption=infoMsg, parse_mode='HTML')
            vh.addToLog(message, client, query)

        except:
            message.reply_text(
                f'''Something Went Wrong..\nMaybe Username {query}  not Available..''')
    except BadRequest as e:
        print(e)
        message.reply(
            text=f"Hi {message.from_user.first_name}\n\nTo use me you have to be a member of the updates channel in order to stay updated with the latest developments.\n\n<b>Please click below button to join and /start the bot again.</b>", reply_markup=help_reply_markup)
        return
