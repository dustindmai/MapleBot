import asyncio
import datetime

from sqlalchemy.future import select

from database import AsyncSessionLocal
from models import Event, Remindees


async def reminder_loop(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        async with AsyncSessionLocal() as session:
            now = datetime.datetime.now(datetime.timezone.utc).time()
            now = datetime.time(now.hour, now.minute)
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
                if remindee.discord_id not in user_reminders:
                    user_reminders[remindee.discord_id] = []
                user_reminders[remindee.discord_id].append(event.event_name)

            for user_id, event_names in user_reminders.items():
                user = bot.get_user(user_id)
                if user:
                    reminder_text = "\n".join(f"- {name}" for name in event_names)
                    await user.send(f"** Your upcoming resets:**\n{reminder_text}")

        await asyncio.sleep(60 - datetime.datetime.now().time().second)
