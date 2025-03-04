from discord import Intents, Interaction, Message
from discord.ext import commands

# from event_enum import initialize_event_enum, EVENT_ENUM
import config
import asyncio
import logging
from database import init_db

# Set Intents
intents: Intents = Intents.default()
intents.message_content = True
# Create bot
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

COGS = ["cogs.event_manager", "cogs.admin"]


async def load_cogs():
    for cog in COGS:
        try:
            print(f"Attemping to load {cog}...")
            await bot.load_extension(cog)
            print(f"Loaded {cog} successfully!")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")


# Sync bot commands
@bot.event
async def on_ready():
    try:
        # print("Loading EVENT_ENUM")
        # await initialize_event_enum()
        # print("Event Enum Loaded: ", EVENT_ENUM)
        print(f"Syncing {bot.user} tree commands...")
        synced = await bot.tree.sync()

        print(f"Synced {len(synced)} tree command(s)!")
    except Exception as e:
        print(e)


@bot.tree.command(name="hello", description="Replies to user secretly.")
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")


@bot.tree.command(name="echo")
async def echo(interaction: Interaction, msg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{msg}' ")


@bot.tree.command(name="pm")
async def pm(interaction: Interaction):
    try:
        await interaction.response.send_message(
            "Sending private message...", ephemeral=True
        )
        await interaction.user.send("hi")
    except Exception as e:
        print(e)


@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}]{username}:"{user_message}"')


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await init_db()
    await load_cogs()
    await bot.start(config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
