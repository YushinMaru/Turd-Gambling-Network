"""
Bet Thread Views - Win/Lose/Dispute buttons for bet threads
"""

import discord
from discord import ui
from discord.ui import View
import logging

logger = logging.getLogger(__name__)


class BetThreadView(View):
    """View with Win/Lose/Dispute buttons for bet threads"""
    
    def __init__(self, bet_id: str, creator_id: str, joiner_id: str = None, channel_manager = None):
        super().__init__(timeout=None, persistent=True)
        self.bet_id = bet_id
        self.creator_id = creator_id
        self.joiner_id = joiner_id
        self.channel_manager = channel_manager
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow participants to use buttons"""
        user_id = str(interaction.user.id)
        
        # Allow creator and joiner
        if user_id == self.creator_id or user_id == self.joiner_id:
            return True
        
        # Allow admin
        if interaction.user.guild_permissions.administrator:
            return True
        
        await interaction.response.send_message(
            "❌ Only bet participants can use these buttons.",
            ephemeral=True
        )
        return False


class IWinButton(ui.Button):
    """Button to claim victory"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="✅ I Win!",
            style=discord.ButtonStyle.success,
            custom_id=f"bet_iwin_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        # Get the view's bet info
        view: BetThreadView = self.view
        
        # Get the bet manager from the bot
        bot = interaction.client
        db = bot.db
        currency = bot.currency
        bet_manager = bot.bet_manager
        channel_manager = bot.channel_manager
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        if bet['status'] != 'pending':
            await interaction.response.send_message(
                f"❌ This bet is already {bet['status']}.", 
                ephemeral=True
            )
            return
        
        # Resolve bet with this user as winner
        success, message = bet_manager.resolve_bet(self.bet_id, user_id)
        
        if success:
            # Post to archive
            if channel_manager:
                embed = discord.Embed(
                    title=f"🎉 Bet Resolved - {self.bet_id}",
                    description=f"**Winner:** {interaction.user.display_name}",
                    color=0x2ECC71
                )
                embed.add_field(name="Topic", value=bet['bet_topic'], inline=True)
                embed.add_field(name="Amount", value=f"{bet['amount']:,} TC", inline=True)
                await channel_manager.post_to_archive(embed)
            
            # Update the thread
            embed = discord.Embed(
                title=f"✅ Bet Resolved",
                description=f"**Winner:** {interaction.user.display_name}",
                color=0x2ECC71
            )
            
            # Disable buttons
            for item in self.view.children:
                item.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self.view)
        else:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)


