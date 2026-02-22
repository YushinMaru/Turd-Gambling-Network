"""
Database initialization and schema for Turd Gambling Network
"""

import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handles database schema initialization"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
    
    def init_database(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                display_name TEXT,
                balance INTEGER DEFAULT 1000,
                total_won INTEGER DEFAULT 0,
                total_lost INTEGER DEFAULT 0,
                bets_won INTEGER DEFAULT 0,
                bets_lost INTEGER DEFAULT 0,
                daily_bonus_claimed TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create bets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bets (
                bet_id TEXT PRIMARY KEY,
                creator_id TEXT NOT NULL,
                bet_topic TEXT NOT NULL,
                bet_description TEXT,
                amount INTEGER NOT NULL,
                bet_type TEXT DEFAULT '1v1',
                category TEXT DEFAULT 'Random',
                odds TEXT DEFAULT 'even',
                visibility TEXT DEFAULT 'open',
                expiration TEXT DEFAULT '7d',
                status TEXT DEFAULT 'open',
                verification_type TEXT DEFAULT 'manual',
                proof_url TEXT,
                scheduled_resolve_time TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT,
                winner_id TEXT,
                FOREIGN KEY (creator_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create bet_participants table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bet_participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bet_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                side TEXT NOT NULL,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(bet_id, user_id)
            )
        ''')
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                bet_id TEXT,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create daily_bonus_log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_bonus_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount INTEGER NOT NULL,
                claimed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create bet_tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bet_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bet_id TEXT NOT NULL,
                tag TEXT NOT NULL,
                FOREIGN KEY (bet_id) REFERENCES bets(bet_id)
            )
        ''')
        
        # Create bet_votes table for poll verification
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bet_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bet_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                voted_for TEXT NOT NULL,
                voted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create bet_proof table for link proof verification
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bet_proof (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bet_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                proof_url TEXT NOT NULL,
                description TEXT,
                submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        
        # Migration: Add missing columns to existing tables
        self._migrate_bets_table(cursor)
        
        conn.close()
        logger.info("Database initialized successfully")
    
    def _migrate_bets_table(self, cursor):
        """Add missing columns to bets table for existing databases"""
        try:
            # Get current columns
            cursor.execute("PRAGMA table_info(bets)")
            existing_columns = [row[1] for row in cursor.fetchall()]
            
            migrations = {
                'bet_type': "ALTER TABLE bets ADD COLUMN bet_type TEXT DEFAULT '1v1'",
                'category': "ALTER TABLE bets ADD COLUMN category TEXT DEFAULT 'Random'",
                'odds': "ALTER TABLE bets ADD COLUMN odds TEXT DEFAULT 'even'",
                'visibility': "ALTER TABLE bets ADD COLUMN visibility TEXT DEFAULT 'open'",
                'expiration': "ALTER TABLE bets ADD COLUMN expiration TEXT DEFAULT '7d'",
                'status': "ALTER TABLE bets ADD COLUMN status TEXT DEFAULT 'open'",
                'verification_type': "ALTER TABLE bets ADD COLUMN verification_type TEXT DEFAULT 'manual'",
                'proof_url': "ALTER TABLE bets ADD COLUMN proof_url TEXT",
                'scheduled_resolve_time': "ALTER TABLE bets ADD COLUMN scheduled_resolve_time TEXT",
                'created_at': "ALTER TABLE bets ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP",
                'resolved_at': "ALTER TABLE bets ADD COLUMN resolved_at TEXT",
                'winner_id': "ALTER TABLE bets ADD COLUMN winner_id TEXT"
            }
            
            for col, sql in migrations.items():
                if col not in existing_columns:
                    try:
                        cursor.execute(sql)
                        logger.info(f"Migration: Added column {col} to bets table")
                    except Exception as e:
                        logger.warning(f"Migration error for {col}: {e}")
            
        except Exception as e:
            logger.warning(f"Migration check error: {e}")
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper settings"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn


def init_db():
    """Initialize the database"""
    initializer = DatabaseInitializer()
    initializer.init_database()


if __name__ == "__main__":
    init_db()
    print("Database initialized!")
