import asyncio
import logging

from discord import Intents, Interaction, Message
from discord.ext import commands

#
import config
from database import init_db
from remind import reminder_loop

# Set Intents
intents: Intents = Intents.default()
intents.message_content = True
# Create bot
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

COGS = ["cogs.event_manager", "cogs.admin", "cogs.user_manager"]


@bot.tree.command(
    name="help",
    description="Returns all commands available and brief descriptions of each command.",
)
async def help(interaction: Interaction):
    helptext = "```"
    for command in bot.tree.walk_commands():
        helptext += f"**{command.name}** - {command.description}\n"

    helptext += "```"
    await interaction.response.send_message(helptext)


async def load_cogs():
    for cog in COGS:
        try:
            print(f"Attemping to load {cog}...")
            await bot.load_extension(cog)
            print(f"Loaded {cog} successfully!")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")


@bot.tree.command(name="reload", description="Reloads all cogs.")
@commands.is_owner()
async def reload(interaction: Interaction):
    for cog in COGS:
        try:
            print(f"Reloading cog {cog}...")
            await bot.reload_extension(cog)
            print(f"Reloaded cog {cog}!")

        except Exception as e:
            print(f"Unable to reload {cog}: {e}")
            await interaction.response.send_message(f"Unable to reload {cog}: {e}")
    await interaction.response.send_message("Reloaded cogs!", ephemeral=True)


# Sync bot commands
@bot.event
async def on_ready():
    try:
        # print("Loading EVENT_ENUM")
        # await EventEnum.load_events()
        # print("Event Enum Loaded: ", EventEnum._member_map)
        print(f"Syncing {bot.user} tree commands...")
        synced = await bot.tree.sync()

        print(f"Synced {len(synced)} tree command(s)!")
        print("Starting reminder event loop...")
        bot.loop.create_task(reminder_loop(bot))
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
