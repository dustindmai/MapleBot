import enum
from sqlalchemy.future import select
#from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from discord import app_commands
from database import get_db
from models import Event

class EventEnum(enum.Enum):
    # Define event_map as a class-level dictionary
    event_map = {}

    @classmethod
    async def load_events(cls):
        # Use async database session to load events
        async for session in get_db():
            stmt = select(Event)
            result = await session.execute(stmt)
            events = result.scalars().all()  # Ensure you're using .scalars() properly
            print(type(cls.event_map))
            # Clear the existing event_map and repopulate with fresh data
            #cls.event_map.clear()  # Now `event_map` is the dictionary, so this will work
            
            # Populate event_map with event_name as the key and event_id as the value
            for event in events:
                cls.event_map[event.event_name.upper().replace(" ", "_")] = event.event_id

    @classmethod
    def get_event_id(cls, name: str):
        # Access event_map to retrieve the event_id based on the name
        return cls.event_map.get(name.upper().replace(" ", "_"))

    @classmethod
    def choices(cls) -> List[app_commands.Choice[int]]:
        # Build the choices list for Discord commands from event_map
        return [app_commands.Choice(name=event_name.replace("_", " ").title(), value=event_id)
                for event_name, event_id in cls.event_map.items()]
