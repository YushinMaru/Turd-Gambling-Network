"""
Configuration and constants for Turd Gambling Network
Loads from .env file
"""

import os
from pathlib import Path

# Load .env file
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# ============== REQUIRED ENVIRONMENT VARIABLES ==============
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN', '')

# Channel IDs
DASHBOARD_CHANNEL_ID = int(os.environ.get('DASHBOARD_CHANNEL_ID', '0')) if os.environ.get('DASHBOARD_CHANNEL_ID', '0').isdigit() else 0
ANNOUNCEMENTS_CHANNEL_ID = int(os.environ.get('ANNOUNCEMENTS_CHANNEL_ID', '0')) if os.environ.get('ANNOUNCEMENTS_CHANNEL_ID', '0').isdigit() else 0
BET_THREADS_CHANNEL_ID = int(os.environ.get('BET_THREADS_CHANNEL_ID', '0')) if os.environ.get('BET_THREADS_CHANNEL_ID', '0').isdigit() else 0

# Turd Coins Configuration
STARTING_BALANCE = int(os.environ.get('STARTING_BALANCE', '1000'))
DAILY_BONUS_AMOUNT = int(os.environ.get('DAILY_BONUS_AMOUNT', '100'))
MIN_BET_AMOUNT = int(os.environ.get('MIN_BET_AMOUNT', '10'))
MAX_BET_AMOUNT = int(os.environ.get('MAX_BET_AMOUNT', '100000'))

# Database
DB_PATH = 'turd_gambling.db'

# Logging
LOG_FILE = 'bot.log'
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB

# Discord
EMBED_COLOR = 0x9B59B6  # Purple
EMBED_COLOR_SUCCESS = 0x2ECC71
EMBED_COLOR_ERROR = 0xE74C3C
EMBED_COLOR_WARNING = 0xF39C12

# Feature Flags (for future phases)
ENABLE_SPORTS_BETTING = False
ENABLE_PREDICTION_MARKETS = False

# Embed Limits
MAX_EMBED_TITLE = 256
MAX_EMBED_FIELD_NAME = 256
MAX_EMBED_FIELD_VALUE = 1024
MAX_EMBED_DESCRIPTION = 4096
MAX_EMBED_FIELDS = 25

# Rate Limiting
DISCORD_RATE_LIMIT = 50  # req/s
ASYNC_SLEEP_BULK = 0.02  # seconds between bulk sends
