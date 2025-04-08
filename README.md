# MapleStory Reminder Bot

A feature-rich, fully asynchronous Discord bot designed to help MapleStory players manage daily, weekly, and monthly reset events. Built with Python and Discord's slash command framework, the bot delivers scheduled reminders, user subscriptions, and customizable DM alerts.

## Features

- 🕒 **Automated Reminders**  
  Sends personalized DM notifications to users when their subscribed events reset.

- 🧠 **Dynamic Event Management**  
  Add, edit, and remove in-game reset events through admin-only commands.

- 🎯 **Subscription System**  
  Users can subscribe to events and receive timely reminders.

- 🧑‍🤝‍🧑 **Role-based & DM Notifications**  
  Choose between role mentions or private DMs.

- 📅 **Support for Daily, Weekly, Monthly Intervals**  
  Accurately handles recurring event resets.

## Tech Stack

- **Python 3.11+**
- **discord.py** with `app_commands` for modern slash commands
- **PostgreSQL** with SQLAlchemy (async ORM)
- **AsyncIO** for event loops and database calls


## Setup & Installation

1. **Clone the repo:**
   ```console
   git clone https://github.com/yourusername/maplestory-reminder-bot.git
   cd maplestory-reminder-bot
   ```
2. **Create and activate a virtual environment:**
   ```console
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```console
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   create a .env file and include:
   ```console
   DISCORD_TOKEN=your_token_here
   DATABASE_URL=your_async_postgres_url
   ```
5. **Initialize the database:**
   ```console
   python src/database.py
   ```
6. **Start the bot:**
   ```console
   python src/bot.py
   ```
