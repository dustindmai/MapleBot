import os
from typing import Final

from dotenv import load_dotenv

## Setting up the bot
# Get environment variables
# load_dotenv(dotenv_path="C:\\Users\\dusti\\Projects\\MapleBot\\.env")
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
DATABASE: Final[str] = os.getenv("DATABASE_URL")
