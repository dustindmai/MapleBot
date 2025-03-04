from discord.ext import commands
from discord import app_commands, Interaction
import asyncio

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name = "shutdown", description="Shuts down the bot.")
    @commands.is_owner()
    async def shutdown(self, interaction: Interaction):
        await interaction.response.send_message("Shutting down...")
        await self.cleanup()
        await self.bot.close()
        
    async def cleanup(self):
        if hasattr(self, 'db_session'):
            await self.db_session.close()
            
        for task in asyncio.all_tasks():
            task.cancel()
        
async def setup(bot):
    await bot.add_cog(Admin(bot))