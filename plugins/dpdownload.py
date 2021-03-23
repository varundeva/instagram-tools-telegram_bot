from pyrogram import Client, filters
from instaloader import Instaloader, Profile
from pyrogram.errors import BadRequest
import re
import helper as vh
import os

L = Instaloader()
L.login(os.environ.get("IG_USERNAME"), os.environ.get("IG_PASSWORD"))


@Client.on_message(filters.command(commands="dp", case_sensitive=False))
def dp(client, message):
    if vh.checkMemberStatus(client, message):
        # Get username/string from the message
        query = ""
        if message.text[:3] == "/dp":
            query = message.text[3:].lstrip()
        else:
            query = message.text

        originalQuery = query

        if message.text[:5] == "/post":
            query = message.text[6:].lstrip()

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
        msg = message.reply_text("Please Wait...")
        print(query)
        try:
            user = Profile.from_username(L.context, query.lstrip())
            caption_msg = f'''Name: {user.full_name}'''
            message.reply_chat_action("upload_photo")
            message.reply_photo(
                photo=user.profile_pic_url,
                caption=caption_msg, parse_mode='MARKDOWN')
            vh.addToLog(message, client, query)
            msg.delete()
            thnk_msg = '''Thank you for using bot \nShare bot with your friends and have fun'''
            message.reply(thnk_msg, 'HTML')

        except Exception:
            msg.edit_text(
                f'''Something Went Wrong..\nMaybe Username {originalQuery}  not Available..''')
