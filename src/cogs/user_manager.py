import discord
from discord.ext import commands
from discord import app_commands
from models import Remindees, Event
from database import get_db
from sqlalchemy.future import select
from sqlalchemy import delete
from views import confirm_view
class UserManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "sub_to",
        description= "Subscribe to a reminder or all reminders."
    )
    async def sub_to(self, interaction: discord.Interaction, eid:int) :
        async for session in get_db():
            stmt = select(Event).where(Event.event_id == eid)
            result = await session.execute(stmt)
            event = result.scalar_one_or_none()
            if not event:
                await interaction.response.send_message(f"Event id {eid} does not exist.")
                return
            remind = Remindees(
                discord_id = interaction.user.id,
                event_id = eid,
                server_id = interaction.guild.id,
                is_role = False,
                is_dm = True
            )
            try:
                print("Attempting to subscribe...")
                session.add(remind)
                await session.commit()
                await interaction.response.send_message(
                    f"Successfully subscribed to {event.event_name}!"
                )
            except Exception as e:
                print(f"Error in add_event: {e}")
                await interaction.response.send_message(
                    f"Unable to subscribe to event {event.event_name}. {e}"
                )
        
    @app_commands.command(
        name = 'unsub',
        description = 'Unsubscribe to a reminder or all reminders.'
    )
    async def unsub(self, interaction:discord.Interaction, eid:int):
        async for session in get_db():
            stmt = select(Remindees).where(Remindees.event_id == eid and Remindees.discord_id == interaction.user.id)
            result = await session.execute(stmt)
            events = result.scalars().all()
            if not events:
                await interaction.response.send_message("You weren't subscribed to this event.")
                return
            embed = discord.Embed(
                title = 'Confirmation',
                description = 'Unsubscribe?',
                color = discord.Color.orange()
            )
            view = confirm_view.ConfirmView()
            await interaction.response.send_message(embed = embed, view = view)
            await view.wait()
            if view.value is None:
                await interaction.followup.send('Timed out.', ephemeral=True)
                return
            elif view.value:
                stmt = delete(Remindees).where(Remindees.event_id == eid and Remindees.discord_id == interaction.user.id)
                await session.commit()
                await interaction.followup.send('Successfully unsubscribed.')
            else:
                await interaction.followup.send('Still subscribed to the event.')

    @app_commands.command(
        name='list_subs',
        description='Lists all event you are currently subscribed to.'
    )
    async def list_subs(self, interaction : discord.Interaction):
        async for session in get_db():
            stmt = select(Event).join(Remindees, Event.event_id == Remindees.event_id).where(Remindees.discord_id == interaction.user.id)
            print(f"Executing {stmt}...")
            result = await session.execute(stmt)
            print(f"Finished executing {stmt}!")
            subs = result.scalars().all()
            
            if not subs:
                await interaction.response.send_message("You are currently not subscribed to any reminders.")
                return
            sub_list = "\n".join(
                f"**{sub.event_name}** - Resets at {sub.reset_time} UTC. ID: {sub.event_id}"
                for sub in subs
            )
            embed = discord.Embed(
                title = "Current Reminders",
                description = sub_list,
                color = discord.Color.blue(),
            )
            await interaction.response.send_message(embed = embed)

async def setup(bot):
    await bot.add_cog(UserManager(bot))