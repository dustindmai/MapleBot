import enum
from sqlalchemy.future import select
from database import get_db_async
from models import Event

class DynamicEventEnum(enum.Enum):
    
    PLACEHOLDER = 0
    
async def generate_event_enum():
    
    async for db in get_db_async():
        result = await db.execute(select(Event.event_id, Event.event_name))
        events = result.all()
        
        event_dict = {name.upper().replace(" ", "_"): eid for eid, name in events}
        return enum.Enum("DynamicEventEnum", event_dict)
    
EVENT_ENUM = None

async def initialize_event_enum():
    global EVENT_ENUM
    EVENT_ENUM = await generate_event_enum()