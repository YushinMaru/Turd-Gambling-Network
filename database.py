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
    
    def create_bet_advanced(self, bet_id: str, creator_id: str, bet_topic: str, amount: int, 
                           bet_description: str = None, bet_type: str = '1v1', category: str = 'Random',
                           odds: str = 'even', visibility: str = 'open', expiration: str = '7d',
                           verification_type: str = 'manual') -> bool:
        """Create a new bet with all advanced options"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO bets (bet_id, creator_id, bet_topic, bet_description, amount,
                        bet_type, category, odds, visibility, expiration, verification_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (bet_id, creator_id, bet_topic, bet_description, amount,
                      bet_type, category, odds, visibility, expiration, verification_type))
            
            # Add creator as participant (side A)
            c.execute('''INSERT INTO bet_participants (bet_id, user_id, side)
                        VALUES (?, ?, 'A')''', (bet_id, creator_id))
            
            # Deduct from creator's balance
            c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, creator_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creating advanced bet: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def add_bet_participant(self, bet_id: str, user_id: str, side: str = 'B') -> bool:
        """Add a participant to a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO bet_participants (bet_id, user_id, side)
                        VALUES (?, ?, ?)''', (bet_id, user_id, side))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding participant: {e}")
            conn.close()
            return False
    
    def create_bet(self, bet_id: str, creator_id: str, bet_topic: str, amount: int, bet_description: str = None, 
                   verification_type: str = 'manual', verification_url: str = None, verification_claim: str = None,
                   verification_date: str = None) -> bool:
        """Create a new bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO bets (bet_id, creator_id, bet_topic, bet_description, amount, status, bet_type, category, odds, visibility, expiration, verification_type, verification_url, verification_claim, verification_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (bet_id, creator_id, bet_topic, bet_description, amount, 'open', '1v1', 'Random', 'even', 'open', '7d', verification_type, verification_url, verification_claim, verification_date))
            
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
    
    def join_bet(self, bet_id: str, user_id: str, side: str = 'B') -> bool:
        """Join an existing bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT amount, status, bet_type FROM bets WHERE bet_id = ?", (bet_id,))
            row = c.fetchone()
            
            if not row:
                conn.close()
                return False
            
            amount, status, bet_type = row[0], row[1], row[2]
            
            if status != 'open':
                conn.close()
                return False
            
            c.execute("SELECT user_id FROM bet_participants WHERE bet_id = ? AND user_id = ?", (bet_id, user_id))
            if c.fetchone():
                conn.close()
                return False
            
            # Determine side based on bet type
            if bet_type == '1v1':
                # Check if there's already someone on side B
                c.execute("SELECT user_id FROM bet_participants WHERE bet_id = ? AND side = 'B'", (bet_id,))
                if c.fetchone():
                    conn.close()
                    return False  # Side B already taken for 1v1
                target_side = 'B'
            elif bet_type == '1vMany':
                # Joiner always goes to side B
                target_side = 'B'
            elif bet_type == 'ManyvMany':
                # Determine side based on team assignment
                target_side = side
            else:
                target_side = side
            
            c.execute('''INSERT INTO bet_participants (bet_id, user_id, side) VALUES (?, ?, ?)''',
                     (bet_id, user_id, target_side))
            
            c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
            
            # Check if bet is now ready
            c.execute("SELECT COUNT(*) FROM bet_participants WHERE bet_id = ?", (bet_id,))
            participant_count = c.fetchone()[0]
            
            if bet_type == '1v1' and participant_count >= 2:
                c.execute("UPDATE bets SET status = 'pending' WHERE bet_id = ?", (bet_id,))
            elif bet_type == '1vMany' and participant_count >= 2:
                c.execute("UPDATE bets SET status = 'pending' WHERE bet_id = ?", (bet_id,))
            elif bet_type == 'ManyvMany':
                # Check if both teams have at least 1 person
                c.execute("SELECT side, COUNT(*) FROM bet_participants WHERE bet_id = ? GROUP BY side", (bet_id,))
                side_counts = c.fetchall()
                has_a = any(s == 'A' for s, _ in side_counts)
                has_b = any(s == 'B' for s, _ in side_counts)
                if has_a and has_b:
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
        
        # Use explicit column names to avoid misalignment issues
        c.execute('''SELECT bet_id, creator_id, bet_topic, bet_description, amount,
                    COALESCE(bet_type, '1v1') as bet_type,
                    COALESCE(category, 'Random') as category,
                    COALESCE(odds, 'even') as odds,
                    COALESCE(visibility, 'open') as visibility,
                    COALESCE(expiration, '7d') as expiration,
                    COALESCE(status, 'open') as status,
                    COALESCE(verification_type, 'manual') as verification_type,
                    proof_url, scheduled_resolve_time, created_at, resolved_at, winner_id,
                    prediction_a, prediction_b, prediction_actual
                    FROM bets WHERE bet_id = ?''', (bet_id,))
        row = c.fetchone()
        
        if row:
            result = {
                'bet_id': row[0],
                'creator_id': row[1],
                'bet_topic': row[2],
                'bet_description': row[3],
                'amount': row[4],
                'bet_type': row[5],
                'category': row[6],
                'odds': row[7],
                'visibility': row[8],
                'expiration': row[9],
                'status': row[10],
                'verification_type': row[11],
                'proof_url': row[12],
                'scheduled_resolve_time': row[13],
                'created_at': row[14],
                'resolved_at': row[15],
                'winner_id': row[16],
                'prediction_a': row[17],
                'prediction_b': row[18],
                'prediction_actual': row[19]
            }
            conn.close()
            return result
        conn.close()
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
    
    # ============== BET FIELD UPDATES ==============
    
    def update_bet(self, bet_id: str, **kwargs) -> bool:
        """Update bet fields"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values())
            values.append(bet_id)
            
            c.execute(f"UPDATE bets SET {fields} WHERE bet_id = ?", values)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating bet: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def set_bet_verification_type(self, bet_id: str, verification_type: str) -> bool:
        """Set verification type for a bet"""
        return self.update_bet(bet_id, verification_type=verification_type)
    
    def set_bet_proof_url(self, bet_id: str, proof_url: str) -> bool:
        """Set proof URL for a bet"""
        return self.update_bet(bet_id, proof_url=proof_url)
    
    def set_scheduled_resolve_time(self, bet_id: str, resolve_time: str) -> bool:
        """Set scheduled resolution time for a bet"""
        return self.update_bet(bet_id, scheduled_resolve_time=resolve_time)
    
    # ============== BET TAGS ==============
    
    def add_bet_tag(self, bet_id: str, tag: str) -> bool:
        """Add a tag to a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO bet_tags (bet_id, tag) VALUES (?, ?)", (bet_id, tag))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding bet tag: {e}")
            conn.close()
            return False
    
    def get_bet_tags(self, bet_id: str) -> List[str]:
        """Get all tags for a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT tag FROM bet_tags WHERE bet_id = ?", (bet_id,))
        tags = [row[0] for row in c.fetchall()]
        conn.close()
        return tags
    
    # ============== BET VOTES (Poll Verification) ==============
    
    def add_vote(self, bet_id: str, user_id: str, voted_for: str) -> bool:
        """Add a vote for a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            # Remove previous vote if exists
            c.execute("DELETE FROM bet_votes WHERE bet_id = ? AND user_id = ?", (bet_id, user_id))
            c.execute("INSERT INTO bet_votes (bet_id, user_id, voted_for) VALUES (?, ?, ?)", 
                     (bet_id, user_id, voted_for))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding vote: {e}")
            conn.close()
            return False
    
    def get_bet_votes(self, bet_id: str) -> Dict[str, int]:
        """Get vote counts for a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT voted_for, COUNT(*) FROM bet_votes WHERE bet_id = ? GROUP BY voted_for", (bet_id,))
        votes = {row[0]: row[1] for row in c.fetchall()}
        conn.close()
        return votes
    
    def get_user_vote(self, bet_id: str, user_id: str) -> Optional[str]:
        """Get what a user voted for"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("SELECT voted_for FROM bet_votes WHERE bet_id = ? AND user_id = ?", (bet_id, user_id))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    
    # ============== BET PROOF (Link Proof) ==============
    
    def submit_proof(self, bet_id: str, user_id: str, proof_url: str, description: str = None) -> bool:
        """Submit proof for a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO bet_proof (bet_id, user_id, proof_url, description) VALUES (?, ?, ?, ?)",
                     (bet_id, user_id, proof_url, description))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error submitting proof: {e}")
            conn.close()
            return False
    
    def get_bet_proof(self, bet_id: str) -> List[Dict]:
        """Get all proof submissions for a bet"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT bp.user_id, u.display_name, bp.proof_url, bp.description, bp.submitted_at
                    FROM bet_proof bp
                    JOIN users u ON bp.user_id = u.user_id
                    WHERE bp.bet_id = ?''', (bet_id,))
        
        results = []
        for row in c.fetchall():
            results.append({
                'user_id': row[0], 'display_name': row[1], 
                'proof_url': row[2], 'description': row[3], 'submitted_at': row[4]
            })
        
        conn.close()
        return results
    
    # ============== PREDICTION VERIFICATION ==============
    
    def set_prediction(self, bet_id: str, side: str, prediction: str) -> bool:
        """Set prediction for a side"""
        if side == 'A':
            return self.update_bet(bet_id, prediction_a=prediction)
        elif side == 'B':
            return self.update_bet(bet_id, prediction_b=prediction)
        return False
    
    def set_actual_result(self, bet_id: str, actual: str) -> bool:
        """Set the actual result for prediction verification"""
        return self.update_bet(bet_id, prediction_actual=actual)
