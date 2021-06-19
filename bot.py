from pyrogram import Client
import os

from pyrogram.methods.utilities import run

# Dev Purpose
if not os.environ.get("API_ID"):
    from dotenv import load_dotenv
    load_dotenv()

app = Client(
    "ig_tool",
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    plugins=dict(root="plugins")
).run()
