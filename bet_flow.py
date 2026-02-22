"""
Bet Flow - Multi-step bet creation through private threads
Handles opponent selection, bet type, category, odds, visibility, and expiration
"""

import discord
from discord import ui
from discord.ui import View
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# Constants
BET_TYPES = [
    ("1v1", "1v1 - Head to Head"),
    ("1vMany", "1vMany - You vs Multiple Opponents"),
    ("ManyvMany", "ManyvMany - Team vs Team"),
]

CATEGORIES = [
    ("Sports", "Sports"),
    ("Gaming", "Gaming"),
    ("Real Life", "Real Life"),
    ("Random", "Random/Challenge"),
]

ODDS = [
    ("even", "Even (1:1)"),
    ("2:1", "2:1"),
    ("3:1", "3:1"),
    ("custom", "Custom Odds"),
]

VISIBILITY = [
    ("open", "Open - Anyone can join"),
    ("invite", "Invite Only - Only invited users"),
]

EXPIRATION = [
    ("24h", "24 Hours"),
    ("7d", "7 Days"),
    ("never", "Never"),
]

VERIFICATION_TYPES = [
    ("manual", "Manual - Admin approves winner"),
    ("link", "Link Proof - Submit URL as evidence"),
    ("scheduled", "Scheduled - Auto-resolve at time"),
    ("poll", "Poll Vote - Server votes on winner"),
]

# Flow states
FLOW_STATE = {}  # user_id -> current step data


