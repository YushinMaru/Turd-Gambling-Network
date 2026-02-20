"""
Dashboard Views - Button handlers and interactions
"""

import discord
from discord import ui
from config import DAILY_BONUS_AMOUNT, MIN_BET_AMOUNT, MAX_BET_AMOUNT


class DashboardView(ui.View):
    """Main dashboard buttons"""
    
    def __init__(self, bot, db, currency, bet_manager, dashboard_builder):
        super().__init__(timeout=None, persistent=True)
        self.bot = bot
        self.db = db
        self.currency = currency
        self.bet_manager = bet_manager
        self.dashboard_builder = dashboard_builder
        
        # Add buttons
        self.add_item(CreateBetButton())
        self.add_item(JoinBetButton())
        self.add_item(MyBetsButton())
        self.add_item(LeaderboardButton())
        self.add_item(DailyBonusButton())


class CreateBetButton(ui.Button):
    """Button to create a new bet"""
    
    def __init__(self):
        super().__init__(
            label="🎲 Create Bet",
            style=discord.ButtonStyle.primary,
            custom_id="dashboard_create_bet"
        )
    
    async def callback(self, interaction: discord.Interaction):
        # Ensure user exists
        user_id = str(interaction.user.id)
        username = interaction.user.name
        display_name = interaction.user.display_name
        
        self.view.db.ensure_user_exists(user_id, username, display_name)
        
        # Create thread for bet creation flow
        thread_name = f"🎲 Bet Setup — {interaction.user.display_name}"
        
        try:
            # Try to create a private thread
            thread = await interaction.message.create_thread(
                name=thread_name,
                type=discord.ChannelType.private_thread,
                auto_archive_duration=60
            )
            
            embed = discord.Embed(
                title="🎲 Create a New Bet",
                description="Let's set up your bet! First, what is the bet topic?",
                color=0x9B59B6
            )
            embed.add_field(name="Instructions", value="Reply with the bet topic (e.g., 'Who will win the game?')", inline=False)
            
            await thread.send(embed=embed, content=interaction.user.mention)
            await interaction.response.send_message("✅ Check your thread to create your bet!", ephemeral=True)
            
        except Exception as e:
            # Fallback to modal
            await interaction.response.send_modal(CreateBetModal(self.view))


class JoinBetButton(ui.Button):
    """Button to join an existing bet"""
    
    def __init__(self):
        super().__init__(
            label="🎯 Join Bet",
            style=discord.ButtonStyle.success,
            custom_id="dashboard_join_bet"
        )
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        username = interaction.user.name
        display_name = interaction.user.display_name
        
        self.view.db.ensure_user_exists(user_id, username, display_name)
        
        # Show open bets
        embed = discord.Embed(
            title="🎯 Join a Bet",
            description="Here are the open bets you can join:",
            color=0x9B59B6
        )
        
        open_bets = self.view.bet_manager.get_open_bets_list()
        
        if not open_bets:
            embed.description = "No open bets right now. Create one!"
        else:
            for bet in open_bets[:10]:
                creator = bet['creator_display'] or bet['creator_username']
                embed.add_field(
                    name=f"📋 {bet['bet_topic']}",
                    value=f"ID: `{bet['bet_id']}`\nAmount: {bet['amount']:,} TC\nBy: {creator}",
                    inline=True
                )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class MyBetsButton(ui.Button):
    """Button to view user's bets"""
    
    def __init__(self):
        super().__init__(
            label="🎫 My Bets",
            style=discord.ButtonStyle.secondary,
            custom_id="dashboard_my_bets"
        )
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        embed = self.view.dashboard_builder.build_my_bets_embed(user_id)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class LeaderboardButton(ui.Button):
    """Button to view leaderboard"""
    
    def __init__(self):
        super().__init__(
            label="🏆 Leaderboard",
            style=discord.ButtonStyle.secondary,
            custom_id="dashboard_leaderboard"
        )
    
    async def callback(self, interaction: discord.Interaction):
        embed = self.view.dashboard_builder.build_leaderboard_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)


class DailyBonusButton(ui.Button):
    """Button to claim daily bonus"""
    
    def __init__(self):
        super().__init__(
            label="🎁 Daily Bonus",
            style=discord.ButtonStyle.success,
            custom_id="dashboard_daily_bonus"
        )
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        success, message = self.view.currency.claim_daily_bonus(user_id)
        
        embed = discord.Embed(
            title="🎁 Daily Bonus",
            description=message,
            color=0x2ECC71 if success else 0xE74C3C
        )
        
        if success:
            balance = self.view.currency.get_balance(user_id)
            embed.add_field(name="New Balance", value=f"💰 **{balance:,}** Turd Coins", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class CreateBetModal(ui.Modal):
    """Modal to create a new bet"""
    
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
        
        success, message, bet_id = self.view.bet_manager.create_bet(user_id, topic, amount, description)
        
        if success:
            embed = discord.Embed(
                title="✅ Bet Created!",
                description=message,
                color=0x2ECC71
            )
            
            embed.add_field(name="Topic", value=topic, inline=True)
            embed.add_field(name="Amount", value=f"{amount:,} TC", inline=True)
            embed.add_field(name="Bet ID", value=f"`{bet_id}`", inline=True)
            
            if description:
                embed.add_field(name="Description", value=description, inline=False)
            
            embed.add_field(
                name="What's Next?",
                value="Share the Bet ID with your opponent so they can join!",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Bet Creation Failed",
                description=message,
                color=0xE74C3C
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class JoinBetModal(ui.Modal):
    """Modal to join a bet"""
    
    def __init__(self, view):
        super().__init__(title="🎯 Join a Bet", timeout=300)
        self.view = view
        
        self.bet_id_input = ui.TextInput(
            label="Bet ID",
            placeholder="Enter the Bet ID (e.g., BET-ABC12345)",
            style=discord.TextStyle.short,
            max_length=20
        )
        
        self.add_item(self.bet_id_input)
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        bet_id = self.bet_id_input.value.strip().upper()
        
        success, message = self.view.bet_manager.join_bet(bet_id, user_id)
        
        if success:
            embed = discord.Embed(
                title="✅ Joined!",
                description=message,
                color=0x2ECC71
            )
        else:
            embed = discord.Embed(
                title="❌ Failed",
                description=message,
                color=0xE74C3C
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


# Store references for persistent views
DASHBOARD_VIEW = None


def setup_dashboard_view(bot, db, currency, bet_manager, dashboard_builder):
    """Set up and return the dashboard view"""
    global DASHBOARD_VIEW
    DASHBOARD_VIEW = DashboardView(bot, db, currency, bet_manager, dashboard_builder)
    return DASHBOARD_VIEW
