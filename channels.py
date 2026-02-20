"""
Channel Setup and Management for Turd Casino
Creates required channels on startup if they don't exist
"""

import logging
import discord
from config import CATEGORY_NAME, CHANNEL_GAMBLING, CHANNEL_BETS, CHANNEL_ADMIN, CHANNEL_ARCHIVE

logger = logging.getLogger(__name__)


class ChannelManager:
    """Manages channel setup and retrieval"""
    
    def __init__(self, bot):
        self.bot = bot
        self.category = None
        self.gambling_channel = None
        self.bets_channel = None
        self.admin_channel = None
        self.archive_channel = None
    
    async def setup_channels(self, guild: discord.Guild):
        """Set up all required channels for the server"""
        logger.info(f"[CHANNELS] Setting up channels for {guild.name}")
        
        # Find or create the Turd Casino category
        self.category = await self._get_or_create_category(guild)
        
        # Get or create each channel
        self.gambling_channel = await self._get_or_create_channel(
            guild, CHANNEL_GAMBLING, "Dashboard and main interactions"
        )
        
        self.bets_channel = await self._get_or_create_channel(
            guild, CHANNEL_BETS, "Active bets with threads"
        )
        
        self.admin_channel = await self._get_or_create_channel(
            guild, CHANNEL_ADMIN, "Dispute notifications"
        )
        
        self.archive_channel = await self._get_or_create_channel(
            guild, CHANNEL_ARCHIVE, "Completed bets for review"
        )
        
        # Move channels to category
        await self._move_channels_to_category(guild)
        
        logger.info("[CHANNELS] All channels set up successfully!")
        return True
    
    async def _get_or_create_category(self, guild: discord.Guild) -> discord.CategoryChannel:
        """Find or create the Turd Casino category"""
        # Look for existing category
        for category in guild.categories:
            if category.name == CATEGORY_NAME:
                logger.info(f"[CHANNELS] Found existing category: {CATEGORY_NAME}")
                return category
        
        # Create new category
        logger.info(f"[CHANNELS] Creating new category: {CATEGORY_NAME}")
        category = await guild.create_category(
            name=CATEGORY_NAME,
            reason="Turd Casino channel setup"
        )
        return category
    
    async def _get_or_create_channel(self, guild: discord.Guild, name: str, topic: str = None) -> discord.TextChannel:
        """Find or create a channel within the category"""
        # Look for existing channel
        for channel in guild.text_channels:
            if channel.name == name and channel.category and channel.category.name == CATEGORY_NAME:
                logger.info(f"[CHANNELS] Found existing channel: {name}")
                return channel
        
        # Also check if channel exists in guild but not in category
        for channel in guild.text_channels:
            if channel.name == name:
                logger.info(f"[CHANNELS] Found existing channel (no category): {name}")
                return channel
        
        # Create new channel
        logger.info(f"[CHANNELS] Creating new channel: {name}")
        
        # First create without category, then move
        channel = await guild.create_text_channel(
            name=name,
            topic=topic,
            reason=f"Turd Casino channel setup: {name}"
        )
        
        return channel
    
    async def _move_channels_to_category(self, guild: discord.Guild):
        """Move all Turd Casino channels to the category"""
        channels_to_move = [
            (self.gambling_channel, CHANNEL_GAMBLING),
            (self.bets_channel, CHANNEL_BETS),
            (self.admin_channel, CHANNEL_ADMIN),
            (self.archive_channel, CHANNEL_ARCHIVE),
        ]
        
        for channel, name in channels_to_move:
            if channel and channel.category != self.category:
                try:
                    await channel.edit(category=self.category)
                    logger.info(f"[CHANNELS] Moved #{name} to {CATEGORY_NAME}")
                except Exception as e:
                    logger.error(f"[CHANNELS] Failed to move #{name}: {e}")
    
    def get_gambling_channel(self) -> discord.TextChannel:
        """Get the gambling/dashboard channel"""
        return self.gambling_channel
    
    def get_bets_channel(self) -> discord.TextChannel:
        """Get the bets channel"""
        return self.bets_channel
    
    def get_admin_channel(self) -> discord.TextChannel:
        """Get the admin channel"""
        return self.admin_channel
    
    def get_archive_channel(self) -> discord.TextChannel:
        """Get the archive channel"""
        return self.archive_channel
    
    async def create_bet_thread(self, bet_id: str, bet_topic: str) -> discord.Thread:
        """Create a thread for a new bet in the bets channel"""
        if not self.bets_channel:
            logger.error("[CHANNELS] Bets channel not set up!")
            return None
        
        # Create a public thread for the bet
        thread = await self.bets_channel.create_thread(
            name=f"🎲 {bet_topic[:50]}",
            type=discord.ChannelType.public_thread,
            auto_archive_duration=10080  # 1 week
        )
        
        logger.info(f"[CHANNELS] Created bet thread: {thread.name}")
        return thread
    
    async def post_to_archive(self, embed: discord.Embed):
        """Post a completed bet to the archive channel"""
        if not self.archive_channel:
            logger.error("[CHANNELS] Archive channel not set up!")
            return
        
        await self.archive_channel.send(embed=embed)
        logger.info("[CHANNELS] Posted to archive")
    
    async def post_dispute_to_admin(self, embed: discord.Embed):
        """Post a dispute to the admin channel"""
        if not self.admin_channel:
            logger.error("[CHANNELS] Admin channel not set up!")
            return
        
        await self.admin_channel.send(embed=embed)
        logger.info("[CHANNELS] Posted dispute to admin")