class BetFlowView(View):
    """View for selecting bet options"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(timeout=300)  # 5 minute timeout
        self.flow_data = flow_data


class BetTypeSelect(ui.Select):
    """Select bet type"""
    
    def __init__(self, flow_data: Dict):
        options = [
            discord.SelectOption(label=label, value=value, description=desc)
            for value, label in BET_TYPES
        ]
        super().__init__(placeholder="Select bet type...", options=options, custom_id="bet_type_select")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['bet_type'] = self.values[0]
        await interaction.response.defer()
        # Continue to next step
        await send_category_prompt(interaction, self.flow_data)


class CategorySelect(ui.Select):
    """Select bet category"""
    
    def __init__(self, flow_data: Dict):
        options = [
            discord.SelectOption(label=label, value=value)
            for value, label in CATEGORIES
        ]
        super().__init__(placeholder="Select category...", options=options, custom_id="category_select")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['category'] = self.values[0]
        await interaction.response.defer()
        # Continue to next step
        await send_odds_prompt(interaction, self.flow_data)


class OddsSelect(ui.Select):
    """Select payout odds"""
    
    def __init__(self, flow_data: Dict):
        options = [
            discord.SelectOption(label=label, value=value)
            for value, label in ODDS
        ]
        super().__init__(placeholder="Select odds...", options=options, custom_id="odds_select")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['odds'] = self.values[0]
        await interaction.response.defer()
        # Continue to next step
        await send_visibility_prompt(interaction, self.flow_data)


class VisibilitySelect(ui.Select):
    """Select visibility"""
    
    def __init__(self, flow_data: Dict):
        options = [
            discord.SelectOption(label=label, value=value)
            for value, label in VISIBILITY
        ]
        super().__init__(placeholder="Select visibility...", options=options, custom_id="visibility_select")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['visibility'] = self.values[0]
        await interaction.response.defer()
        # Continue to next step
        await send_expiration_prompt(interaction, self.flow_data)


class ExpirationSelect(ui.Select):
    """Select expiration"""
    
    def __init__(self, flow_data: Dict):
        options = [
            discord.SelectOption(label=label, value=value)
            for value, label in EXPIRATION
        ]
        super().__init__(placeholder="Select expiration...", options=options, custom_id="expiration_select")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['expiration'] = self.values[0]
        await interaction.response.defer()
        # Continue to next step
        await send_verification_prompt(interaction, self.flow_data)


class VerificationSelect(ui.Select):
    """Select verification type"""
    
    def __init__(self, flow_data: Dict):
        options = [
            discord.SelectOption(label=label, value=value)
            for value, label in VERIFICATION_TYPES
        ]
        super().__init__(placeholder="Select verification method...", options=options, custom_id="verification_select")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['verification_type'] = self.values[0]
        await interaction.response.defer()
        # Continue to final confirmation
        await send_confirmation(interaction, self.flow_data)


class UserSelect(ui.UserSelect):
    """Select opponent(s)"""
    
    def __init__(self, flow_data: Dict, multi: bool = False):
        self.flow_data = flow_data
        self.multi = multi
        super().__init__(
            placeholder="Select opponent(s)...",
            custom_id="opponent_select",
            min_values=1,
            max_values=1 if not multi else 25
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.multi:
            self.flow_data['opponents'] = [str(u.id) for u in self.values]
            self.flow_data['opponent_names'] = [u.display_name for u in self.values]
        else:
            self.flow_data['opponent_id'] = str(self.values[0].id)
            self.flow_data['opponent_name'] = self.values[0].display_name
        
        await interaction.response.defer()
        # Continue to bet type
        await send_bet_type_prompt(interaction, self.flow_data)


class BetTopicModal(ui.Modal):
    """Modal for bet topic and amount"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(title="Create Your Bet", timeout=300)
        self.flow_data = flow_data
        
        self.topic_input = ui.TextInput(
            label="Bet Topic",
            placeholder="What are you betting on?",
            style=discord.TextStyle.short,
            max_length=100,
            required=True
        )
        
        self.amount_input = ui.TextInput(
            label="Bet Amount",
            placeholder="Amount in Turd Coins",
            style=discord.TextStyle.short,
            max_length=10,
            required=True
        )
        
        self.description_input = ui.TextInput(
            label="Description (optional)",
            placeholder="More details about the bet",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=False
        )
        
        self.add_item(self.topic_input)
        self.add_item(self.amount_input)
        self.add_item(self.description_input)
    
    async def callback(self, interaction: discord.Interaction):
        try:
            logger.info(f"[BET_FLOW] Modal callback started for user {interaction.user.id}")
            
            self.flow_data['bet_topic'] = self.topic_input.value
            self.flow_data['amount'] = self.amount_input.value
            self.flow_data['description'] = self.description_input.value if self.description_input.value else None
            
            logger.info(f"[BET_FLOW] Topic: {self.flow_data['bet_topic']}, Amount: {self.flow_data['amount']}")
            
            # Validate amount
            try:
                amount = int(self.amount_input.value.replace(',', ''))
                if amount <= 0:
                    await interaction.response.send_message("❌ Amount must be positive!", ephemeral=True)
                    return
            except ValueError:
                await interaction.response.send_message("❌ Invalid amount! Please enter a number.", ephemeral=True)
                return
            
            logger.info(f"[BET_FLOW] Amount validated: {amount}")
            
            await interaction.response.defer()
            logger.info(f"[BET_FLOW] Deferred response, sending opponent prompt")
            
            # Continue to opponent selection
            await send_opponent_prompt(interaction, self.flow_data)
            logger.info(f"[BET_FLOW] Opponent prompt sent successfully")
            
        except Exception as e:
            logger.error(f"[BET_FLOW] Error in modal callback: {e}", exc_info=True)
            try:
                await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
            except:
                pass


