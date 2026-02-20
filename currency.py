"""
Turd Coins Economy - Balance management and daily bonuses
"""

import logging
from datetime import datetime
from typing import Optional
from database import DatabaseManager
from config import STARTING_BALANCE, DAILY_BONUS_AMOUNT, MIN_BET_AMOUNT, MAX_BET_AMOUNT

logger = logging.getLogger(__name__)


class CurrencyManager:
    """Manages Turd Coins economy"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_balance(self, user_id: str) -> int:
        """Get user's current balance"""
        return self.db.get_balance(user_id)
    
    def can_afford(self, user_id: str, amount: int) -> bool:
        """Check if user can afford a bet"""
        if amount < MIN_BET_AMOUNT:
            return False
        if amount > MAX_BET_AMOUNT:
            return False
        return self.get_balance(user_id) >= amount
    
    def validate_bet_amount(self, amount: int) -> tuple[bool, str]:
        """Validate a bet amount"""
        if amount < MIN_BET_AMOUNT:
            return False, f"Minimum bet is {MIN_BET_AMOUNT} Turd Coins"
        if amount > MAX_BET_AMOUNT:
            return False, f"Maximum bet is {MAX_BET_AMOUNT} Turd Coins"
        return True, "Valid"
    
    def claim_daily_bonus(self, user_id: str) -> tuple[bool, str]:
        """Claim daily bonus"""
        success = self.db.claim_daily_bonus(user_id, DAILY_BONUS_AMOUNT)
        
        if success:
            logger.info(f"User {user_id} claimed daily bonus of {DAILY_BONUS_AMOUNT}")
            return True, f"✅ You claimed **{DAILY_BONUS_AMOUNT}** Turd Coins!"
        else:
            return False, "❌ You already claimed your daily bonus today! Come back tomorrow."
    
    def format_balance(self, balance: int) -> str:
        """Format balance for display"""
        return f"💰 **{balance:,}** Turd Coins"
    
    def get_user_stats(self, user_id: str) -> Optional[dict]:
        """Get user's gambling statistics"""
        user = self.db.get_user(user_id)
        if not user:
            return None
        
        bets_won = user['bets_won']
        bets_lost = user['bets_lost']
        total_bets = bets_won + bets_lost
        win_rate = (bets_won / total_bets * 100) if total_bets > 0 else 0
        
        return {
            'balance': user['balance'],
            'total_won': user['total_won'],
            'total_lost': user['total_lost'],
            'bets_won': bets_won,
            'bets_lost': bets_lost,
            'total_bets': total_bets,
            'win_rate': win_rate
        }
    
    def format_stats(self, user_id: str) -> str:
        """Format user stats for display"""
        stats = self.get_user_stats(user_id)
        
        if not stats:
            return "No statistics available."
        
        lines = [
            f"💰 Balance: **{stats['balance']:,}** Turd Coins",
            f"📊 Total Bets: **{stats['total_bets']}**",
            f"✅ Wins: **{stats['bets_won']}** | ❌ Losses: **{stats['bets_lost']}**",
            f"📈 Win Rate: **{stats['win_rate']:.1f}%**",
            f"💎 Total Won: **{stats['total_won']:,}** | 💸 Total Lost: **{stats['total_lost']:,}**"
        ]
        
        return "\n".join(lines)
