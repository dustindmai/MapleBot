import asyncio
from database import AsyncSessionLocal 
from models import Event
from datetime import time, timedelta
from sqlalchemy.future import select
async def test_db():
    async with AsyncSessionLocal() as session:
        
        new_event = Event(
            event_name="test event",
            reset_time = time(0,0),
            reset_type = "daily",
            reset_interval = timedelta(days=1),
            reset_day = None
        )
        session.add(new_event)
        await session.commit()
        
        result = await session.execute(select(Event))
        events=result.scalars().all()
        
        print("Database query result: ")
        for event in events:
            print(f"{event.event_id}")
            
asyncio.run(test_db())