class CustomOddsModal(ui.Modal):
    """Modal for custom odds input"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(title="Custom Odds", timeout=300)
        self.flow_data = flow_data
        
        self.odds_input = ui.TextInput(
            label="Odds (e.g., 2.5:1)",
            placeholder="Enter custom odds",
            style=discord.TextStyle.short,
            max_length=10,
            required=True
        )
        
        self.add_item(self.odds_input)
    
    async def callback(self, interaction: discord.Interaction):
        self.flow_data['custom_odds'] = self.odds_input.value
        await interaction.response.defer()
        await send_visibility_prompt(interaction, self.flow_data)


class ScheduledTimeModal(ui.Modal):
    """Modal for scheduled resolution time"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(title="Schedule Resolution", timeout=300)
        self.flow_data = flow_data
        
        self.time_input = ui.TextInput(
            label="Hours from now",
            placeholder="e.g., 24 for 24 hours",
            style=discord.TextStyle.short,
            max_length=5,
            required=True
        )
        
        self.add_item(self.time_input)
    
    async def callback(self, interaction: discord.Interaction):
        try:
            hours = int(self.time_input.value)
            if hours <= 0:
                await interaction.response.send_message("❌ Must be positive!", ephemeral=True)
                return
            self.flow_data['resolve_hours'] = hours
        except ValueError:
            await interaction.response.send_message("❌ Invalid number!", ephemeral=True)
            return
        
        await interaction.response.defer()
        await send_verification_prompt(interaction, self.flow_data)


# ============== SIMPLIFIED FLOW FUNCTIONS ==============

async def start_bet_flow(interaction: discord.Interaction, bot) -> None:
    """Start the bet creation flow with a simple modal"""
    logger.info(f"[BET_FLOW] start_bet_flow called by user {interaction.user.id}")
    
    user_id = str(interaction.user.id)
    
    # Initialize flow data
    flow_data = {
        'user_id': user_id,
        'username': interaction.user.name,
        'display_name': interaction.user.display_name,
        'bot': bot,
    }
    
    FLOW_STATE[user_id] = flow_data
    logger.info(f"[BET_FLOW] Flow state initialized for user {user_id}")
    
    # Use the simple bet modal (single modal with all options)
    modal = SimpleBetModal(flow_data)
    logger.info(f"[BET_FLOW] Sending simple modal to user")
    
    # Send modal directly (no defer)
    await interaction.response.send_modal(modal)
    logger.info(f"[BET_FLOW] Simple modal sent successfully")


