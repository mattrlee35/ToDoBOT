import datetime
import discord
from discord.ext import tasks
import os
import time

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
timeRightNow = datetime.datetime.now()
todoList = []

async def displayList(message):
        await message.channel.send("**"+timeRightNow.strftime("%m") + "/" + timeRightNow.strftime("%d") + "/" + timeRightNow.strftime("%Y")+"**"+"\n"+"**-------------**")
        for i in todoList:
            await message.channel.send("• " + i)

async def add(message):
        holder = message.content.split(" ", 1)
        if len(holder) < 2:
            await message.channel.send('What would you like to add to the todo list?')
            response = await client.wait_for("message", check=lambda m: m.author == message.author)
            todoList.append(response.content)
            await message.channel.send("Added `" + response.content + "` to the list")
        else:
            todoList.append(holder[1])
            await message.channel.send("Added `" + holder[1] + "` to the list")

async def remove(message):
        holder = message.content.split(" ", 1)
        if len(holder) < 2:
            await message.channel.send('What would you like to remove from the todo list?')
            response = await client.wait_for("message", check=lambda m: m.author == message.author)
            todoList.remove(response.content)
            await message.channel.send("Removed `" + response.content + "` from the list")
        else:
            todoList.remove(holder[1])
            await message.channel.send("Removed `" + holder[1] + "` from the list")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!add'):
        await add(message)
        
    if message.content.startswith('!remove'):
        await remove(message)
        
    if message.content.startswith('!preview'):
        await displayList(message)

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
