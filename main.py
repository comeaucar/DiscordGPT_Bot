from revChatGPT.revChatGPT import Chatbot
import json
import discord
from discord.ext import commands
import os

# bot setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!",
                      case_insensitive=True,
                      intents=intents)
BOT_SECRET = os.environ['BOT_SECRET']

# chatGPT config

with open("config.json", "r") as f:
  config = json.load(f)

config['Authorization'] = os.environ['AUTH']
config['session_token'] = os.environ['SESS_TOKEN']
config['email'] = os.environ['EMAIL']
config['password'] = os.environ['PASSWORD']

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
      if (len(resp['message']) > 1999):
        await ctx.send((resp['message'])[:1999])
        await ctx.send("-" + (resp['message'])[1999:])
      else:
        await ctx.send(resp['message'])
  except Exception as e:
    await ctx.send("An error occurred during the request")
    print("Something went wrong")
    print(e)

# reset chat
@client.command()
async def reset(ctx, arg):
  try:
    chatbot.reset_chat()
    await ctx.send("Chat was reset")
  except Exception as e:
    await ctx.send("An error occurred during the request")
    print(e)


# run bot
client.run(BOT_SECRET)