from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from models import Base
import config

engine = create_async_engine(config.DATABASE.replace("postgresql://","postgresql+asyncpg://"), echo = True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def init_db():
    
    async with engine.begin() as conn:
        print("Initializing Database")
        await conn.run_sync(Base.metadata.create_all)
        print("Database initialized")