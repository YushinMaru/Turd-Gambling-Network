"""
Bet Thread Views - Win/Lose/Dispute buttons for bet threads
"""

import discord
from discord import ui
from discord.ui import View
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BetThreadView(View):
    """View with Win/Lose/Dispute buttons for bet threads"""
    
    def __init__(self, bet_id: str, creator_id: str, joiner_id: str = None, channel_manager = None):
        super().__init__(timeout=None)
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
    """Button to claim victory - implements dual confirmation"""
    
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
        
        print(f"[DEBUG] IWinButton - bet: {bet}")
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        print(f"[DEBUG] IWinButton - status: {bet.get('status')}")
        
        if bet.get('status') != 'pending':
            await interaction.response.send_message(
                f"❌ This bet is already {bet.get('status')}.", 
                ephemeral=True
            )
            return
        
        # Get participants to find the other user
        participants = db.get_bet_participants(self.bet_id)
        other_user_id = None
        other_user_side = None
        for p in participants:
            if p['user_id'] != user_id:
                other_user_id = p['user_id']
                other_user_side = p['side']
                break
        
        # Check if there's already a pending confirmation (first response)
        if bet.get('pending_confirmation') == 1 and bet.get('first_responder_id') == other_user_id:
            # The other user already claimed - this user is confirming
            # Resolve bet with this user as winner
            success, message = bet_manager.resolve_bet(self.bet_id, user_id)
            
            if success:
                await self._resolve_and_post(bot, db, self.bet_id, user_id, channel_manager)
                await interaction.response.send_message(f"✅ Bet resolved! You confirmed and won!", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
            return
        
        # First response - store it and ping the other user
        if other_user_id:
            # Store first response in database
            db.update_bet(self.bet_id, 
                         pending_confirmation=1, 
                         first_responder_id=user_id, 
                         first_response='win')
            
            # Get the other user
            other_user = await bot.fetch_user(other_user_id)
            
            # Send confirmation request to the other user in thread
            thread = interaction.channel
            confirm_embed = discord.Embed(
                title="⏰ Confirmation Required",
                description=f"**{interaction.user.display_name}** claims they won!\n\n{other_user.mention if other_user else 'The other participant'}, please confirm or dispute this claim.",
                color=0xF39C12
            )
            confirm_embed.add_field(name="Action Needed", value="Click ✅ to confirm you lost, or ⚠️ to dispute", inline=False)
            
            # Send to thread
            await thread.send(embed=confirm_embed)
            
            await interaction.response.send_message(
                f"⏰ Confirmation sent to the other participant! They must confirm or dispute your win claim.",
                ephemeral=True
            )
        else:
            # No other participant - resolve immediately
            success, message = bet_manager.resolve_bet(self.bet_id, user_id)
            
            if success:
                await self._resolve_and_post(bot, db, self.bet_id, user_id, channel_manager)
                await interaction.response.send_message("✅ Bet resolved! You win!", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
    
    async def _resolve_and_post(self, bot, db, bet_id, winner_id, channel_manager):
        """Helper to resolve bet and post to archive"""
        # Get full bet details including winner/loser info
        participants = db.get_bet_participants(bet_id)
        winner_user = await bot.fetch_user(winner_id)
        loser_user = None
        
        for p in participants:
            if p['user_id'] != winner_id:
                loser_user = await bot.fetch_user(p['user_id'])
                break
        
        # Get updated bet info
        bet = db.get_bet(bet_id)
        
        # Get winner/loser balance changes
        winner_new_balance = db.get_balance(winner_id)
        loser_new_balance = 0
        if loser_user:
            loser_new_balance = db.get_balance(loser_user.id)
        
        # Post detailed embed to archive
        if channel_manager:
            embed = discord.Embed(
                title=f"🏆 Bet Resolved - {bet_id}",
                description=f"✅ **Bet Complete!**",
                color=0x2ECC71
            )
            embed.add_field(name="📝 Topic", value=bet['bet_topic'], inline=False)
            embed.add_field(name="💰 Wager Amount", value=f"**{bet['amount']:,}** Turd Coins", inline=True)
            embed.add_field(name="👑 Winner", value=f"**{winner_user.display_name}**", inline=True)
            embed.add_field(name="😢 Loser", value=f"**{loser_user.display_name if loser_user else 'N/A'}**", inline=True)
            embed.add_field(name="💵 Winner New Balance", value=f"**{winner_new_balance:,}** TC", inline=True)
            if loser_user:
                embed.add_field(name="💸 Loser New Balance", value=f"**{loser_new_balance:,}** TC", inline=True)
            embed.add_field(name="⏰ Resolved At", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=True)
            embed.set_footer(text=f"Bet ID: {bet_id}")
            
            await channel_manager.post_to_archive(embed)


class ILoseButton(ui.Button):
    """Button to admit defeat - implements dual confirmation"""
    
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
        other_user_id = None
        for p in participants:
            if p['user_id'] != user_id:
                other_user_id = p['user_id']
                break
        
        if not other_user_id:
            await interaction.response.send_message(
                "❌ Can't resolve - need both parties.",
                ephemeral=True
            )
            return
        
        # Check if there's already a pending confirmation
        if bet.get('pending_confirmation') == 1 and bet.get('first_responder_id') == other_user_id:
            # The other user already claimed - this user is confirming they lost
            # Resolve bet with the other user as winner
            success, message = bet_manager.resolve_bet(self.bet_id, other_user_id)
            
            if success:
                # Get full bet details
                winner_user = await bot.fetch_user(other_user_id)
                loser_user = interaction.user
                
                bet = db.get_bet(self.bet_id)
                
                # Get balances
                winner_new_balance = db.get_balance(other_user_id)
                loser_new_balance = db.get_balance(user_id)
                
                # Post detailed embed to archive
                if channel_manager:
                    embed = discord.Embed(
                        title=f"🏆 Bet Resolved - {self.bet_id}",
                        description=f"✅ **Bet Complete!**",
                        color=0x2ECC71
                    )
                    embed.add_field(name="📝 Topic", value=bet['bet_topic'], inline=False)
                    embed.add_field(name="💰 Wager Amount", value=f"**{bet['amount']:,}** Turd Coins", inline=True)
                    embed.add_field(name="👑 Winner", value=f"**{winner_user.display_name}**", inline=True)
                    embed.add_field(name="😢 Loser", value=f"**{loser_user.display_name}**", inline=True)
                    embed.add_field(name="💵 Winner New Balance", value=f"**{winner_new_balance:,}** TC", inline=True)
                    embed.add_field(name="💸 Loser New Balance", value=f"**{loser_new_balance:,}** TC", inline=True)
                    embed.add_field(name="⏰ Resolved At", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=True)
                    embed.set_footer(text=f"Bet ID: {self.bet_id}")
                    
                    await channel_manager.post_to_archive(embed)
                
                # Update the thread
                embed = discord.Embed(
                    title=f"✅ Bet Resolved",
                    description=f"**Winner:** {winner_user.display_name if winner_user else 'Unknown'}",
                    color=0x2ECC71
                )
                
                await interaction.response.send_message("✅ Bet resolved! You confirmed your loss.", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
            return
        
        # First response - store it and ping the other user
        # Store first response in database
        db.update_bet(self.bet_id, 
                     pending_confirmation=1, 
                     first_responder_id=user_id, 
                     first_response='lose')
        
        # Get the other user
        other_user = await bot.fetch_user(other_user_id)
        
        # Send confirmation request to the other user in thread
        thread = interaction.channel
        confirm_embed = discord.Embed(
            title="⏰ Confirmation Required",
            description=f"**{interaction.user.display_name}** admits defeat!\n\n{other_user.mention if other_user else 'The other participant'}, please confirm this win.",
            color=0xF39C12
        )
        confirm_embed.add_field(name="Action Needed", value="Click ✅ to confirm you won", inline=False)
        
        # Send to thread
        await thread.send(embed=confirm_embed)
        
        await interaction.response.send_message(
            f"⏰ Confirmation sent to the other participant! They must confirm your loss claim.",
            ephemeral=True
        )


class SubmitProofButton(ui.Button):
    """Button to submit proof for link proof verification"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="📎 Submit Proof",
            style=discord.ButtonStyle.primary,
            custom_id=f"bet_proof_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        # Get the bet manager from the bot
        bot = interaction.client
        db = bot.db
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Check verification type
        if bet.get('verification_type') != 'link':
            await interaction.response.send_message(
                "❌ Proof submission is only available for Link Proof verification bets.",
                ephemeral=True
            )
            return
        
        # Show a modal to submit proof
        modal = SubmitProofModal(self.bet_id)
        await interaction.response.send_modal(modal)


class VoteButton(ui.Button):
    """Button to start a vote for community decision"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="🗳️ Start Vote",
            style=discord.ButtonStyle.primary,
            custom_id=f"bet_vote_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        
        # Get bot and db
        bot = interaction.client
        db = bot.db
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Check if this is a vote verification type
        if bet.get('verification_type') != 'vote':
            await interaction.response.send_message(
                "❌ Voting is only available for Vote verification bets.",
                ephemeral=True
            )
            return
        
        # Get participants
        participants = db.get_bet_participants(self.bet_id)
        
        if len(participants) < 2:
            await interaction.response.send_message(
                "❌ Need at least 2 participants to start a vote.",
                ephemeral=True
            )
            return
        
        # Build vote embed
        side_a_names = []
        side_b_names = []
        for p in participants:
            name = p['display_name'] or p['username']
            if p['side'] == 'A':
                side_a_names.append(name)
            else:
                side_b_names.append(name)
        
        embed = discord.Embed(
            title=f"🗳️ Vote: {bet['bet_topic']}",
            description="Vote for the winner! The majority decides.",
            color=0x9B59B6
        )
        embed.add_field(
            name="Side A", 
            value=", ".join(side_a_names) if side_a_names else "None", 
            inline=True
        )
        embed.add_field(
            name="Side B", 
            value=", ".join(side_b_names) if side_b_names else "None", 
            inline=True
        )
        embed.add_field(
            name="How to Vote",
            value="React with 🇦 for Side A or 🇧 for Side B",
            inline=False
        )
        embed.set_footer(text=f"Bet ID: {self.bet_id} • Vote ends in 24 hours")
        
        # Send vote message
        thread = interaction.channel
        vote_msg = await thread.send(embed=embed)
        
        # Add reactions
        await vote_msg.add_reaction("🇦")
        await vote_msg.add_reaction("🇧")
        
        await interaction.response.send_message(
            "✅ Vote started! Community can now vote.",
            ephemeral=True
        )


class SubmitProofModal(ui.Modal):
    """Modal to submit proof URL"""
    
    def __init__(self, bet_id: str):
        super().__init__(title="📎 Submit Proof", timeout=300)
        self.bet_id = bet_id
        
        self.proof_url_input = ui.TextInput(
            label="Proof URL",
            placeholder="https://example.com/proof (screenshot, score, etc)",
            style=discord.TextStyle.short,
            required=True,
            max_length=500
        )
        
        self.proof_description_input = ui.TextInput(
            label="Description (optional)",
            placeholder="What does this prove?",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=200
        )
        
        self.add_item(self.proof_url_input)
        self.add_item(self.proof_description_input)
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        proof_url = self.proof_url_input.value
        description = self.proof_description_input.value if self.proof_description_input.value else None
        
        # Get bot and db
        bot = interaction.client
        db = bot.db
        
        # Submit proof to database
        success = db.submit_proof(self.bet_id, user_id, proof_url, description)
        
        if success:
            # Post proof to thread
            thread = interaction.channel
            proof_embed = discord.Embed(
                title="📎 Proof Submitted",
                description=f"**{interaction.user.display_name}** submitted proof:",
                color=0x3498DB
            )
            proof_embed.add_field(name="🔗 URL", value=proof_url, inline=False)
            if description:
                proof_embed.add_field(name="📝 Description", value=description, inline=False)
            
            await thread.send(embed=proof_embed)
            
            await interaction.response.send_message("✅ Proof submitted successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to submit proof.", ephemeral=True)


class ResolveVoteButton(ui.Button):
    """Button to resolve a vote"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="🗳️ Resolve Vote",
            style=discord.ButtonStyle.success,
            custom_id=f"bet_resolve_vote_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        # Get bot and db
        bot = interaction.client
        db = bot.db
        
        # Get bet info
        bet = db.get_bet(self.bet_id)
        
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        # Get votes
        votes = db.get_bet_votes(self.bet_id)
        
        if not votes:
            await interaction.response.send_message("❌ No votes cast yet!", ephemeral=True)
            return
        
        # Get participants
        participants = db.get_bet_participants(self.bet_id)
        
        vote_a = votes.get('A', 0)
        vote_b = votes.get('B', 0)
        
        # Determine winner
        if vote_a > vote_b:
            winner_side = 'A'
            winner_id = participants[0]['user_id'] if participants else None
        elif vote_b > vote_a:
            winner_side = 'B'
            winner_id = participants[1]['user_id'] if len(participants) > 1 else None
        else:
            # Tie - creator wins
            winner_side = 'A'
            winner_id = participants[0]['user_id'] if participants else None
        
        if winner_id:
            # Resolve the bet
            bet_manager = bot.bet_manager
            success, message = bet_manager.resolve_bet(self.bet_id, winner_id)
            
            if success:
                await interaction.response.send_message(
                    f"✅ Vote resolved! Side {winner_side} wins with {max(vote_a, vote_b)} votes!",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Could not determine winner.", ephemeral=True)


class DisputeButton(ui.Button):
    """Button to file a dispute"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="⚠️ Dispute",
            style=discord.ButtonStyle.secondary,
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


class JoinBetButton(ui.Button):
    """Button to join this bet"""
    
    def __init__(self, bet_id: str):
        super().__init__(
            label="🎯 Join This Bet",
            style=discord.ButtonStyle.success,
            custom_id=f"bet_join_{bet_id}"
        )
        self.bet_id = bet_id
    
    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        username = interaction.user.name
        display_name = interaction.user.display_name
        
        # Get the bet manager from the bot
        bot = interaction.client
        db = bot.db
        bet_manager = bot.bet_manager
        
        # Ensure user exists first
        db.ensure_user_exists(user_id, username, display_name)
        
        # Check if user is the creator
        bet = db.get_bet(self.bet_id)
        if not bet:
            await interaction.response.send_message("❌ Bet not found.", ephemeral=True)
            return
        
        if bet['creator_id'] == user_id:
            await interaction.response.send_message("❌ You can't join your own bet!", ephemeral=True)
            return
        
        # Check if already joined
        participants = db.get_bet_participants(self.bet_id)
        for p in participants:
            if p['user_id'] == user_id:
                await interaction.response.send_message("❌ You've already joined this bet!", ephemeral=True)
                return
        
        # Try to join
        success = db.join_bet(self.bet_id, user_id)
        
        if success:
            # Get updated bet and participants
            bet = db.get_bet(self.bet_id)
            participants = db.get_bet_participants(self.bet_id)
            
            # Build participants text
            side_a = []
            side_b = []
            for p in participants:
                name = p['display_name'] or p['username']
                if p['side'] == 'A':
                    side_a.append(name)
                else:
                    side_b.append(name)
            
            # Update the original message in the thread
            embed = discord.Embed(
                title="🎲 New Bet: " + bet['bet_topic'],
                description=f"**Bet ID:** `{self.bet_id}`",
                color=0x9B59B6
            )
            embed.add_field(name="Amount", value=f"💰 **{bet['amount']:,}** Turd Coins", inline=True)
            embed.add_field(name="Status", value="🟡 **PENDING** - Both parties ready!", inline=True)
            embed.add_field(name="Side A (Creator)", value=", ".join(side_a) if side_a else "None", inline=True)
            embed.add_field(name="Side B (Opponent)", value=", ".join(side_b) if side_b else "None", inline=True)
            embed.set_footer(text="Use the Bet ID to join • Turd Casino")
            
            # Try to edit the message - we'll need to track the message somehow
            # For now, just send a new message in the thread
            await interaction.response.send_message("✅ You joined the bet! The thread has been updated.", ephemeral=True)
            
            # Send update to the thread
            thread = interaction.channel
            if thread and hasattr(thread, 'parent') or isinstance(thread, discord.Thread):
                await thread.send(embed=embed)
        else:
            await interaction.response.send_message("❌ Could not join bet. It may be closed.", ephemeral=True)


def create_bet_thread_view(bet_id: str, creator_id: str, joiner_id: str = None, show_join: bool = True, verification_type: str = 'manual') -> BetThreadView:
    """Create a view with buttons for a bet thread"""
    view = BetThreadView(bet_id, creator_id, joiner_id)
    
    # Add Join button if show_join is True (bet is open)
    if show_join:
        view.add_item(JoinBetButton(bet_id))
    
    # Add Submit Proof button for link proof verification
    if verification_type == 'link':
        view.add_item(SubmitProofButton(bet_id))
    
    # Add Vote button for vote verification
    if verification_type == 'vote':
        view.add_item(VoteButton(bet_id))
        view.add_item(ResolveVoteButton(bet_id))
    
    # Add resolution buttons
    view.add_item(IWinButton(bet_id))
    view.add_item(ILoseButton(bet_id))
    view.add_item(DisputeButton(bet_id))
    
    return view


async def post_bet_to_channel(bet_id: str, bet_topic: str, amount: int, creator_id: str, creator_name: str, 
                             channel_manager, bot, guild_id: int = None) -> discord.Message:
    """Post a bet to the #turd-bets channel with a thread"""
    
    bets_channel = channel_manager.get_bets_channel(guild_id)
    
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
    view = create_bet_thread_view(bet_id, creator_id, None, show_join=True)
    
    await thread.send(embed=thread_embed, view=view)
    
    logger.info(f"[BET_THREAD] Posted bet {bet_id} to #turd-bets with thread")
    
    return message
