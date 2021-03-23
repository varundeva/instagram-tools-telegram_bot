from pyrogram import Client
import os

from dotenv import load_dotenv
load_dotenv()

app = Client(
    "ig_tools",
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    plugins=dict(root="plugins")
).run()
