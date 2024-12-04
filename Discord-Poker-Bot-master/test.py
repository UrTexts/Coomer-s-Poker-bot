#this is a santity check if the main file for some reason isnt working.

from collections import namedtuple
import os
from typing import Dict, List

import discord

from game import Game, GAME_OPTIONS, GameState

# Create intents to enable required events
intents = discord.Intents.default()  # Default intents will enable basic events
intents.message_content = True  # Allow the bot to read message content (important for handling messages)

# Create a Discord client with the defined intents
client = discord.Client(intents=intents)

# Example bot events to demonstrate usage
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!startgame'):
        await start_new_game(message)

# Sample function for starting a new game
async def start_new_game(message):
    # Initialize your game logic
    game = Game()
    await message.channel.send("Starting a new game!")
    # Your game logic here (create a game, set up players, etc.)

# Run the bot with your token
client.run('YOUR_TOKEN_HERE')

