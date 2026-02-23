"""
Dashboard Views - Button handlers and interactions
"""

import discord
from discord import ui
from discord.ui import View
from config import DAILY_BONUS_AMOUNT, MIN_BET_AMOUNT, MAX_BET_AMOUNT
from bet_threads import post_bet_to_channel
from bet_flow import start_bet_flow


class DashboardView(ui.View):
    """Main dashboard buttons"""
    
    def __init__(self, bot, db, currency, bet_manager, dashboard_builder, channel_manager):
        super().__init__(timeout=None)
        self.bot = bot
        self.db = db
        self.currency = currency
        self.bet_manager = bet_manager
        self.dashboard_builder = dashboard_builder
        self.channel_manager = channel_manager
        
        # Add buttons
        self.add_item(CustomBetsButton())
        self.add_item(JoinBetButton())
        self.add_item(MyBetsButton())
        self.add_item(LeaderboardButton())
        self.add_item(DailyBonusButton())


class VerificationSelectView(View):
    """View to select verification method before creating a bet"""
    
    def __init__(self, dashboard_view):
        super().__init__(timeout=60)
        self.dashboard_view = dashboard_view
        
        # Add all verification options as buttons
        self.add_item(VerificationButton("manual", "🤝 Manual", "Participants agree on winner"))
        self.add_item(VerificationButton("vote", "🗳️ Vote", "Community votes on winner"))
        self.add_item(VerificationButton("link", "🔗 Link Proof", "Either party submits proof"))
        self.add_item(VerificationButton("ai", "🤖 AI Verification", "Bot scrapes URL to verify"))
        self.add_item(VerificationButton("scheduled", "⏰ Scheduled", "Bot pings at date for resolution"))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True


class VerificationButton(ui.Button):
    """Button to select verification method"""
    
    def __init__(self, value: str, label: str, description: str):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            custom_id=f"verify_{value}"
        )
        self.value = value
        self.description = description
    
    async def callback(self, interaction: discord.Interaction):
        print(f"[DEBUG] VerificationButton callback triggered for value: {self.value}")
        try:
            # Show the modal with the selected verification
            modal = CreateBetModal(self.view.dashboard_view, self.value)
            await interaction.response.send_modal(modal)
            print(f"[DEBUG] Modal sent successfully")
        except Exception as e:
            print(f"[DEBUG] VerificationButton ERROR: {e}")
            try:
                await interaction.followup.send("Error opening bet modal. Please try again.", ephemeral=True)
            except:
                pass


class CustomBetsButton(ui.Button):
    """Button to create custom bets - shows verification selection first"""
    
    def __init__(self):
        super().__init__(
            label="🎲 Custom Bets",
            style=discord.ButtonStyle.primary,
            custom_id="dashboard_custom_bets"
        )
    
    async def callback(self, interaction: discord.Interaction):
        print(f"[DEBUG] CustomBetsButton callback triggered for user {interaction.user.id}")
        
        try:
            # Ensure user exists
            user_id = str(interaction.user.id)
            username = interaction.user.name
            display_name = interaction.user.display_name
            
            self.view.db.ensure_user_exists(user_id, username, display_name)
            
            # Show verification selection view first
            view = VerificationSelectView(self.view)
            embed = discord.Embed(
                title="🎲 Create a Bet",
                description="Select a verification method:",
                color=0x9B59B6
            )
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            print(f"[DEBUG] Verification selection sent to user {interaction.user.id}")
        except Exception as e:
            print(f"[DEBUG] CustomBetsButton ERROR: {e}")
            import traceback
            traceback.print_exc()


class JoinBetButton(ui.Button):
    """Button to join an existing bet"""
    
    def __init__(self):
        super().__init__(
            label="🎯 Join Bet",
            style=discord.ButtonStyle.success,
            custom_id="dashboard_join_bet"
        )
    
    async def callback(self, interaction: discord.Interaction):
        try:
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
        except discord.errors.NotFound:
            pass  # Interaction expired - user clicked old button