class ILoseButton(ui.Button):
    """Button to admit defeat"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="❌ I Lose",
            style=discord.ButtonStyle.danger,
            custom_id=f"bet_ilose_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        # Get the bet manager from the bot
        bot = interaction.client
        db = bot.db
        currency = bot.currency
        bet_manager = bot.bet_manager
        channel_manager = bot.channel_manager
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        if bet['status'] != 'pending':
            await interaction.response.send_message(
                f"❌ This bet is already {bet['status']}.", 
                ephemeral=True
            )
            return
        
        # Get participants
        participants = db.get_bet_participants(self.bet_id)
        
        # Find the other user (winner)
        winner_id = None
        for p in participants:
            if p['user_id'] != user_id:
                winner_id = p['user_id']
                break
        
        if not winner_id:
            await interaction.response.send_message(
                "❌ Can't resolve - need both parties.",
                ephemeral=True
            )
            return
        
        # Resolve bet with the other user as winner
        success, message = bet_manager.resolve_bet(self.bet_id, winner_id)
        
        if success:
            # Post to archive
            if channel_manager:
                winner_user = await bot.fetch_user(winner_id)
                embed = discord.Embed(
                    title=f"🎉 Bet Resolved - {self.bet_id}",
                    description=f"**Winner:** {winner_user.display_name if winner_user else 'Unknown'}",
                    color=0x2ECC71
                )
                embed.add_field(name="Topic", value=bet['bet_topic'], inline=True)
                embed.add_field(name="Amount", value=f"{bet['amount']:,} TC", inline=True)
                await channel_manager.post_to_archive(embed)
            
            # Update the thread
            winner_user = await bot.fetch_user(winner_id)
            embed = discord.Embed(
                title=f"✅ Bet Resolved",
                description=f"**Winner:** {winner_user.display_name if winner_user else 'Unknown'}",
                color=0x2ECC71
            )
            
            # Disable buttons
            for item in self.view.children:
                item.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self.view)
        else:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)


class DisputeButton(ui.Button):
    """Button to file a dispute"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="⚠️ Dispute",
            style=discord.ButtonStyle.warning,
            custom_id=f"bet_dispute_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        # Get the bet manager from the bot
        bot = interaction.client
        db = bot.db
        channel_manager = bot.channel_manager
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Get participants
        participants = db.get_bet_participants(self.bet_id)
        
        # Find the other user
        other_user_id = None
        for p in participants:
            if p['user_id'] != user_id:
                other_user_id = p['user_id']
                break
        
        other_user = await bot.fetch_user(other_user_id) if other_user_id else None
        
        # Send to admin channel
        if channel_manager:
            embed = discord.Embed(
                title=f"⚠️ Dispute Filed - {self.bet_id}",
                description=f"**Filed by:** {interaction.user.display_name}",
                color=0xF39C12
            )
            embed.add_field(name="Topic", value=bet['bet_topic'], inline=True)
            embed.add_field(name="Amount", value=f"{bet['amount']:,} TC", inline=True)
            if other_user:
                embed.add_field(name="Opponent", value=other_user.display_name, inline=True)
            embed.add_field(
                name="Reason", 
                value="User filed a dispute. Please review and resolve manually.",
                inline=False
            )
            
            await channel_manager.post_dispute_to_admin(embed)
        
        await interaction.response.send_message(
            "⚠️ Dispute filed! An admin will review this bet.",
            ephemeral=True
        )


def create_bet_thread_view(bet_id: str, creator_id: str, joiner_id: str = None) -> BetThreadView:
    """Create a view with Win/Lose/Dispute buttons for a bet thread"""
    view = BetThreadView(bet_id, creator_id, joiner_id)
    
    # Add buttons
    view.add_item(IWinButton(bet_id))
    view.add_item(ILoseButton(bet_id))
    view.add_item(DisputeButton(bet_id))
    
    return view


async def post_bet_to_channel(bet_id: str, bet_topic: str, amount: int, creator_name: str, 
                             channel_manager, bot) -> discord.Message:
    """Post a bet to the #turd-bets channel with a thread"""
    
    bets_channel = channel_manager.get_bets_channel()
    
    if not bets_channel:
        logger.error("[BET_THREAD] Bets channel not available!")
        return None
    
    # Create embed for the bet
    embed = discord.Embed(
        title=f"🎲 New Bet: {bet_topic}",
        description=f"**Bet ID:** `{bet_id}`",
        color=0x9B59B6
    )
    embed.add_field(name="Amount", value=f"💰 **{amount:,}** Turd Coins", inline=True)
    embed.add_field(name="Creator", value=creator_name, inline=True)
    embed.add_field(name="Status", value="🔴 **OPEN** - Waiting for opponent!", inline=True)
    embed.set_footer(text="Use the Bet ID to join • Turd Casino")
    
    # Send message and create thread
    message = await bets_channel.send(embed=embed)
    
    # Create a public thread
    thread = await message.create_thread(
        name=f"🎲 {bet_topic[:50]}",
        type=discord.ChannelType.public_thread,
        auto_archive_duration=10080  # 1 week
    )
    
    # Send initial thread message with buttons
    thread_embed = discord.Embed(
        title="🎯 Bet Details",
        description=f"**Topic:** {bet_topic}\n**Amount:** {amount:,} TC\n**Creator:** {creator_name}",
        color=0x9B59B6
    )
    thread_embed.add_field(
        name="How to Join",
        value="Go to the dashboard and click 'Join Bet', then enter this Bet ID.",
        inline=False
    )
    
    # Add view with Win/Lose/Dispute buttons
    view = create_bet_thread_view(bet_id, None)
    
    await thread.send(embed=thread_embed, view=view)
    
    logger.info(f"[BET_THREAD] Posted bet {bet_id} to #turd-bets with thread")
    
    return message
