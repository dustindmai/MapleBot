import asyncio
import datetime

import discord
from sqlalchemy.future import select

from database import AsyncSessionLocal
from models import Event, Remindees


async def reminder_loop(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        async with AsyncSessionLocal() as session:
            nowFull = datetime.datetime.now(datetime.timezone.utc)
            now = datetime.time(nowFull.time().hour, nowFull.time().minute)
            print(f"\nTIME NOW: {now}\n")
            result = await session.execute(
                select(Remindees, Event)
                .join(Event, Remindees.event_id == Event.event_id)
                .where(Event.reset_time == now)
            )

            reminders = result.all()

            print(f"\nREMINDERS: {reminders}\n")

            user_reminders = {}
            for remindee, event in reminders:
                print(f"{event.event_name}\n")
                if remindee.discord_id not in user_reminders:
                    user_reminders[remindee.discord_id] = []
                user_reminders[remindee.discord_id].append(event.event_name)

            for user_id, event_names in user_reminders.items():
                print(f"user_id:{user_id}, event_name:{event_names}")
                user = bot.get_user(int(user_id))
                print(user)
                if not user:
                    try:
                        user = await bot.fetch_user(int(user_id))
                    except discord.NotFound:
                        print(f"User {user_id} not found.")
                        continue
                reminder_text = "\n".join(f"- {name}" for name in event_names)
                try:
                    await user.send(f"**Upcoming resets:**\n{reminder_text}")
                except discord.Forbidden:
                    for guild in bot.guilds:
                        member = guild.get_member(user_id)
                        if member:
                            channel = guild.system_channel or discord.utils.get(
                                guild.text_channels, name="general"
                            )
                            if channel:
                                try:
                                    await channel.send(
                                        f"{member.mention}, I couldn't DM you your reset reminders!"
                                        f"Please enable DMs or check notifications in the bot channel."
                                    )
                                except Exception as e:
                                    print(f"Error sending message in {
                                          guild.name}: {e}")
                            break
        await asyncio.sleep(60 - datetime.datetime.now().time().second)
