from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import BadRequest
import os
welcome_msg = '''<b>Welcome To the Bot</b>
<i>Send instagram username to get DP</i>
Bot is for Education Purpose only. Don't Misuse'''

help_keyboard = [[InlineKeyboardButton(
    "Join Channel", url="https://t.me/helpingbots")]]
help_reply_markup = InlineKeyboardMarkup(help_keyboard)


@Client.on_message(filters.command(commands="start", case_sensitive=False))
def start(client, message):
    try:
        channel_member = client.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"),
                                                user_id=message.chat.id)
        message.reply(welcome_msg, quote=True, parse_mode="html")
    except BadRequest as e:
        print(e)
        message.reply(
            text=f"Hi {message.from_user.first_name}\n\nTo use me you have to be a member of the updates channel in order to stay updated with the latest developments.\n\n<b>Please click below button to join and /start the bot again.</b>", reply_markup=help_reply_markup)
        return


@Client.on_message(filters.command(commands="contact", case_sensitive=False))
def contact(client, message):
    message.reply_text(
        'Join Group.. There You Can Contact')


@Client.on_message(filters.command(commands="about", case_sensitive=False))
def about(client, message):
    message.reply_text(
        'Im Instagram Tool Bot')


@Client.on_message(filters.command(commands="help", case_sensitive=False))
def help(client, message):
    message.reply_text(
        'OK..! Join Group My Owner will help you')
