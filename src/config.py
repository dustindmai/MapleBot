import os
from typing import Final

from dotenv import load_dotenv

## Setting up the bot
# Get environment variables
load_dotenv(dotenv_path="../.env")
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

