"""
Bet System Core - Bet creation, joining, and resolution
"""

import logging
import uuid
from datetime import datetime
from typing import Optional, List, Dict
from database import DatabaseManager
from currency import CurrencyManager

logger = logging.getLogger(__name__)


class BetManager:
    """Manages bet operations"""
    
    def __init__(self, db: DatabaseManager, currency: CurrencyManager):
        self.db = db
        self.currency = currency
    
    def generate_bet_id(self) -> str:
        """Generate unique bet ID"""
        return f"BET-{uuid.uuid4().hex[:8].upper()}"
    
    def create_bet(self, creator_id: str, bet_topic: str, amount: int, bet_description: str = None, 
                   verification_type: str = 'manual', verification_url: str = None, verification_claim: str = None,
                   verification_date: str = None) -> tuple[bool, str, Optional[str]]:
        """Create a new bet"""
        # Validate amount
        valid, message = self.currency.validate_bet_amount(amount)
        if not valid:
            return False, message, None
        
        # Check if creator can afford
        if not self.currency.can_afford(creator_id, amount):
            balance = self.currency.get_balance(creator_id)
            return False, f"Insufficient balance. You have {balance:,} Turd Coins.", None
        
        # Generate bet ID
        bet_id = self.generate_bet_id()
        
        # Create bet
        success = self.db.create_bet(
            bet_id, creator_id, bet_topic, amount, bet_description, 
            verification_type=verification_type,
            verification_url=verification_url,
            verification_claim=verification_claim,
            verification_date=verification_date
        )
        
        if success:
            logger.info(f"Bet created: {bet_id} by {creator_id} for {amount} (verification: {verification_type})")
            return True, f"✅ Bet created! Bet ID: `{bet_id}`", bet_id
        else:
            return False, "❌ Failed to create bet. Please try again.", None
    
    def join_bet(self, bet_id: str, user_id: str) -> tuple[bool, str]:
        """Join an existing bet"""
        # Get bet info
        bet = self.db.get_bet(bet_id)
        
        if not bet:
            return False, "❌ Bet not found."
        
        if bet['status'] != 'open':
            return False, "❌ This bet is no longer open."
        
        # Check if user is the creator
        if bet['creator_id'] == user_id:
            return False, "❌ You cannot join your own bet."
        
        # Check balance
        amount = bet['amount']
        if not self.currency.can_afford(user_id, amount):
            balance = self.currency.get_balance(user_id)
            return False, f"Insufficient balance. You have {balance:,} Turd Coins. Need {amount:,}."
        
        # Join bet
        success = self.db.join_bet(bet_id, user_id)
        
        if success:
            logger.info(f"User {user_id} joined bet {bet_id}")
            return True, f"✅ You joined the bet! Good luck!"
        else:
            return False, "❌ Failed to join bet. You may have already joined."
    
    def resolve_bet(self, bet_id: str, winner_id: str) -> tuple[bool, str]:
        """Resolve a bet and declare winner"""
        bet = self.db.get_bet(bet_id)
        
        if not bet:
            return False, "❌ Bet not found."
        
        if bet['status'] != 'pending':
            return False, "❌ This bet cannot be resolved. It's not pending."
        
        # Verify winner is a participant
        participants = self.db.get_bet_participants(bet_id)
        winner_ids = [p['user_id'] for p in participants]
        
        if winner_id not in winner_ids:
            return False, "❌ Winner must be a participant in this bet."
        
        # Resolve bet
        success = self.db.resolve_bet(bet_id, winner_id)
        
        if success:
            logger.info(f"Bet {bet_id} resolved. Winner: {winner_id}")
            return True, f"✅ Bet resolved! Congratulations to the winner!"
        else:
            return False, "❌ Failed to resolve bet."
    
    def cancel_bet(self, bet_id: str, user_id: str) -> tuple[bool, str]:
        """Cancel an open bet"""
        bet = self.db.get_bet(bet_id)
        
        if not bet:
            return False, "❌ Bet not found."
        
        if bet['status'] != 'open':
            return False, "❌ This bet cannot be cancelled. It's no longer open."
        
        if bet['creator_id'] != user_id:
            return False, "❌ Only the bet creator can cancel."
        
        success = self.db.cancel_bet(bet_id)
        
        if success:
            logger.info(f"Bet {bet_id} cancelled by {user_id}")
            return True, "✅ Bet cancelled. All participants have been refunded."
        else:
            return False, "❌ Failed to cancel bet."
    
    def get_bet_info(self, bet_id: str) -> Optional[Dict]:
        """Get full bet info with participants"""
        bet = self.db.get_bet(bet_id)
        
        if not bet:
            return None
        
        participants = self.db.get_bet_participants(bet_id)
        
        return {
            'bet': bet,
            'participants': participants
        }
    
    def format_bet_embed(self, bet_id: str) -> str:
        """Format bet info for display"""
        info = self.get_bet_info(bet_id)
        
        if not info:
            return "Bet not found."
        
        bet = info['bet']
        participants = info['participants']
        
        lines = [
            f"**Bet ID:** `{bet['bet_id']}`",
            f"**Topic:** {bet['bet_topic']}",
            f"**Amount:** 💰 **{bet['amount']:,}** Turd Coins",
            f"**Status:** {bet['status'].upper()}",
        ]
        
        if bet['bet_description']:
            lines.append(f"**Description:** {bet['bet_description']}")
        
        if participants:
            lines.append("\n**Participants:**")
            for p in participants:
                side = "Side A" if p['side'] == 'A' else "Side B"
                name = p['display_name'] or p['username']
                lines.append(f"  • {name} ({side})")
        
        return "\n".join(lines)
    
    def get_open_bets_list(self) -> List[Dict]:
        """Get list of open bets"""
        return self.db.get_open_bets()
    
    def get_user_bets(self, user_id: str) -> List[Dict]:
        """Get all bets for a user"""
        return self.db.get_user_bets(user_id)