class MyBetsButton(ui.Button):
    """Button to view user's bets"""
    
    def __init__(self):
        super().__init__(
            label="🎫 My Bets",
            style=discord.ButtonStyle.secondary,
            custom_id="dashboard_my_bets"
        )
    
    async def callback(self, interaction: discord.Interaction):
        try:
            user_id = str(interaction.user.id)
            
            embed = self.view.dashboard_builder.build_my_bets_embed(user_id)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.errors.NotFound:
            pass  # Interaction expired - user clicked old button


class LeaderboardButton(ui.Button):
    """Button to view leaderboard"""
    
    def __init__(self):
        super().__init__(
            label="🏆 Leaderboard",
            style=discord.ButtonStyle.secondary,
            custom_id="dashboard_leaderboard"
        )
    
    async def callback(self, interaction: discord.Interaction):
        try:
            embed = self.view.dashboard_builder.build_leaderboard_embed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.errors.NotFound:
            pass  # Interaction expired - user clicked old button


class DailyBonusButton(ui.Button):
    """Button to claim daily bonus"""
    
    def __init__(self):
        super().__init__(
            label="🎁 Daily Bonus",
            style=discord.ButtonStyle.success,
            custom_id="dashboard_daily_bonus"
        )
    
    async def callback(self, interaction: discord.Interaction):
        try:
            user_id = str(interaction.user.id)
            username = interaction.user.name
            display_name = interaction.user.display_name
            
            # Ensure user exists first
            self.view.db.ensure_user_exists(user_id, username, display_name)
            
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
        except discord.errors.NotFound:
            pass  # Interaction expired - user clicked old button


import traceback

