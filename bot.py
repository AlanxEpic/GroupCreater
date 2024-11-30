import os
import random
import pyrogram
from pyrogram import Client, filters, idle
from flask import Flask
import re, os, random, asyncio, logging, time, io, sys, traceback

# Telegram Bot Config
api_id = 25895085
api_hash = "4d83e959108956d7c0b05bd8f52f54b5"
STRING_SESSION = os.environ.get("STRING_SESSION")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ru = random.randint(182763637281, 82828272726525262)
OWNER_ID = (6106882014, 5644071668)
#user = Client("user", api_id=api_id, api_hash=api_hash, session_string=STRING_SESSION, in_memory=True)
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

# Flask Web Server
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"
@bot.on_message(filters.command("eval"))
#@user.on_message(filters.command("eval"))
async def deval(client, message):
    me = await client.get_me()
    print(me)
    print(message)
    print(dir(message))
    if not message.from_user.id in OWNER_ID:
        return
    status_message = await message.reply("**•×• Processing... •×•**")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**•• Eᴠᴀʟ ••\n** "
    final_output += f"`{cmd}`\n\n"
    final_output += "**•• Oᴜᴛᴘᴜᴛ ••** \n"
    final_output += f"`{evaluation.strip()}` \n"

    if len(final_output) > 1900:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply(file=discord.File(out_file, filename=out_file.name))
            print(evaluation.strip())
    else:
        await status_message.edit(content=final_output)
        print(evaluation.strip())

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

        
# Start the Bot and Web Server
def start():
    print("Starting the user and web server...")
    #user.run()
    #user.send_message(5644071668, "Bot has been started")
    print("Starting the bot....")
    bot.start()
    bot.send_message(5644071668, "Bot has been started")

    # Run Flask in a separate thread
    import threading
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8000}).start()

    idle()  # Keep the bot running
    #user.stop()
    print("User has stopped.")
    bot.stop()
    print("Bot has stopped.")

if __name__ == "__main__":
    start()
