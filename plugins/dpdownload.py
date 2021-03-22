from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instaloader import Instaloader, Profile
from pyrogram.errors import BadRequest
import os
import re
L = Instaloader()

help_keyboard = [[InlineKeyboardButton(
    "Join Channel 📢", url="https://t.me/helpingbots")]]
help_reply_markup = InlineKeyboardMarkup(help_keyboard)


@Client.on_message(filters.command(commands="dp", case_sensitive=False))
def dp(client, message):
    try:
        channel_member = client.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"),
                                                user_id=message.chat.id)
        # Get username/string from the message
        query = ""
        if message.text[:3] == "/dp":
            query = message.text[3:].lstrip()
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
        msg = message.reply_text("Downloading...")
        try:
            print("Search Query" + query.lstrip())
            user = Profile.from_username(L.context, query.lstrip())
            caption_msg = f'''Name: {user.full_name}'''
            message.reply_chat_action("upload_photo")
            message.reply_photo(
                photo=user.profile_pic_url,
                caption=caption_msg, parse_mode='MARKDOWN')
            msg.delete()
            thnk_msg = '''Thank you for using bot \nShare bot with your friends and have fun'''
            message.reply(thnk_msg, 'HTML')

        except Exception:
            msg.edit_text(
                f'''Something Went Wrong..\nMaybe Username {originalQuery}  not Available..''')

    except BadRequest as e:
        print(e)
        message.reply(
            text=f"Hi {message.from_user.first_name}\n\nTo use me you have to be a member of the updates channel in order to stay updated with the latest developments.\n\n<b>Please click below button to join and /start the bot again.</b>", reply_markup=help_reply_markup)
        return
