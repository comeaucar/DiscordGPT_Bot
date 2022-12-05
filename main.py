from revChatGPT.revChatGPT import Chatbot
import json
import discord
from discord.ext import commands, tasks
import requests
import os
import asyncio

# bot setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
BOT_SECRET = os.environ['BOT_SECRET']

# chatGPT config

with open("config.json", "r") as f: config = json.load(f)
chatbot = Chatbot(config, conversation_id=None)

# on ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# ask command
@client.command()
async def ask(ctx, *arg):
    try:
        async with ctx.typing():
            chatbot.reset_chat()
            chatbot.refresh_session()
            prompt = " ".join(arg)
            resp = chatbot.get_chat_response(prompt, output="text")
            print(resp)
            await ctx.send(resp['message'])
    except Exception as e:
        print("Something went wrong")
        print(e)

# run bot
client.run(BOT_SECRET)