class SimpleBetModal(ui.Modal):
    """Simple modal with all bet options at once"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(title="🎲 Create Your Bet", timeout=300)
        self.flow_data = flow_data
        
        # Topic
        self.topic_input = ui.TextInput(
            label="Bet Topic",
            placeholder="What are you betting on?",
            style=discord.TextStyle.short,
            max_length=100,
            required=True
        )
        
        # Amount
        self.amount_input = ui.TextInput(
            label="Bet Amount (Turd Coins)",
            placeholder="e.g., 100",
            style=discord.TextStyle.short,
            max_length=10,
            required=True
        )
        
        # Description
        self.description_input = ui.TextInput(
            label="Description (optional)",
            placeholder="More details about the bet",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=False
        )
        
        # Bet Type
        self.type_input = ui.TextInput(
            label="Bet Type",
            placeholder="1v1, 1vMany, or ManyvMany",
            style=discord.TextStyle.short,
            max_length=10,
            required=False
        )
        
        # Category
        self.category_input = ui.TextInput(
            label="Category",
            placeholder="Sports, Gaming, Real Life, or Random",
            style=discord.TextStyle.short,
            max_length=20,
            required=False
        )
        
        self.add_item(self.topic_input)
        self.add_item(self.amount_input)
        self.add_item(self.description_input)
        self.add_item(self.type_input)
        self.add_item(self.category_input)
    
    async def callback(self, interaction: discord.Interaction):
        logger.info(f"[BET_FLOW] Modal callback STARTED for user {interaction.user.id}")
        
        # First, just test if we can respond at all
        try:
            await interaction.response.send_message("✅ Modal received! Processing...", ephemeral=True)
            logger.info(f"[BET_FLOW] Initial response sent")
        except Exception as e:
            logger.error(f"[BET_FLOW] Error sending initial response: {e}")
            return
        
        # Store values
        self.flow_data['bet_topic'] = self.topic_input.value
        self.flow_data['amount'] = self.amount_input.value
        self.flow_data['description'] = self.description_input.value if self.description_input.value else None
        
        logger.info(f"[BET_FLOW] Topic: {self.flow_data['bet_topic']}, Amount: {self.flow_data['amount']}")
        
        # Validate amount
        try:
            amount = int(self.amount_input.value.replace(',', ''))
            if amount <= 0:
                await interaction.followup.send("❌ Amount must be positive!", ephemeral=True)
                return
        except ValueError:
            await interaction.followup.send("❌ Invalid amount! Please enter a number.", ephemeral=True)
            return
        
        # Try to create the bet
        try:
            bot = self.flow_data.get('bot')
            db = bot.db
            
            bet_id = f"BET-{uuid.uuid4().hex[:8].upper()}"
            logger.info(f"[BET_FLOW] Creating bet: {bet_id}")
            
            success = db.create_bet_advanced(
                bet_id=bet_id,
                creator_id=self.flow_data['user_id'],
                bet_topic=self.flow_data.get('bet_topic', 'No topic'),
                amount=amount,
                bet_description=self.flow_data.get('description'),
                bet_type='1v1',
                category='Random',
                odds='even',
                visibility='open',
                expiration='7d',
                verification_type='manual'
            )
            
            if not success:
                await interaction.followup.send("❌ Failed to create bet! Please try again.", ephemeral=True)
                return
            
            logger.info(f"[BET_FLOW] Bet created: {bet_id}")
            
            # Send success
            embed = discord.Embed(
                title="✅ Bet Created!",
                description=f"Your bet has been created!",
                color=0x2ECC71
            )
            embed.add_field(name="Bet ID", value=f"`{bet_id}`", inline=True)
            embed.add_field(name="Topic", value=self.flow_data.get('bet_topic', 'N/A'), inline=True)
            embed.add_field(name="Amount", value=f"{amount:,} TC", inline=True)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"[BET_FLOW] Error in modal callback: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}", ephemeral=True)


async def send_opponent_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send opponent selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    # Determine if we need single or multiple selection based on bet type
    bet_type = flow_data.get('bet_type', '1v1')
    multi = bet_type in ['1vMany', 'ManyvMany']
    
    embed = discord.Embed(
        title="🎯 Select Opponent(s)",
        description="Choose who you want to bet against:",
        color=0x9B59B6
    )
    embed.add_field(name="Step 2 of 6", value="Select opponent(s)", inline=False)
    
    view = View()
    view.add_item(UserSelect(flow_data, multi=multi))
    
    await thread.send(embed=embed, view=view)


async def send_bet_type_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send bet type selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    embed = discord.Embed(
        title="🎲 Select Bet Type",
        description="What kind of bet is this?",
        color=0x9B59B6
    )
    embed.add_field(name="Step 3 of 6", value="Select bet type", inline=False)
    
    view = View()
    view.add_item(BetTypeSelect(flow_data))
    
    await thread.send(embed=embed, view=view)


async def send_category_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send category selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    embed = discord.Embed(
        title="📂 Select Category",
        description="What category does this bet belong to?",
        color=0x9B59B6
    )
    embed.add_field(name="Step 4 of 6", value="Select category", inline=False)
    
    view = View()
    view.add_item(CategorySelect(flow_data))
    
    await thread.send(embed=embed, view=view)


async def send_odds_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send odds selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    embed = discord.Embed(
        title="💰 Select Payout Odds",
        description="What are the payout odds?",
        color=0x9B59B6
    )
    embed.add_field(name="Step 5 of 6", value="Select odds", inline=False)
    
    view = View()
    view.add_item(OddsSelect(flow_data))
    
    await thread.send(embed=embed, view=view)


async def send_visibility_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send visibility selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    # Check if custom odds
    if flow_data.get('odds') == 'custom':
        modal = CustomOddsModal(flow_data)
        await interaction.response.send_modal(modal)
        return
    
    embed = discord.Embed(
        title="🔒 Select Visibility",
        description="Who can join this bet?",
        color=0x9B59B6
    )
    embed.add_field(name="Step 6 of 6", value="Select visibility", inline=False)
    
    view = View()
    view.add_item(VisibilitySelect(flow_data))
    
    await thread.send(embed=embed, view=view)


async def send_expiration_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send expiration selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    embed = discord.Embed(
        title="⏰ Select Expiration",
        description="When should this bet expire if not accepted?",
        color=0x9B59B6
    )
    embed.add_field(name="Additional", value="Select expiration", inline=False)
    
    view = View()
    view.add_item(ExpirationSelect(flow_data))
    
    await thread.send(embed=embed, view=view)


async def send_verification_prompt(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send verification type selection prompt"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    # Check if scheduled
    if flow_data.get('expiration') == 'scheduled':
        modal = ScheduledTimeModal(flow_data)
        await interaction.response.send_modal(modal)
        return
    
    embed = discord.Embed(
        title="✅ Select Verification Method",
        description="How should the winner be verified?",
        color=0x9B59B6
    )
    embed.add_field(name="Verification", value="Select method", inline=False)
    
    view = View()
    view.add_item(VerificationSelect(flow_data))
    
    await thread.send(embed=embed, view=view)


async def send_confirmation(interaction: discord.Interaction, flow_data: Dict) -> None:
    """Send final confirmation"""
    thread = flow_data.get('thread')
    if not thread:
        return
    
    # Calculate expiration time
    exp = flow_data.get('expiration', '7d')
    if exp == '24h':
        exp_text = "24 hours"
    elif exp == '7d':
        exp_text = "7 days"
    else:
        exp_text = "Never"
    
    # Get opponent info
    if 'opponents' in flow_data:
        opponent_text = ", ".join(flow_data.get('opponent_names', []))
    else:
        opponent_text = flow_data.get('opponent_name', 'Not selected')
    
    # Build confirmation embed
    embed = discord.Embed(
        title="📋 Bet Summary",
        description="Please confirm your bet details:",
        color=0x9B59B6
    )
    embed.add_field(name="Topic", value=flow_data.get('bet_topic', 'N/A'), inline=True)
    embed.add_field(name="Amount", value=f"{flow_data.get('amount', 'N/A')} TC", inline=True)
    embed.add_field(name="Opponent", value=opponent_text, inline=True)
    embed.add_field(name="Bet Type", value=flow_data.get('bet_type', '1v1'), inline=True)
    embed.add_field(name="Category", value=flow_data.get('category', 'Random'), inline=True)
    embed.add_field(name="Odds", value=flow_data.get('odds', 'even'), inline=True)
    embed.add_field(name="Visibility", value=flow_data.get('visibility', 'open'), inline=True)
    embed.add_field(name="Expiration", value=exp_text, inline=True)
    embed.add_field(name="Verification", value=flow_data.get('verification_type', 'manual'), inline=True)
    
    if flow_data.get('description'):
        embed.add_field(name="Description", value=flow_data['description'], inline=False)
    
    # Add confirmation buttons
    view = View()
    view.add_item(ConfirmBetButton(flow_data))
    view.add_item(CancelFlowButton(flow_data))
    
    await thread.send(embed=embed, view=view)


class ConfirmBetButton(ui.Button):
    """Confirm and create the bet"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(label="✅ Confirm & Create", style=discord.ButtonStyle.success, custom_id="confirm_bet")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        # Create the bet
        bot = self.flow_data.get('bot')
        db = bot.db
        
        # Generate bet ID
        bet_id = f"BET-{uuid.uuid4().hex[:8].upper()}"
        
        # Parse amount
        try:
            amount = int(self.flow_data.get('amount', '0').replace(',', ''))
        except ValueError:
            await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
            return
        
        # Create bet in database
        success = db.create_bet_advanced(
            bet_id=bet_id,
            creator_id=self.flow_data['user_id'],
            bet_topic=self.flow_data.get('bet_topic', 'No topic'),
            amount=amount,
            bet_description=self.flow_data.get('description'),
            bet_type=self.flow_data.get('bet_type', '1v1'),
            category=self.flow_data.get('category', 'Random'),
            odds=self.flow_data.get('odds', 'even'),
            visibility=self.flow_data.get('visibility', 'open'),
            expiration=self.flow_data.get('expiration', '7d'),
            verification_type=self.flow_data.get('verification_type', 'manual')
        )
        
        if not success:
            await interaction.response.send_message("❌ Failed to create bet!", ephemeral=True)
            return
        
        # Add opponents as participants
        if 'opponents' in self.flow_data:
            for opp_id in self.flow_data['opponents']:
                db.add_bet_participant(bet_id, opp_id, 'B')
        elif 'opponent_id' in self.flow_data:
            db.add_bet_participant(bet_id, self.flow_data['opponent_id'], 'B')
        
        # Post to bets channel
        channel_manager = bot.channel_manager
        await post_bet_to_channel(
            bet_id=bet_id,
            bet_topic=self.flow_data.get('bet_topic', 'No topic'),
            amount=amount,
            creator_name=self.flow_data.get('display_name', 'Unknown'),
            channel_manager=channel_manager,
            bot=bot
        )
        
        # Send success message
        embed = discord.Embed(
            title="✅ Bet Created!",
            description=f"Your bet has been created with ID: `{bet_id}`",
            color=0x2ECC71
        )
        embed.add_field(name="Topic", value=self.flow_data.get('bet_topic', 'N/A'), inline=True)
        embed.add_field(name="Amount", value=f"{amount:,} TC", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Clean up flow state
        user_id = self.flow_data['user_id']
        if user_id in FLOW_STATE:
            del FLOW_STATE[user_id]


class CancelFlowButton(ui.Button):
    """Cancel the bet flow"""
    
    def __init__(self, flow_data: Dict):
        super().__init__(label="❌ Cancel", style=discord.ButtonStyle.danger, custom_id="cancel_flow")
        self.flow_data = flow_data
    
    async def callback(self, interaction: discord.Interaction):
        # Clean up flow state
        user_id = self.flow_data['user_id']
        if user_id in FLOW_STATE:
            del FLOW_STATE[user_id]
        
        embed = discord.Embed(
            title="❌ Bet Cancelled",
            description="Your bet creation has been cancelled.",
            color=0xE74C3C
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def post_bet_to_channel(bet_id: str, bet_topic: str, amount: int, creator_name: str, 
                             channel_manager, bot) -> None:
    """Post a bet to the #turd-bets channel"""
    from bet_threads import create_bet_thread_view
    
    bets_channel = channel_manager.get_bets_channel()
    
    if not bets_channel:
        logger.error("[BET_FLOW] Bets channel not available!")
        return
    
    embed = discord.Embed(
        title=f"🎲 New Bet: {bet_topic}",
        description=f"**Bet ID:** `{bet_id}`",
        color=0x9B59B6
    )
    embed.add_field(name="Amount", value=f"💰 **{amount:,}** Turd Coins", inline=True)
    embed.add_field(name="Creator", value=creator_name, inline=True)
    embed.add_field(name="Status", value="🔴 **OPEN** - Waiting for opponent!", inline=True)
    embed.set_footer(text="Use the Bet ID to join • Turd Casino")
    
    message = await bets_channel.send(embed=embed)
    
    # Create thread
    thread = await message.create_thread(
        name=f"🎲 {bet_topic[:50]}",
        auto_archive_duration=10080
    )
    
    # Send thread message with buttons
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
    
    view = create_bet_thread_view(bet_id, None)
    await thread.send(embed=thread_embed, view=view)
    
    logger.info(f"[BET_FLOW] Posted bet {bet_id} to #turd-bets with thread")


def get_flow_state(user_id: str) -> Optional[Dict]:
    """Get flow state for a user"""
    return FLOW_STATE.get(user_id)


def clear_flow_state(user_id: str) -> None:
    """Clear flow state for a user"""
    if user_id in FLOW_STATE:
        del FLOW_STATE[user_id]
