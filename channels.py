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
        # Store channels per guild
        self.guild_channels = {}  # guild_id -> {category, gambling_channel, bets_channel, admin_channel, archive_channel}
    
    async def setup_channels(self, guild: discord.Guild):
        """Set up all required channels for the server"""
        logger.info(f"[CHANNELS] Setting up channels for {guild.name}")
        
        # Find or create the Turd Casino category
        category = await self._get_or_create_category(guild)
        
        # Get or create each channel
        gambling_channel = await self._get_or_create_channel(
            guild, CHANNEL_GAMBLING, "Dashboard and main interactions"
        )
        
        bets_channel = await self._get_or_create_channel(
            guild, CHANNEL_BETS, "Active bets with threads"
        )
        
        admin_channel = await self._get_or_create_channel(
            guild, CHANNEL_ADMIN, "Dispute notifications"
        )
        
        archive_channel = await self._get_or_create_channel(
            guild, CHANNEL_ARCHIVE, "Completed bets for review"
        )
        
        # Move channels to category
        await self._move_channels_to_category(guild, category, gambling_channel, bets_channel, admin_channel, archive_channel)
        
        # Store per guild
        self.guild_channels[guild.id] = {
            'category': category,
            'gambling_channel': gambling_channel,
            'bets_channel': bets_channel,
            'admin_channel': admin_channel,
            'archive_channel': archive_channel,
        }
        
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
        """Find or create a channel within the SPECIFIC guild"""
        # Look for existing channel IN THIS GUILD ONLY
        for channel in guild.text_channels:
            if channel.name == name:
                logger.info(f"[CHANNELS] Found existing channel in {guild.name}: {name}")
                return channel
        
        # Create new channel in THIS guild
        logger.info(f"[CHANNELS] Creating new channel in {guild.name}: {name}")
        
        channel = await guild.create_text_channel(
            name=name,
            topic=topic,
            reason=f"Turd Casino channel setup: {name}"
        )
        
        return channel
    
    async def _move_channels_to_category(self, guild: discord.Guild, category, gambling_channel, bets_channel, admin_channel, archive_channel):
        """Move all Turd Casino channels to the category"""
        channels_to_move = [
            (gambling_channel, CHANNEL_GAMBLING),
            (bets_channel, CHANNEL_BETS),
            (admin_channel, CHANNEL_ADMIN),
            (archive_channel, CHANNEL_ARCHIVE),
        ]
        
        for channel, name in channels_to_move:
            if channel and channel.category != category:
                try:
                    await channel.edit(category=category)
                    logger.info(f"[CHANNELS] Moved #{name} to {CATEGORY_NAME}")
                except Exception as e:
                    logger.error(f"[CHANNELS] Failed to move #{name}: {e}")
    
    def get_gambling_channel(self, guild_id: int = None) -> discord.TextChannel:
        """Get the gambling/dashboard channel"""
        if guild_id and guild_id in self.guild_channels:
            return self.guild_channels[guild_id].get('gambling_channel')
        # Return first available
        for gid in self.guild_channels:
            return self.guild_channels[gid].get('gambling_channel')
        return None
    
    def get_bets_channel(self, guild_id: int = None) -> discord.TextChannel:
        """Get the bets channel"""
        if guild_id and guild_id in self.guild_channels:
            return self.guild_channels[guild_id].get('bets_channel')
        for gid in self.guild_channels:
            return self.guild_channels[gid].get('bets_channel')
        return None
    
    def get_admin_channel(self, guild_id: int = None) -> discord.TextChannel:
        """Get the admin channel"""
        if guild_id and guild_id in self.guild_channels:
            return self.guild_channels[guild_id].get('admin_channel')
        for gid in self.guild_channels:
            return self.guild_channels[gid].get('admin_channel')
        return None
    
    def get_archive_channel(self, guild_id: int = None) -> discord.TextChannel:
        """Get the archive channel"""
        if guild_id and guild_id in self.guild_channels:
            return self.guild_channels[guild_id].get('archive_channel')
        for gid in self.guild_channels:
            return self.guild_channels[gid].get('archive_channel')
        return None
    
    async def create_bet_thread(self, bet_id: str, bet_topic: str, guild_id: int = None) -> discord.Thread:
        """Create a thread for a new bet in the bets channel"""
        bets_channel = self.get_bets_channel(guild_id)
        if not bets_channel:
            logger.error("[CHANNELS] Bets channel not set up!")
            return None
        
        # Create a public thread for the bet
        thread = await bets_channel.create_thread(
            name=f"🎲 {bet_topic[:50]}",
            type=discord.ChannelType.public_thread,
            auto_archive_duration=10080  # 1 week
        )
        
        logger.info(f"[CHANNELS] Created bet thread: {thread.name}")
        return thread
    
    async def post_to_archive(self, embed: discord.Embed, guild_id: int = None):
        """Post a completed bet to the archive channel"""
        archive_channel = self.get_archive_channel(guild_id)
        if not archive_channel:
            logger.error("[CHANNELS] Archive channel not set up!")
            return
        
        await archive_channel.send(embed=embed)
        logger.info("[CHANNELS] Posted to archive")
    
    async def post_dispute_to_admin(self, embed: discord.Embed, guild_id: int = None):
        """Post a dispute to the admin channel"""
        admin_channel = self.get_admin_channel(guild_id)
        if not admin_channel:
            logger.error("[CHANNELS] Admin channel not set up!")
            return
        
        await admin_channel.send(embed=embed)
        logger.info("[CHANNELS] Posted dispute to admin")
