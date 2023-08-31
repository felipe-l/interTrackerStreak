# This example requires the 'message_content' intent.

import discord
import modules
import config
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

streakCount = [3,5,8,10,15,20]

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

async def check_streak_loop():
    targetChannelId = 1145501551755001918
    targetChannel = client.get_channel(targetChannelId)
    while True:
        # loop = asyncio.get_event_loop()
        for count in streakCount:
            res = modules.databaseFunctions.getNewStreakData(count)
            if res is not None:
                for announcement in res:
                    finalMessage = "! " + str(announcement[0]) + " ON WIN STREAK(" + str(announcement)[1] + ") " + " with streak of " + str(announcement[2])
                    await targetChannel.send(finalMessage)
                    modules.databaseFunctions.updateUserStreak(announcement[0], announcement[1], announcement[2], announcement[3], "true")
        await asyncio.sleep(60)  # Wait for 60 seconds (1 minute)

client.run(config.DISCORD_KEY)