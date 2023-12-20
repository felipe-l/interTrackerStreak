# This example requires the 'message_content' intent.

import discord
import modules
import config
import asyncio
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

streakCount = [3,5,8,10,15,20]
winType = {"0": "Loss", "1": "Win"}

async def send_embed_message(channel, summoner, streakType, count):
    # Your JSON string representing the embed
    embed_data = {
        "title": f"{summoner} is on a roll",
        "color": 35406,
        "url": "https://discord.com",
        "author": {
            "url": "https://discord.com"
        },
        "thumbnail": {
            "url": "https://opgg-static.akamaized.net/images/lol/champion/Viego.png"
        },
        "image": {
            "url": "https://media.tenor.com/images/f590e2a074ab988236f6ff90704ada2f/tenor.gif"
        },
        "footer": {
            "text": "InterTracker",
            "icon_url": "https://cdn.discordapp.com/avatars/939295770291634256/cc157a90af4e7f293ededc54afb9a83d.webp?size=80"
        },
        "fields": [
            {
                "name": f"{summoner} is now on a {streakType} streak of {count}",
                "value": "Keep up the climb :D",
                "inline": True
            }
        ]
    }

    # Create an Embed object
    embed = discord.Embed.from_dict(embed_data)

    # Send the embedded message
    await channel.send(embed=embed)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(check_streak_loop())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith("$send"):
        await send_embed_message(message.channel)

async def check_streak_loop():
    targetChannelId = 1145501551755001918
    targetChannel = client.get_channel(targetChannelId)
    while True:
        # loop = asyncio.get_event_loop()
        for count in streakCount:
            res = modules.databaseFunctions.getNewStreakData(count)
            print("FETCHED DB: ", res)
            if res is not None:
                for announcement in res:
                    finalMessage = "! " + str(announcement[1]) + " ON " + winType[str(announcement[2])] + " Streak of " + str(announcement[3])
                    await targetChannel.send(finalMessage)
                    modules.databaseFunctions.updateUserStreak(announcement[1], announcement[2], announcement[3], announcement[4], "true", announcement[6])
        await asyncio.sleep(60)  # Wait for 60 seconds (1 minute)

client.run(config.DISCORD_KEY)