class CreateBetModal(ui.Modal):
    """Modal to create a new bet"""
    
    def __init__(self, view, verification_type: str = "manual"):
        print(f"[DEBUG] CreateBetModal __init__ called with verification: {verification_type}")
        super().__init__(title="🎲 Create a Bet", timeout=300)
        self.view = view
        self.selected_verification = verification_type
        
        # Set title based on verification type
        verify_label = {
            "manual": "🤝 Manual",
            "vote": "🗳️ Vote",
            "link": "🔗 Link Proof",
            "ai": "🤖 AI Verification",
            "scheduled": "⏰ Scheduled"
        }.get(verification_type, "🤝 Manual")
        
        self.title = f"🎲 Create Bet - {verify_label}"
        
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
        
        # Add fields based on verification type
        self.verification_url_input = None
        self.verification_claim_input = None
        self.verification_date_input = None
        
        if verification_type == "ai":
            # AI verification needs URL and expected result
            self.verification_url_input = ui.TextInput(
                label="URL to Verify",
                placeholder="https://example.com (page to scrape)",
                style=discord.TextStyle.short,
                required=True,
                max_length=500
            )
            
            self.verification_claim_input = ui.TextInput(
                label="Expected Result",
                placeholder="e.g., > 100 or contains 'Winner'",
                style=discord.TextStyle.short,
                required=True,
                max_length=100
            )
        
        if verification_type == "scheduled":
            # Scheduled verification needs date/time
            self.verification_date_input = ui.TextInput(
                label="Verify At (YYYY-MM-DD HH:MM)",
                placeholder="2025-12-31 23:59",
                style=discord.TextStyle.short,
                required=True,
                max_length=16
            )
        
        # Always add base fields
        self.add_item(self.topic_input)
        self.add_item(self.amount_input)
        self.add_item(self.description_input)
        
        # Add verification-specific fields
        if self.verification_url_input:
            self.add_item(self.verification_url_input)
        if self.verification_claim_input:
            self.add_item(self.verification_claim_input)
        if self.verification_date_input:
            self.add_item(self.verification_date_input)
        
        print(f"[DEBUG] CreateBetModal __init__ complete")
    
    async def on_submit(self, interaction: discord.Interaction):
        print(f"[DEBUG] CreateBetModal on_submit called for user {interaction.user.id}")
        try:
            await self.callback(interaction)
        except Exception as e:
            print(f"[DEBUG] CreateBetModal on_submit EXCEPTION: {e}")
            traceback.print_exc()
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(f"[DEBUG] CreateBetModal on_error: {error}")
        traceback.print_exc()
    
    async def callback(self, interaction: discord.Interaction):
        print(f"[DEBUG] CreateBetModal callback triggered for user {interaction.user.id}")
        
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
        
        # Use the selected verification from the dropdown
        verification = self.selected_verification
        
        # Get verification-specific fields
        verification_url = None
        verification_claim = None
        verification_date = None
        
        if self.selected_verification == "ai":
            verification_url = self.verification_url_input.value if self.verification_url_input else None
            verification_claim = self.verification_claim_input.value if self.verification_claim_input else None
        
        if self.selected_verification == "scheduled":
            verification_date = self.verification_date_input.value if self.verification_date_input else None
        
        success, message, bet_id = self.view.bet_manager.create_bet(
            user_id, topic, amount, description, 
            verification_type=verification,
            verification_url=verification_url,
            verification_claim=verification_claim,
            verification_date=verification_date
        )
        
        if success:
            # Post bet to #turd-bets channel - use the guild from interaction
            bot = self.view.bot
            guild = interaction.guild
            guild_id = guild.id if guild else None
            
            print(f"[DEBUG] Creating bet in guild: {guild.name if guild else 'None'} (id: {guild_id})")
            
            try:
                await post_bet_to_channel(
                    bet_id, topic, amount, user_id, display_name,
                    self.view.channel_manager, bot, guild_id
                )
            except Exception as e:
                print(f"[DEBUG] Error posting bet to channel: {e}")
            
            embed = discord.Embed(
                title="✅ Bet Created!",
                description=message,
                color=0x2ECC71
            )
            
            # Get verification display
            verify_display = {
                "manual": "🤝 Manual",
                "vote": "🗳️ Vote",
                "link": "🔗 Link Proof",
                "ai": "🤖 AI Verification",
                "scheduled": "⏰ Scheduled"
            }.get(verification, verification.capitalize())
            
            embed.add_field(name="Topic", value=topic, inline=True)
            embed.add_field(name="Amount", value=f"{amount:,} TC", inline=True)
            embed.add_field(name="Bet ID", value=f"`{bet_id}`", inline=True)
            embed.add_field(name="Verification", value=verify_display, inline=True)
            
            # Add verification-specific info
            if verification == "ai" and verification_url:
                embed.add_field(name="🔗 URL", value=verification_url[:50] + "..." if len(verification_url) > 50 else verification_url, inline=True)
                embed.add_field(name="📋 Claim", value=verification_claim, inline=True)
            
            if verification == "scheduled" and verification_date:
                embed.add_field(name="📅 Verify At", value=verification_date, inline=True)
            
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
        print(f"[DEBUG] CreateBetModal callback completed for user {interaction.user.id}")


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


def setup_dashboard_view(bot, db, currency, bet_manager, dashboard_builder, channel_manager):
    """Set up and return the dashboard view"""
    global DASHBOARD_VIEW
    DASHBOARD_VIEW = DashboardView(bot, db, currency, bet_manager, dashboard_builder, channel_manager)
    return DASHBOARD_VIEW


