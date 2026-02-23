"""
Bet Management - Edit, cancel, and manage bets
"""

import logging
import discord
from discord import ui
from discord.ui import View
from typing import Optional

logger = logging.getLogger(__name__)


class EditBetModal(ui.Modal):
    """Modal to edit bet details"""
    
    def __init__(self, bet_id: str, current_topic: str, current_amount: int, current_description: str = None):
        super().__init__(title="✏️ Edit Bet", timeout=300)
        self.bet_id = bet_id
        
        self.topic_input = ui.TextInput(
            label="Bet Topic",
            placeholder="What are you betting on?",
            style=discord.TextStyle.short,
            default_value=current_topic,
            max_length=100
        )
        
        self.amount_input = ui.TextInput(
            label="Bet Amount",
            placeholder="Amount in Turd Coins",
            style=discord.TextStyle.short,
            default_value=str(current_amount),
            max_length=10
        )
        
        self.description_input = ui.TextInput(
            label="Description (optional)",
            placeholder="More details about the bet",
            style=discord.TextStyle.paragraph,
            required=False,
            default_value=current_description or "",
            max_length=500
        )
        
        self.add_item(self.topic_input)
        self.add_item(self.amount_input)
        self.add_item(self.description_input)
    
    async def callback(self, interaction: discord.Interaction):
        # Get db from bot
        bot = interaction.client
        db = bot.db
        
        # Validate amount
        try:
            new_amount = int(self.amount_input.value.replace(',', ''))
        except ValueError:
            await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
            return
        
        # Update bet
        success = db.update_bet(
            self.bet_id,
            bet_topic=self.topic_input.value,
            amount=new_amount,
            bet_description=self.description_input.value if self.description_input.value else None
        )
        
        if success:
            await interaction.response.send_message(
                f"✅ Bet updated!\n\n**Topic:** {self.topic_input.value}\n**Amount:** {new_amount:,} TC",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("❌ Failed to update bet.", ephemeral=True)


class CancelBetModal(ui.Modal):
    """Modal to confirm bet cancellation"""
    
    def __init__(self, bet_id: str, amount: int):
        super().__init__(title="❌ Cancel Bet", timeout=300)
        self.bet_id = bet_id
        self.amount = amount
        self.fee = int(amount * 0.1)  # 10% cancellation fee
        
        self.confirm_input = ui.TextInput(
            label=f"Type 'cancel' to confirm (fee: {self.fee:,} TC)",
            placeholder="Type 'cancel' here",
            style=discord.TextStyle.short,
            max_length=10
        )
        self.add_item(self.confirm_input)
    
    async def callback(self, interaction: discord.Interaction):
        if self.confirm_input.value.lower() != 'cancel':
            await interaction.response.send_message("❌ Cancellation not confirmed.", ephemeral=True)
            return
        
        # Get db and bet manager
        bot = interaction.client
        db = bot.db
        
        # Cancel the bet
        success = db.cancel_bet(self.bet_id)
        
        if success:
            await interaction.response.send_message(
                f"✅ Bet cancelled! A {self.fee:,} TC cancellation fee has been applied.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("❌ Failed to cancel bet.", ephemeral=True)


class EditBetButton(ui.Button):
    """Button to edit a bet"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="✏️ Edit",
            style=discord.ButtonStyle.primary,
            custom_id=f"edit_bet_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        db = bot.db
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Check if user is creator
        if bet['creator_id'] != str(interaction.user.id):
            await interaction.response.send_message("❌ Only the bet creator can edit.", ephemeral=True)
            return
        
        # Check if bet is still open
        if bet['status'] != 'open':
            await interaction.response.send_message("❌ Can only edit open bets.", ephemeral=True)
            return
        
        # Show edit modal
        modal = EditBetModal(
            self.bet_id,
            bet['bet_topic'],
            bet['amount'],
            bet.get('bet_description')
        )
        await interaction.response.send_modal(modal)


class CancelBetButton(ui.Button):
    """Button to cancel a bet"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="❌ Cancel",
            style=discord.ButtonStyle.danger,
            custom_id=f"cancel_bet_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        db = bot.db
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Check if user is creator
        if bet['creator_id'] != str(interaction.user.id):
            await interaction.response.send_message("❌ Only the bet creator can cancel.", ephemeral=True)
            return
        
        # Check if bet is still open
        if bet['status'] != 'open':
            await interaction.response.send_message("❌ Can only cancel open bets.", ephemeral=True)
            return
        
        # Show cancel modal with fee
        fee = int(bet['amount'] * 0.1)
        modal = CancelBetModal(self.bet_id, bet['amount'])
        await interaction.response.send_modal(modal)


class BetManagementView(View):
    """View for managing a bet"""
    
    def __init__(self, bet_id: str, creator_id: str):
        super().__init__(timeout=None)
        self.bet_id = bet_id
        self.creator_id = creator_id
        
        self.add_item(EditBetButton(bet_id))
        self.add_item(CancelBetButton(bet_id))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == self.creator_id


# Bet tags functionality
class BetTagsView(View):
    """View for managing bet tags"""
    
    def __init__(self, bet_id: str):
        super().__init__(timeout=60)
        self.bet_id = bet_id
        
        # Add tag buttons
        self.add_item(TagButton(bet_id, "high-stakes", "💰"))
        self.add_item(TagButton(bet_id, "friendly", "😊"))
        self.add_item(TagButton(bet_id, "tournament", "🏆"))
        self.add_item(TagButton(bet_id, "practice", "🎯"))


class TagButton(ui.Button):
    """Button to add a tag"""
    
    def __init__(self, bet_id: str, tag: str, emoji: str):
        super().__init__(
            label=f"{emoji} {tag.replace('-', ' ').title()}",
            style=discord.ButtonStyle.secondary,
            custom_id=f"tag_{bet_id}_{tag}"
        )
        self.bet_id = bet_id
        self.tag = tag
    
    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        db = bot.db
        
        # Add tag
        success = db.add_bet_tag(self.bet_id, self.tag)
        
        if success:
            await interaction.response.send_message(
                f"✅ Added tag: {self.label}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to add tag.",
                ephemeral=True
            )


class BetReminderButton(ui.Button):
    """Button to set a reminder for a bet"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="⏰ Remind Me",
            style=discord.ButtonStyle.secondary,
            custom_id=f"remind_bet_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        db = bot.db
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Store reminder
        user_id = str(interaction.user.id)
        
        # TODO: Store reminder in database
        # For now, just acknowledge
        await interaction.response.send_message(
            f"⏰ Reminder set for bet: {bet['bet_topic']}",
            ephemeral=True
        )
