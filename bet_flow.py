"""
Bet Flow - Multi-step bet creation flow using threads
"""

import logging
import discord
from discord import ui
from discord.ui import View
from typing import Optional, List, Dict
from config import MIN_BET_AMOUNT, MAX_BET_AMOUNT

logger = logging.getLogger(__name__)


class BetFlowView(View):
    """View for multi-step bet creation"""
    
    def __init__(self, bot, db, bet_manager, channel_manager, creator_id: str):
        super().__init__(timeout=300)  # 5 minute timeout
        self.bot = bot
        self.db = db
        self.bet_manager = bet_manager
        self.channel_manager = channel_manager
        self.creator_id = creator_id
        
        # Flow state
        self.opponent_id: Optional[str] = None
        self.bet_type: str = "1v1"
        self.category: str = "Random"
        self.topic: str = ""
        self.amount: int = 0
        self.description: str = ""
        self.odds: str = "even"
        self.visibility: str = "open"
        self.expiration: str = "7d"
        self.verification_type: str = "manual"
        
        self.current_step: int = 0
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the creator to interact"""
        return str(interaction.user.id) == self.creator_id


class BetTypeSelect(ui.Select):
    """Select bet type"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="1v1", description="Head-to-head", emoji="⚔️"),
            discord.SelectOption(label="1vMany", description="You vs multiple opponents", emoji="👥"),
            discord.SelectOption(label="ManyvMany", description="Team vs team", emoji="🆚"),
        ]
        super().__init__(placeholder="Select bet type...", options=options, custom_id="bet_type_select")
    
    async def callback(self, interaction: discord.Interaction):
        # This will be handled by the parent view
        pass


class CategorySelect(ui.Select):
    """Select bet category"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="Sports", emoji="⚽"),
            discord.SelectOption(label="Gaming", emoji="🎮"),
            discord.SelectOption(label="Real Life", emoji="🌍"),
            discord.SelectOption(label="Random", emoji="🎲"),
        ]
        super().__init__(placeholder="Select category...", options=options, custom_id="category_select")
    
    async def callback(self, interaction: discord.Interaction):
        pass


class OddsSelect(ui.Select):
    """Select payout odds"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="Even (1:1)", value="even", emoji="⚖️"),
            discord.SelectOption(label="Double (2:1)", value="double", emoji="2️⃣"),
            discord.SelectOption(label="Triple (3:1)", value="triple", emoji="3️⃣"),
        ]
        super().__init__(placeholder="Select odds...", options=options, custom_id="odds_select")
    
    async def callback(self, interaction: discord.Interaction):
        pass


class VisibilitySelect(ui.Select):
    """Select visibility"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="Open", description="Anyone can join", value="open", emoji="🔓"),
            discord.SelectOption(label="Invite Only", description="Only invited users", value="invite", emoji="🔒"),
        ]
        super().__init__(placeholder="Select visibility...", options=options, custom_id="visibility_select")
    
    async def callback(self, interaction: discord.Interaction):
        pass


class ExpirationSelect(ui.Select):
    """Select expiration"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="24 Hours", value="24h", emoji="⏰"),
            discord.SelectOption(label="7 Days", value="7d", emoji="📅"),
            discord.SelectOption(label="Never", value="never", emoji="♾️"),
        ]
        super().__init__(placeholder="Select expiration...", options=options, custom_id="expiration_select")
    
    async def callback(self, interaction: discord.Interaction):
        pass