class AdminBetResolveSelect(ui.Select):
    """Dropdown to select a bet to resolve"""
    
    def __init__(self, db, channel_manager):
        self.db = db
        self.channel_manager = channel_manager
        
        # Get pending bets
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''SELECT b.bet_id, b.bet_topic, b.amount, u.display_name, b.status
                    FROM bets b JOIN users u ON b.creator_id = u.user_id
                    WHERE b.status = 'pending' OR b.status = 'open'
                    ORDER BY b.created_at DESC LIMIT 25''')
        rows = c.fetchall()
        conn.close()
        
        options = []
        for row in rows:
            bet_id, topic, amount, creator, status = row
            options.append(discord.SelectOption(
                label=f"{topic[:40]} - {amount}TC",
                value=bet_id,
                description=f"Status: {status} | ID: {bet_id}"
            ))
        
        if not options:
            options.append(discord.SelectOption(label="No active bets", value="none"))
        
        super().__init__(placeholder="Select a bet to resolve...", options=options, custom_id="admin_bet_select")
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message("No active bets to resolve.", ephemeral=True)
            return
        
        bet_id = self.values[0]
        
        # Get bet details
        bet = self.db.get_bet(bet_id)
        if not bet:
            await interaction.response.send_message("Bet not found.", ephemeral=True)
            return
        
        participants = self.db.get_bet_participants(bet_id)
        
        # Build resolution embed
        embed = discord.Embed(
            title=f"🛡️ Resolve Bet: {bet['bet_topic']}",
            description=f"**Bet ID:** `{bet_id}`\n**Amount:** {bet['amount']:,} TC\n**Status:** {bet['status']}",
            color=0xF39C12
        )
        
        side_a = []
        side_b = []
        for p in participants:
            name = p['display_name'] or p['username']
            if p['side'] == 'A':
                side_a.append(name)
            else:
                side_b.append(name)
        
        embed.add_field(name="Side A", value=", ".join(side_a) if side_a else "None", inline=True)
        embed.add_field(name="Side B", value=", ".join(side_b) if side_b else "None", inline=True)
        
        view = AdminResolveView(self.db)
        view.add_item(ResolveBetButton(bet_id, "A"))
        view.add_item(ResolveBetButton(bet_id, "B"))
        
        # Add cancel/refund button for admins
        view.add_item(CancelBetButton(bet_id))
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class ResolveBetButton(ui.Button):
    """Button to resolve bet for a specific side"""
    
    def __init__(self, bet_id: str, side: str):
        label = "Side A Wins" if side == "A" else "Side B Wins"
        super().__init__(label=label, style=discord.ButtonStyle.success, custom_id=f"resolve_{bet_id}_{side}")
        self.bet_id = bet_id
        self.side = side
    
    async def callback(self, interaction: discord.Interaction):
        # Find the winner
        participants = self.view.db.get_bet_participants(self.bet_id)
        winner_id = None
        for p in participants:
            if p['side'] == self.side:
                winner_id = p['user_id']
                break
        
        if not winner_id:
            await interaction.response.send_message("No participant on that side!", ephemeral=True)
            return
        
        # Resolve
        success = self.view.db.resolve_bet(self.bet_id, winner_id)
        
        if success:
            await interaction.response.send_message(f"✅ Bet resolved! Winner: {winner_id}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to resolve bet.", ephemeral=True)


class CancelBetButton(ui.Button):
    """Button to cancel/refund a bet"""
    
    def __init__(self, bet_id: str):
        super().__init__(label="❌ Cancel & Refund", style=discord.ButtonStyle.danger, custom_id=f"cancel_{bet_id}")
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        # Cancel and refund
        success = self.view.db.cancel_bet(self.bet_id)
        
        if success:
            await interaction.response.send_message("✅ Bet cancelled and refunded!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to cancel bet.", ephemeral=True)


class AdminResolveView(View):
    """View for resolving bets - used after selecting a bet"""
    
    def __init__(self, db):
        super().__init__(timeout=None)
        self.db = db


class AdminBetResolveView(View):
    """Admin view for resolving bets"""
    
    def __init__(self, bot, db, channel_manager):
        super().__init__(timeout=None)
        self.bot = bot
        self.db = db
        self.channel_manager = channel_manager
        self.add_item(AdminBetResolveSelect(db, channel_manager))
