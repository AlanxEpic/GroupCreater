from openai import OpenAI
import pyrogram
from pyrogram import Client, filters, idle
from flask import Flask
import re, os, random, asyncio, logging, time, io, sys, traceback
import openai

# Telegram Bot Config
api_id = 25895085
api_hash = "4d83e959108956d7c0b05bd8f52f54b5"
STRING_SESSION = os.environ.get("STRING_SESSION")
GPT_KEY = os.environ.get("GPT_KEY")  # Add your OpenAI API key here or as an environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ru = random.randint(182763637281, 82828272726525262)
OWNERS = 6106882014, 5644071668
gpt = OpenAI(api_key=GPT_KEY)

user = Client("user", api_id=api_id, api_hash=api_hash, session_string=STRING_SESSION, in_memory=True)
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

# Flask Web Server
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@bot.on_message(filters.command(commands="eval", prefixes="."))
@user.on_message(filters.command("eval"))
async def deval(client, message):
    if not message.from_user.id in OWNERS:
        return

    me = await client.get_me()

    status_message = None
    try:
        status_message = await message.edit("**•×• Processing... •×•**")
    except:
        status_message = await message.reply("**•×• Processing... •×•**")

    # Get the command without Markdown formatting
    cmd = message.text.split(" ", maxsplit=1)[1]
    if not cmd:
        await status_message.edit("Give a eval code first")

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

    final_output = "**•• Eval ••\n** "
    final_output += f"`{cmd}`\n\n"
    final_output += "**•• Output ••** \n"
    final_output += f"`{evaluation.strip()}` \n"

    if len(final_output) > 4000:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(document=out_file)
            print(evaluation.strip())
    else:
        await status_message.edit(final_output)
        print(evaluation.strip())

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@bot.on_message(filters.command("gpt", prefixes="."))
@user.on_message(filters.command("gpt"))
async def gpt_response(client, message):
    if not GPT_KEY:
        await message.reply("OpenAI API key is missing. Set it as an environment variable.")
        return

    try:
        # Extract user query
        query = message.text.split(" ", maxsplit=1)[1]
        
        response = gpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who is programming pro, the best question answerers, the advanced answer provider and detailed provider."},
                {"role": "user", "content": query}
            ]
        )

        # Retrieve the response content
        for gans in response:
            reply = gans.choices[0].delta.content
        
        await message.reply(reply)

    except IndexError:
        await message.reply("Please provide a query. Usage: `.gpt <your question>`")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@bot.on_message(filters.command(commands="open", prefixes="."))
@user.on_message(filters.command("open"))
async def open_file(client, message):
    if not message.reply_to_message.document:
        await message.reply("Please reply to a file!")
        return

    try:
        # Download the file
        file_path = await client.download_media(message.reply_to_message.document)

        # Read the content of the file
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Split the content into chunks of 4096 characters
        chunks = [content[i:i+4096] for i in range(0, len(content), 4096)]

        # Send each chunk as a separate message
        for chunk in chunks:
            await message.reply(chunk)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@user.on_message()
async def vip(client, message):
    if message.chat.id in (-1002488817605, -1002430649843):
        await message.copy(-1002478370016)
    else:
        return

@bot.on_message(filters.command("ping", prefixes="."))
async def ping(client, message):
    await message.reply("Pong!")

@user.on_message(filters.command("ping"))
async def ping_user(client, message):
    await message.reply("Pong from user!")

# Start the Bot and Web Server
def start():
    print("Starting the user and web server...")
    user.start()
    user.send_message(5644071668, "Bot has been started")
    print("Starting the bot....")
    bot.start()
    bot.send_message(5644071668, "Bot has been started")

    # Run Flask in a separate thread
    import threading
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8000}).start()

    idle()  # Keep the bot running
    user.stop()
    print("User has stopped.")
    bot.stop()
    print("Bot has stopped.")

if __name__ == "__main__":
    start()
