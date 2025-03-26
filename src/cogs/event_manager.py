from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy.future import select

from database import get_db
from models import Event
from views import confirm_view


# from typing import List
class EventManager(commands.Cog):
    """Cog to manage Events table

    Args:
        commands (_type_): Commands Cog
    """

    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot= bot


        # async def get_db(self):
    #     """Gets and returns an asynchronous database session

    #     Returns:
    #         AsyncSession: database session
    #     """
    #     async with AsyncSessionLocal() as session:
    #         yield session

    @app_commands.command(name="add_event", description="Adds a new event/reminder.")
    @app_commands.choices(
        interval=[
            app_commands.Choice(name="Daily", value=1),
            app_commands.Choice(name="Weekly", value=7),
            app_commands.Choice(name="Monthly", value=31),
        ]
    )
    # @commands.is_owner()
    async def add_event(
        self,
        interaction: discord.Interaction,
        name: str,
        res_time: str,
        interval: app_commands.Choice[int],
        day: int,
    ):
        """Adds an event reminder to the events table

        Args:
            interaction (discord.Interaction): Discord user command call
            name (str): name of the event to add
            res_time (str): reset time for event
            interval (app_commands.Choice[int]): how often reminder needs to go out
            day (int): what day the reminder needs to go out
        """
        async for session in get_db():
            try:
                res_time = datetime.strptime(res_time, "%H:%M")
            except Exception as e:
                await interaction.response.send_message(f"Reset time is invalid. {e}")
            new_event = Event(
                event_name=name,
                reset_time=res_time,
                reset_type=interval.name,
                reset_interval=timedelta(days=interval.value),
                reset_day=None if day <= 0 else day,
            )
            try:
                session.add(new_event)
                await session.commit()
                await interaction.response.send_message(
                    f"Event '{name}' added successfully."
                )
            except Exception as e:
                print(f"Error in add_event: {e}")
                await interaction.response.send_message(
                    f"Event was not added successfully: {e}"
                )

    @app_commands.command(
        name="edit_event", description="Edits an event's reset time/interval/name etc."
    )
    async def edit_event(self, interaction: discord.Interaction):
        return

    @app_commands.command(
        name="list_reminders", description="Lists all current events/reminders."
    )
    async def list_reminders(self, interaction: discord.Interaction):
        """Generates a list of available reminders.

        Args:
            interaction (discord.Interaction): Discord user interaction/command call.
        """
        async for session in get_db():
            stmt = select(Event)
            result = await session.execute(stmt)
            events = result.scalars().all()

            if not events:
                await interaction.response.send_message("No events found.")
                return
            event_list = "\n".join(
                f"**{event.event_name}** - Resets at {event.reset_time} UTC. ID: {event.event_id}"
                for event in events
            )

            embed = discord.Embed(
                title="Available Events",
                description=event_list,
                color=discord.Color.blue(),
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="remove_reminder", description="Removes an event from the event table."
    )
    @commands.is_owner()
    async def remove_reminder(self, interaction: discord.Interaction, event_id: int):
        async for session in get_db():
            stmt = select(Event).where(Event.event_id == event_id)
            result = await session.execute(stmt)
            event = result.scalar_one_or_none()
            if event:
                embed = discord.Embed(
                    title="Confirmation",
                    description=f"Do you really want to remove '{
                        event.event_name}' from the events table?",
                    color=discord.Color.orange(),
                )
                view = confirm_view.ConfirmView()
                await interaction.response.send_message(embed=embed, view=view)
                await view.wait()
                if view.value is None:
                    await interaction.followup.send("Timed out.", ephemeral=True)
                    return
                elif view.value:
                    await session.delete(event)
                    await session.commit()
                    await interaction.followup.send(
                        "Event removed successfully.", ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        "Event was not removed.", ephemeral=True
                    )
            else:
                await interaction.response.send_message("Event does not exist.")


async def setup(bot):
    await bot.add_cog(EventManager(bot))
