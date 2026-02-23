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
        self.check_scheduled_verifications.start()
        
        logger.info("[SETUP] Setup complete!")
    
    async def post_admin_panel(self):
        """Post admin panel to admin channel for each guild"""
        for guild in self.guilds:
            try:
                await self.channel_manager.setup_channels(guild)
                admin_channel = self.channel_manager.get_admin_channel(guild.id)
                
                if admin_channel:
                    # Purge and post
                    try:
                        await admin_channel.purge(check=lambda m: True)
                    except:
                        pass
                    
                    # Build admin panel
                    embed = discord.Embed(
                        title="🛡️ Turd Casino Admin Panel",
                        description="Manage bets and resolve disputes",
                        color=0xF39C12
                    )
                    
                    from dashboard_views import AdminBetResolveView
                    view = AdminBetResolveView(self, self.db, self.channel_manager)
                    
                    await admin_channel.send(embed=embed, view=view)
                    logger.info(f"[ADMIN] Posted admin panel to {guild.name}")
            except Exception as e:
                logger.error(f"[ADMIN] Error posting admin panel: {e}")
    
    async def on_ready(self):
        """Bot ready"""
        logger.info(f"[BOT] Turd Casino is ready: {self.user}")
        logger.info(f"[BOT] Bot ID: {self.user.id}")
        
        # Set up channels for ALL guilds the bot is in
        for guild in self.guilds:
            logger.info(f"[BOT] Setting up channels for server: {guild.name}")
            await self.channel_manager.setup_channels(guild)
        
        # Post initial dashboard to all channels (not just once)
        if not hasattr(self, '_dashboard_posted') or not self._dashboard_posted:
            self._dashboard_posted = True
            await self.post_dashboard_for_all_guilds()
            await self.post_admin_panel()
    
    async def post_dashboard_for_all_guilds(self):
        """Post dashboard to each guild's gambling channel"""
        logger.info(f"[DASHBOARD] Starting dashboard post for {len(self.guilds)} guilds")
        
        for guild in self.guilds:
            logger.info(f"[DASHBOARD] Processing guild: {guild.name} (id: {guild.id})")
            try:
                # Set up channels for this guild to get the right channel
                await self.channel_manager.setup_channels(guild)
                channel = self.channel_manager.get_gambling_channel(guild.id)
                
                logger.info(f"[DASHBOARD] Channel for {guild.name}: {channel}")
                
                if channel:
                    logger.info(f"[DASHBOARD] Found channel #{channel.name} in {guild.name}")
                    
                    # Purge and post
                    try:
                        await channel.purge(check=lambda m: True)
                    except Exception as e:
                        logger.warning(f"[DASHBOARD] Could not purge {channel.name}: {e}")
                    
                    embed = self.dashboard_builder.build_dashboard(guild)
                    sent_msg = await channel.send(embed=embed, view=self.dashboard_view)
                    logger.info(f"[DASHBOARD] Posted message {sent_msg.id} to #{channel.name} in {guild.name} (channel id: {channel.id})")
                else:
                    logger.warning(f"[DASHBOARD] No gambling channel found for {guild.name}")
            except Exception as e:
                logger.error(f"[DASHBOARD] Error posting to {guild.name}: {e}", exc_info=True)
    
    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a new server"""
        logger.info(f"[BOT] Joined new server: {guild.name} (ID: {guild.id})")
        
        # Set up channels for the new server
        await self.channel_manager.setup_channels(guild)
        
        logger.info(f"[BOT] Channels set up for {guild.name}")
    
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
    
    @tasks.loop(seconds=60)
    async def dashboard_refresh(self):
        """Refresh dashboard periodically for all guilds"""
        try:
            await self.post_dashboard_for_all_guilds()
        except Exception as e:
            logger.error(f"[DASHBOARD] Refresh error: {e}")
    
    @dashboard_refresh.before_loop
    async def before_dashboard_refresh(self):
        """Wait for bot to be ready"""
        await self.wait_until_ready()
    
    @tasks.loop(minutes=5)
    async def check_scheduled_verifications(self):
        """Check for scheduled bets that need verification"""
        try:
            await self._check_scheduled_bets()
        except Exception as e:
            logger.error(f"[SCHEDULED] Error checking scheduled bets: {e}")
    
    @check_scheduled_verifications.before_loop
    async def before_scheduled_check(self):
        """Wait for bot to be ready"""
        await self.wait_until_ready()
    
    async def _check_scheduled_bets(self):
        """Check and process scheduled bets"""
        from datetime import datetime
        
        conn = self.db.get_connection()
        c = conn.cursor()
        
        # Get pending bets with scheduled verification dates
        c.execute('''SELECT bet_id, bet_topic, verification_type, verification_date, verification_url, verification_claim
                    FROM bets 
                    WHERE status = 'pending' 
                    AND (verification_type = 'scheduled' OR verification_type = 'ai')
                    AND verification_date IS NOT NULL''')
        
        bets = c.fetchall()
        conn.close()
        
        now = datetime.now()
        
        for bet in bets:
            bet_id, topic, verif_type, verif_date, verif_url, verif_claim = bet
            
            if not verif_date:
                continue
            
            try:
                # Parse the verification date
                scheduled_dt = datetime.strptime(verif_date, '%Y-%m-%d %H:%M')
                
                if now >= scheduled_dt:
                    logger.info(f"[SCHEDULED] Processing bet {bet_id} - verification time reached")
                    
                    if verif_type == 'ai' and verif_url and verif_claim:
                        # Run AI verification
                        from verification import verify_bet
                        
                        success, result = await verify_bet(bet_id, verif_url, verif_claim, self.db)
                        
                        if success and '|' in result:
                            result_type, explanation = result.split('|')
                            
                            # Get participants to determine winner
                            participants = self.db.get_bet_participants(bet_id)
                            
                            if result_type == "WIN_A" and len(participants) >= 1:
                                winner_id = participants[0]['user_id']
                            elif result_type == "WIN_B" and len(participants) >= 2:
                                winner_id = participants[1]['user_id']
                            else:
                                winner_id = None
                            
                            if winner_id:
                                # Resolve the bet
                                self.bet_manager.resolve_bet(bet_id, winner_id)
                                logger.info(f"[SCHEDULED] Bet {bet_id} resolved via AI - winner: {winner_id}")
                            else:
                                logger.warning(f"[SCHEDULED] Could not determine winner for {bet_id}")
                        else:
                            logger.warning(f"[SCHEDULED] AI verification failed for {bet_id}: {result}")
                    
                    elif verif_type == 'scheduled':
                        # Ping participants to resolve
                        participants = self.db.get_bet_participants(bet_id)
                        
                        for p in participants:
                            user = await self.fetch_user(p['user_id'])
                            if user:
                                # Try to DM user
                                try:
                                    embed = discord.Embed(
                                        title="⏰ Time to Resolve Your Bet!",
                                        description=f"Your bet is ready for resolution:\n\n**{topic}**\n\nPlease click 'I Win' or 'I Lose' in the bet thread.",
                                        color=0xF39C12
                                    )
                                    await user.send(embed=embed)
                                except:
                                    pass  # Can't DM
                        
                        logger.info(f"[SCHEDULED] Sent resolution reminders for {bet_id}")
                        
            except Exception as e:
                logger.error(f"[SCHEDULED] Error processing bet {bet_id}: {e}")
    
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
    
    @commands.command(name="dashboard")
    async def dashboard_cmd(self, ctx):
        """Force refresh the dashboard"""
        if not ctx.guild:
            await ctx.send("This command must be used in a server!")
            return
        
        channel = self.channel_manager.get_gambling_channel(ctx.guild.id)
        if not channel:
            await ctx.send("Gambling channel not found!")
            return
        
        try:
            await channel.purge(check=lambda m: True)
        except:
            pass
        
        embed = self.dashboard_builder.build_dashboard(ctx.guild)
        await channel.send(embed=embed, view=self.dashboard_view)
        await ctx.send("✅ Dashboard refreshed!")


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
