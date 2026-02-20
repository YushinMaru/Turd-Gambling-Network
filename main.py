"""
Turd Gambling Network - Main Bot Entry Point
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

import discord
from discord.ext import commands, tasks

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    DISCORD_BOT_TOKEN, DB_PATH,
    LOG_FILE, LOG_MAX_BYTES, EMBED_COLOR
)
from database import DatabaseManager
from database_init import DatabaseInitializer
from currency import CurrencyManager
from bets import BetManager
from dashboard import DashboardBuilder
from dashboard_views import setup_dashboard_view
from channels import ChannelManager


# ============== LOGGING SETUP ==============
def setup_logging():
    """Set up logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ============== BOT CLASS ==============
class TurdCasinoBot(commands.Bot):
    """Main bot class for Turd Casino"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        
        logger.info("[INIT] Loading Turd Gambling Network...")
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Initialize managers
        self.currency = CurrencyManager(self.db)
        self.bet_manager = BetManager(self.db, self.currency)
        self.dashboard_builder = DashboardBuilder(self.db, self.currency, self.bet_manager)
        
        # Channel manager
        self.channel_manager = ChannelManager(self)
        
        # Dashboard view will be set up in setup_hook
        self.dashboard_view = None
        self.dashboard_message = None
        
        logger.info("[INIT] All components loaded!")
    
    async def setup_hook(self):
        """Set up the bot"""
        logger.info("[SETUP] Setting up bot...")
        
        # Set up dashboard view
        self.dashboard_view = setup_dashboard_view(
            self, self.db, self.currency, self.bet_manager, self.dashboard_builder, self.channel_manager
        )
        
        # Register persistent view
        self.add_view(self.dashboard_view)
        
        # Start background tasks
        self.dashboard_refresh.start()
        
        logger.info("[SETUP] Setup complete!")
    
    async def on_ready(self):
        """Bot ready"""
        logger.info(f"[BOT] Turd Casino is ready: {self.user}")
        logger.info(f"[BOT] Bot ID: {self.user.id}")
        
        # Set up channels for the first guild
        if self.guilds:
            guild = self.guilds[0]
            await self.channel_manager.setup_channels(guild)
        
        # Post initial dashboard
        await self.post_dashboard()
    
    async def post_dashboard(self):
        """Post the dashboard to the gambling channel"""
        try:
            # Use the gambling channel from channel manager
            channel = self.channel_manager.get_gambling_channel()
            
            if not channel:
                logger.warning("[DASHBOARD] Gambling channel not set up yet!")
                return
            
            # Purge all messages in the channel
            try:
                await channel.purge(check=lambda m: True)
                logger.info("[DASHBOARD] Purged channel")
            except Exception as e:
                logger.warning(f"[DASHBOARD] Could not purge channel: {e}")
            
            # Get guild for dashboard
            guild = channel.guild
            
            # Build and post dashboard
            embed = self.dashboard_builder.build_dashboard(guild)
            self.dashboard_message = await channel.send(embed=embed, view=self.dashboard_view)
            
            logger.info(f"[DASHBOARD] Posted to #{channel.name}")
            
        except Exception as e:
            logger.error(f"[DASHBOARD] Error posting dashboard: {e}")
    
    @tasks.loop(minutes=10)
    async def dashboard_refresh(self):
        """Refresh dashboard periodically"""
        try:
            await self.post_dashboard()
        except Exception as e:
            logger.error(f"[DASHBOARD] Refresh error: {e}")
    
    @dashboard_refresh.before_loop
    async def before_dashboard_refresh(self):
        """Wait for bot to be ready"""
        await self.wait_until_ready()
    
    async def on_message(self, message):
        """Handle messages"""
        # Don't respond to bots
        if message.author.bot:
            return
        
        # Ensure user exists in database
        user_id = str(message.author.id)
        username = message.author.name
        display_name = message.author.display_name
        self.db.ensure_user_exists(user_id, username, display_name)
        
        # Process commands
        await self.process_commands(message)


# ============== MAIN ==============
async def run_bot():
    """Run the bot"""
    print("=" * 50)
    print("🎰 TURD CASINO")
    print("=" * 50)
    print("Custom Bets - Dashboard Only")
    print("=" * 50)
    
    if not DISCORD_BOT_TOKEN:
        logger.error("No Discord bot token found! Set DISCORD_BOT_TOKEN in .env")
        return
    
    # Initialize database
    initializer = DatabaseInitializer(DB_PATH)
    initializer.init_database()
    logger.info("Database initialized")
    
    # Run bot
    bot = TurdCasinoBot()
    
    try:
        await bot.start(DISCORD_BOT_TOKEN)
    except discord.errors.LoginFailure:
        logger.error("Invalid Discord bot token!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await bot.close()


def main():
    """Main entry point"""
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