class UserSelectModal(ui.Modal):
    """Modal to search and select a user"""
    
    def __init__(self, view: BetFlowView):
        super().__init__(title="Select Opponent", timeout=300)
        self.view = view
        
        self.search_input = ui.TextInput(
            label="Search User",
            placeholder="Type username to search...",
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        self.add_item(self.search_input)
    
    async def callback(self, interaction: discord.Interaction):
        # Get guild members
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("This must be used in a server!", ephemeral=True)
            return
        
        # Search members
        query = self.search_input.value.lower()
        members = []
        
        async for member in guild.fetch_members(limit=100):
            if member.bot:
                continue
            if query in member.name.lower() or query in (member.display_name or "").lower():
                members.append(member)
        
        if not members:
            await interaction.response.send_message("No users found!", ephemeral=True)
            return
        
        # Show user selection
        options = []
        for member in members[:10]:  # Max 10
            options.append(discord.SelectOption(
                label=member.display_name,
                value=str(member.id),
                description=member.name
            ))
        
        select = UserSelectView(self.view, options)
        embed = discord.Embed(
            title="Select Opponent",
            description="Choose who you want to bet against:",
            color=0x9B59B6
        )
        await interaction.response.send_message(embed=embed, view=select, ephemeral=True)


class UserSelectView(View):
    """View for user selection"""
    
    def __init__(self, bet_flow_view: BetFlowView, options: List[discord.SelectOption]):
        super().__init__(timeout=60)
        self.bet_flow_view = bet_flow_view
        
        select = ui.Select(placeholder="Select opponent...", options=options, custom_id="opponent_select")
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        self.bet_flow_view.opponent_id = interaction.values[0]
        
        # Move to next step
        embed = discord.Embed(
            title="🎲 Bet Created!",
            description=f"Opponent selected: <@{self.bet_flow_view.opponent_id}>",
            color=0x2ECC71
        )
        await interaction.response.edit_message(embed=embed, view=None)


async def start_bet_flow(bot, db, bet_manager, channel_manager, creator_id: str, channel: discord.TextChannel):
    """Start the multi-step bet creation flow in a thread"""
    
    # Create a thread for the bet creation
    user = await bot.fetch_user(creator_id)
    
    # Send initial instructions
    embed = discord.Embed(
        title="🎲 Create a Custom Bet",
        description="Follow the steps to create your bet!\n\n"
                   "**Step 1:** Click the button below to select an opponent\n"
                   "**Step 2:** Choose your bet type\n"
                   "**Step 3:** Enter topic and amount\n"
                   "**Step 4:** Choose category and odds\n"
                   "**Step 5:** Confirm and create!",
        color=0x9B59B6
    )
    
    view = BetFlowStartView(bot, db, bet_manager, channel_manager, creator_id)
    
    msg = await channel.send(embed=embed, view=view)
    
    # Create a private thread
    thread = await msg.create_thread(
        name=f"🎲 Bet Setup — {user.display_name}",
        type=discord.ChannelType.private_thread,
        auto_archive_duration=60
    )
    
    # Add the creator to the thread
    await thread.add_user(user)
    
    # Send detailed instructions in thread
    thread_embed = discord.Embed(
        title="🎲 Bet Creation Wizard",
        description="Let's create your bet step by step!",
        color=0x9B59B6
    )
    thread_embed.add_field(
        name="Step 1: Select Opponent",
        value="Click the button below to search for and select your opponent.",
        inline=False
    )
    
    await thread.send(embed=thread_embed, view=view)
    
    return thread


class BetFlowStartView(View):
    """Starting view for bet flow"""
    
    def __init__(self, bot, db, bet_manager, channel_manager, creator_id: str):
        super().__init__(timeout=300)
        self.bot = bot
        self.db = db
        self.bet_manager = bet_manager
        self.channel_manager = channel_manager
        self.creator_id = creator_id
        
        # Add start button
        self.add_item(StartBetFlowButton())
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == self.creator_id


class StartBetFlowButton(ui.Button):
    """Button to start bet flow"""
    
    def __init__(self):
        super().__init__(
            label="🎯 Select Opponent",
            style=discord.ButtonStyle.primary,
            custom_id="start_bet_flow"
        )
    
    async def callback(self, interaction: discord.Interaction):
        # Show user search modal
        modal = UserSearchModal()
        await interaction.response.send_modal(modal)


class UserSearchModal(ui.Modal):
    """Modal to search for opponent"""
    
    def __init__(self):
        super().__init__(title="Search for Opponent", timeout=300)
        
        self.search_input = ui.TextInput(
            label="Username",
            placeholder="Type username to search...",
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        self.add_item(self.search_input)
    
    async def callback(self, interaction: discord.Interaction):
        # This would need the full flow context
        # For now, show a placeholder
        await interaction.response.send_message(
            "🔍 Searching for users... (Full flow coming soon!)",
            ephemeral=True
        )


class BetDetailsModal(ui.Modal):
    """Modal for bet topic and amount"""
    
    def __init__(self):
        super().__init__(title="Bet Details", timeout=300)
        
        self.topic_input = ui.TextInput(
            label="Bet Topic",
            placeholder="What are you betting on?",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        
        self.amount_input = ui.TextInput(
            label="Amount",
            placeholder=f"{MIN_BET_AMOUNT} - {MAX_BET_AMOUNT}",
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        
        self.description_input = ui.TextInput(
            label="Description (optional)",
            placeholder="More details...",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=500
        )
        
        self.add_item(self.topic_input)
        self.add_item(self.amount_input)
        self.add_item(self.description_input)
    
    async def callback(self, interaction: discord.Interaction):
        # Validate amount
        try:
            amount = int(self.amount_input.value.replace(',', ''))
        except ValueError:
            await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
            return
        
        if amount < MIN_BET_AMOUNT or amount > MAX_BET_AMOUNT:
            await interaction.response.send_message(
                f"❌ Amount must be between {MIN_BET_AMOUNT:,} and {MAX_BET_AMOUNT:,}!",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            f"✅ Topic: {self.topic_input.value}\n💰 Amount: {amount:,} TC",
            ephemeral=True
        )


# Simple bet creation modal for quick use
class QuickBetModal(ui.Modal):
    """Quick bet creation modal"""
    
    def __init__(self, view):
        super().__init__(title="🎲 Create a Bet", timeout=300)
        self.view = view
        
        self.topic_input = ui.TextInput(
            label="Bet Topic",
            placeholder="What are you betting on?",
            style=discord.TextStyle.short,
            max_length=100
        )
        
        self.amount_input = ui.TextInput(
            label="Bet Amount",
            placeholder=f"{MIN_BET_AMOUNT} - {MAX_BET_AMOUNT}",
            style=discord.TextStyle.short,
            max_length=10
        )
        
        self.description_input = ui.TextInput(
            label="Description (optional)",
            placeholder="More details about the bet",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=500
        )
        
        self.add_item(self.topic_input)
        self.add_item(self.amount_input)
        self.add_item(self.description_input)
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        username = interaction.user.name
        display_name = interaction.user.display_name
        
        # Ensure user exists
        self.view.db.ensure_user_exists(user_id, username, display_name)
        
        # Validate amount
        try:
            amount = int(self.amount_input.value.replace(',', ''))
        except ValueError:
            await interaction.response.send_message("❌ Invalid amount. Please enter a number.", ephemeral=True)
            return
        
        # Create bet
        topic = self.topic_input.value
        description = self.description_input.value if self.description_input.value else None
        
        success, message, bet_id = self.view.bet_manager.create_bet(
            user_id, topic, amount, description
        )
        
        if success:
            # Post to channel
            from bet_threads import post_bet_to_channel
            
            bot = self.view.bot
            guild = interaction.guild
            guild_id = guild.id if guild else None
            
            try:
                await post_bet_to_channel(
                    bet_id, topic, amount, user_id, display_name,
                    self.view.channel_manager, bot, guild_id
                )
            except Exception as e:
                print(f"[DEBUG] Error posting bet: {e}")
            
            embed = discord.Embed(
                title="✅ Bet Created!",
                description=message,
                color=0x2ECC71
            )
            embed.add_field(name="Topic", value=topic, inline=True)
            embed.add_field(name="Amount", value=f"{amount:,} TC", inline=True)
            embed.add_field(name="Bet ID", value=f"`{bet_id}`", inline=True)
        else:
            embed = discord.Embed(
                title="❌ Bet Creation Failed",
                description=message,
                color=0xE74C3C
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
