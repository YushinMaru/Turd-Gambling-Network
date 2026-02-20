"""
Database operations and queries for Turd Gambling Network
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Dict
from config import DB_PATH, STARTING_BALANCE
from database_init import DatabaseInitializer

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.initializer = DatabaseInitializer(db_path)
        self.initializer.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with timeout to prevent locking"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn
    
    # ============== USER OPERATIONS ==============
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'user_id': row[0], 'username': row[1], 'display_name': row[2],
                'balance': row[3], 'total_won': row[4], 'total_lost': row[5],
                'bets_won': row[6], 'bets_lost': row[7],
                'daily_bonus_claimed': row[8], 'created_at': row[9], 'last_active': row[10]
            }
        return None
    
    def ensure_user_exists(self, user_id: str, username: str, display_name: str = None):
        """Ensure user exists in database, create if not"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not c.fetchone():
            c.execute('''INSERT INTO users (user_id, username, display_name, balance)
                        VALUES (?, ?, ?, ?)''', (user_id, username, display_name, STARTING_BALANCE))
            conn.commit()
            logger.info(f"Created new user: {username} ({user_id})")
        
        c.execute("UPDATE users SET last_active = ? WHERE user_id = ?", (datetime.now().isoformat(), user_id))
        conn.commit()
        conn.close()
    
    def get_balance(self, user_id: str) -> int:
        """Get user's balance"""
        user = self.get_user(user_id)
        return user['balance'] if user else 0
    
    def update_balance(self, user_id: str, amount: int, transaction_type: str, bet_id: str = None, description: str = None):
        """Update user balance and log transaction"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
            
            c.execute('''INSERT INTO transactions (user_id, amount, transaction_type, bet_id, description)
                        VALUES (?, ?, ?, ?, ?)''',
                     (user_id, amount, transaction_type, bet_id, description))
            
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating balance: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def claim_daily_bonus(self, user_id: str, amount: int) -> bool:
        """Claim daily bonus if available"""
        conn = self.get_connection()
        c = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        c.execute("SELECT daily_bonus_claimed FROM users WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        
        if row and row[0] and row[0].startswith(today):
            conn.close()
            return False  # Already claimed today
        
        c.execute("UPDATE users SET balance = balance + ?, daily_bonus_claimed = ? WHERE user_id = ?",
                  (amount, datetime.now().isoformat(), user_id))
        
        c.execute('''INSERT INTO daily_bonus_log (user_id, amount) VALUES (?, ?)''', (user_id, amount))
        
        conn.commit()
        conn.close()
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by balance"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT user_id, username, display_name, balance, bets_won, bets_lost
                    FROM users ORDER BY balance DESC LIMIT ?''', (limit,))
        
        results = []
        for row in c.fetchall():
            results.append({
                'user_id': row[0], 'username': row[1], 'display_name': row[2],
                'balance': row[3], 'bets_won': row[4], 'bets_lost': row[5]
            })
        
        conn.close()
        return results
    
    # ============== BET OPERATIONS ==============
    
    def create_bet(self, bet_id: str, creator_id: str, bet_topic: str, amount: int, bet_description: str = None) -> bool:
        """Create a new bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO bets (bet_id, creator_id, bet_topic, bet_description, amount)
                        VALUES (?, ?, ?, ?, ?)''',
                     (bet_id, creator_id, bet_topic, bet_description, amount))
            
            # Add creator as participant (side A)
            c.execute('''INSERT INTO bet_participants (bet_id, user_id, side)
                        VALUES (?, ?, 'A')''', (bet_id, creator_id))
            
            # Deduct from creator's balance
            c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, creator_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creating bet: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def join_bet(self, bet_id: str, user_id: str) -> bool:
        """Join an existing bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT amount, status FROM bets WHERE bet_id = ?", (bet_id,))
            row = c.fetchone()
            
            if not row:
                conn.close()
                return False
            
            amount, status = row[0], row[1]
            
            if status != 'open':
                conn.close()
                return False
            
            c.execute("SELECT user_id FROM bet_participants WHERE bet_id = ? AND user_id = ?", (bet_id, user_id))
            if c.fetchone():
                conn.close()
                return False
            
            c.execute('''INSERT INTO bet_participants (bet_id, user_id, side) VALUES (?, ?, 'B')''',
                     (bet_id, user_id))
            
            c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
            
            c.execute("UPDATE bets SET status = 'pending' WHERE bet_id = ?", (bet_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error joining bet: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def get_bet(self, bet_id: str) -> Optional[Dict]:
        """Get bet by ID"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT * FROM bets WHERE bet_id = ?", (bet_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'bet_id': row[0], 'creator_id': row[1], 'bet_topic': row[2],
                'bet_description': row[3], 'amount': row[4], 'bet_type': row[5],
                'status': row[6], 'created_at': row[7], 'resolved_at': row[8],
                'winner_id': row[9]
            }
        return None
    
    def get_bet_participants(self, bet_id: str) -> List[Dict]:
        """Get all participants in a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT bp.user_id, u.username, u.display_name, bp.side
                    FROM bet_participants bp
                    JOIN users u ON bp.user_id = u.user_id
                    WHERE bp.bet_id = ?''', (bet_id,))
        
        results = []
        for row in c.fetchall():
            results.append({'user_id': row[0], 'username': row[1], 'display_name': row[2], 'side': row[3]})
        
        conn.close()
        return results
    
    def get_open_bets(self) -> List[Dict]:
        """Get all open bets"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT b.bet_id, b.bet_topic, b.amount, b.status, b.created_at,
                    u.username, u.display_name
                    FROM bets b JOIN users u ON b.creator_id = u.user_id
                    WHERE b.status = 'open'
                    ORDER BY b.created_at DESC''')
        
        results = []
        for row in c.fetchall():
            results.append({
                'bet_id': row[0], 'bet_topic': row[1], 'amount': row[2],
                'status': row[3], 'created_at': row[4],
                'creator_username': row[5], 'creator_display': row[6]
            })
        
        conn.close()
        return results
    
    def resolve_bet(self, bet_id: str, winner_id: str) -> bool:
        """Resolve a bet and pay out winners"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT amount, status FROM bets WHERE bet_id = ?", (bet_id,))
            row = c.fetchone()
            
            if not row or row[1] != 'pending':
                conn.close()
                return False
            
            amount = row[0]
            
            c.execute("SELECT user_id, side FROM bet_participants WHERE bet_id = ?", (bet_id,))
            participants = c.fetchall()
            
            # Find winner's side
            winner_side = None
            for user_id, side in participants:
                if user_id == winner_id:
                    winner_side = side
                    break
            
            if not winner_side:
                conn.close()
                return False
            
            # Pay all winners on the winning side
            for user_id, side in participants:
                if side == winner_side:
                    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
                    c.execute("UPDATE users SET bets_won = bets_won + 1, total_won = total_won + ? WHERE user_id = ?",
                             (amount, user_id))
                else:
                    c.execute("UPDATE users SET bets_lost = bets_lost + 1, total_lost = total_lost + ? WHERE user_id = ?",
                             (amount, user_id))
            
            c.execute("UPDATE bets SET status = 'resolved', winner_id = ?, resolved_at = ? WHERE bet_id = ?",
                      (winner_id, datetime.now().isoformat(), bet_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error resolving bet: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def cancel_bet(self, bet_id: str) -> bool:
        """Cancel a bet and refund all participants"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT amount, status FROM bets WHERE bet_id = ?", (bet_id,))
            row = c.fetchone()
            
            if not row or row[1] != 'open':
                conn.close()
                return False
            
            amount = row[0]
            
            c.execute("SELECT user_id FROM bet_participants WHERE bet_id = ?", (bet_id,))
            participants = c.fetchall()
            
            for (user_id,) in participants:
                c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
            
            c.execute("UPDATE bets SET status = 'cancelled' WHERE bet_id = ?", (bet_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error cancelling bet: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def get_user_bets(self, user_id: str) -> List[Dict]:
        """Get all bets for a user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT b.bet_id, b.bet_topic, b.amount, b.status, b.created_at, b.winner_id
                    FROM bets b
                    JOIN bet_participants bp ON b.bet_id = bp.bet_id
                    WHERE bp.user_id = ?
                    ORDER BY b.created_at DESC''', (user_id,))
        
        results = []
        for row in c.fetchall():
            results.append({
                'bet_id': row[0], 'bet_topic': row[1], 'amount': row[2],
                'status': row[3], 'created_at': row[4], 'winner_id': row[5]
            })
        
        conn.close()
        return results
