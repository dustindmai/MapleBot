from discord import Intents, Interaction, Message
from discord.ext import commands

import config

# Set Intents
intents: Intents = Intents.default()
intents.message_content = True
# Create bot
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)


# Sync bot commands
@bot.event
async def on_ready():
    try:
        print(f"Syncing {bot.user} tree commands.")
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


bot.run(token=config.TOKEN)
