import os
import random
import pyrogram
from pyrogram import Client, filters, idle
from flask import Flask

# Telegram Bot Config
api_id = 
api_hash = " "
bot_token = os.environ.get("BOT_TOKEN")
ru = random.randint(182763637281, 82828272726525262)
bot = Client("Bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Flask Web Server
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

        
# Start the Bot and Web Server
def start():
    print("Starting the bot and web server...")
    bot.start()
    bot.send_message(5644071668, "Bot has been started")

    # Run Flask in a separate thread
    import threading
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8000}).start()

    idle()  # Keep the bot running
    bot.stop()
    print("Bot has stopped.")

if __name__ == "__main__":
    start()
