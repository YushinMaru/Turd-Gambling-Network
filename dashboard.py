"""
Dashboard - Main dashboard embed and views
"""

import discord
from typing import List, Dict, Optional
from datetime import datetime
from config import EMBED_COLOR, EMBED_COLOR_SUCCESS, EMBED_COLOR_ERROR
from database import DatabaseManager
from currency import CurrencyManager
from bets import BetManager
from quips import get_dashboard_quip


class DashboardBuilder:
    """Build the main dashboard embed"""
    
    def __init__(self, db: DatabaseManager, currency: CurrencyManager, bet_manager: BetManager):
        self.db = db
        self.currency = currency
        self.bet_manager = bet_manager
    
    def build_dashboard(self, guild: discord.Guild) -> discord.Embed:
        """Build the main dashboard embed"""
        embed = discord.Embed(
            title="🎰 Turd Casino",
            description="Welcome to the premier betting experience!",
            color=EMBED_COLOR,
            timestamp=datetime.now()
        )
        
        # Add quip with character name
        quip_text, character_name = get_dashboard_quip()
        embed.add_field(name=f"💬 {character_name} Says", value=f"_{quip_text}_", inline=False)
        
        # Get stats
        leaderboard = self.db.get_leaderboard(5)
        
        if leaderboard:
            lb_text = []
            for i, user in enumerate(leaderboard, 1):
                name = user['display_name'] or user['username']
                balance = user['balance']
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                lb_text.append(f"{emoji} {name}: **{balance:,}** TC")
            
            embed.add_field(name="🏆 Top Gamblers", value="\n".join(lb_text), inline=True)
        
        # Open bets
        open_bets = self.bet_manager.get_open_bets_list()
        
        if open_bets:
            bets_text = []
            for bet in open_bets[:5]:
                creator = bet['creator_display'] or bet['creator_username']
                bets_text.append(f"📋 `{bet['bet_id']}` - {bet['bet_topic']} ({bet['amount']:,} TC) by {creator}")
            
            if bets_text:
                embed.add_field(name="🎯 Open Bets", value="\n".join(bets_text), inline=False)
        
        # Footer with instructions
        embed.set_footer(text="Use the buttons below to interact • Turd Casino")
        
        return embed
    
    def build_balance_embed(self, user_id: str) -> discord.Embed:
        """Build user's balance display"""
        balance = self.currency.get_balance(user_id)
        
        embed = discord.Embed(
            title="💰 Your Balance",
            description=self.currency.format_balance(balance),
            color=EMBED_COLOR_SUCCESS
        )
        
        return embed
    
    def build_stats_embed(self, user_id: str) -> discord.Embed:
        """Build user's stats display"""
        stats = self.currency.get_user_stats(user_id)
        
        if not stats:
            embed = discord.Embed(
                title="📊 Your Stats",
                description="No stats yet. Place some bets!",
                color=EMBED_COLOR
            )
            return embed
        
        embed = discord.Embed(
            title="📊 Your Stats",
            description=self.currency.format_stats(user_id),
            color=EMBED_COLOR
        )
        
        return embed
    
    def build_leaderboard_embed(self) -> discord.Embed:
        """Build leaderboard display"""
        leaderboard = self.db.get_leaderboard(10)
        
        if not leaderboard:
            embed = discord.Embed(
                title="🏆 Leaderboard",
                description="No players yet!",
                color=EMBED_COLOR
            )
            return embed
        
        lines = []
        for i, user in enumerate(leaderboard, 1):
            name = user['display_name'] or user['username']
            balance = user['balance']
            wins = user['bets_won']
            losses = user['bets_lost']
            
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            lines.append(f"{emoji} **{name}** - {balance:,} TC (W: {wins} / L: {losses})")
        
        embed = discord.Embed(
            title="🏆 Leaderboard",
            description="\n".join(lines),
            color=EMBED_COLOR
        )
        
        return embed
    
    def build_my_bets_embed(self, user_id: str) -> discord.Embed:
        """Build user's bets display"""
        bets = self.bet_manager.get_user_bets(user_id)
        
        if not bets:
            embed = discord.Embed(
                title="🎫 Your Bets",
                description="You haven't participated in any bets yet!",
                color=EMBED_COLOR
            )
            return embed
        
        open_bets = [b for b in bets if b['status'] in ['open', 'pending']]
        resolved_bets = [b for b in bets if b['status'] == 'resolved']
        
        lines = []
        
        if open_bets:
            lines.append("**🎯 Active Bets:**")
            for bet in open_bets[:5]:
                lines.append(f"  `{bet['bet_id']}` - {bet['bet_topic']} ({bet['amount']:,} TC) - {bet['status']}")
        
        if resolved_bets:
            lines.append("\n**✅ Resolved Bets:**")
            for bet in resolved_bets[:5]:
                won = bet['winner_id'] == user_id
                result = "✅ WON" if won else "❌ LOST"
                lines.append(f"  `{bet['bet_id']}` - {bet['bet_topic']} ({bet['amount']:,} TC) - {result}")
        
        embed = discord.Embed(
            title="🎫 Your Bets",
            description="\n".join(lines) if lines else "No bets yet!",
            color=EMBED_COLOR
        )
        
        return embed
    
    def build_open_bets_embed(self) -> discord.Embed:
        """Build open bets list"""
        bets = self.bet_manager.get_open_bets_list()
        
        if not bets:
            embed = discord.Embed(
                title="🎯 Open Bets",
                description="No open bets right now. Create one!",
                color=EMBED_COLOR
            )
            return embed
        
        lines = []
        for bet in bets[:10]:
            creator = bet['creator_display'] or bet['creator_username']
            lines.append(f"📋 `{bet['bet_id']}`")
            lines.append(f"   Topic: {bet['bet_topic']}")
            lines.append(f"   Amount: {bet['amount']:,} TC | By: {creator}")
            lines.append("")
        
        embed = discord.Embed(
            title="🎯 Open Bets",
            description="\n".join(lines),
            color=EMBED_COLOR
        )
        
        return embed
    
    def build_user_analytics(self, user_id: str) -> discord.Embed:
        """Build detailed user analytics"""
        user = self.db.get_user(user_id)
        
        if not user:
            embed = discord.Embed(
                title="📊 Your Analytics",
                description="No data available yet.",
                color=EMBED_COLOR
            )
            return embed
        
        # Get user's bets
        bets = self.bet_manager.get_user_bets(user_id)
        
        total_bets = len(bets)
        resolved_bets = [b for b in bets if b['status'] == 'resolved']
        wins = sum(1 for b in resolved_bets if b['winner_id'] == user_id)
        losses = len(resolved_bets) - wins
        
        win_rate = (wins / len(resolved_bets) * 100) if resolved_bets else 0
        
        # Get category breakdown
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute('''SELECT b.category, COUNT(*) as count, SUM(b.amount) as total
                    FROM bets b
                    JOIN bet_participants bp ON b.bet_id = bp.bet_id
                    WHERE bp.user_id = ? AND b.status = 'resolved'
                    GROUP BY b.category''', (user_id,))
        category_rows = c.fetchall()
        
        c.execute('''SELECT b.bet_type, COUNT(*) as count
                    FROM bets b
                    JOIN bet_participants bp ON b.bet_id = bp.bet_id
                    WHERE bp.user_id = ? AND b.status = 'resolved'
                    GROUP BY b.bet_type''', (user_id,))
        type_rows = c.fetchall()
        conn.close()
        
        embed = discord.Embed(
            title=f"📊 Analytics for {user['display_name'] or user['username']}",
            color=EMBED_COLOR
        )
        
        # Overview
        embed.add_field(
            name="📈 Overview",
            value=f"**Total Bets:** {total_bets}\n"
                  f"**Resolved:** {len(resolved_bets)}\n"
                  f"**Wins:** {wins}\n"
                  f"**Losses:** {losses}\n"
                  f"**Win Rate:** {win_rate:.1f}%",
            inline=True
        )
        
        # Money
        embed.add_field(
            name="💰 Money",
            value=f"**Current Balance:** {user['balance']:,} TC\n"
                  f"**Total Won:** {user['total_won']:,} TC\n"
                  f"**Total Lost:** {user['total_lost']:,} TC\n"
                  f"**Net Profit:** {user['total_won'] - user['total_lost']:,} TC",
            inline=True
        )
        
        # Categories
        if category_rows:
            cat_text = "\n".join([f"{cat or 'Random'}: {count} ({total:,} TC)" 
                                  for cat, count, total in category_rows])
            embed.add_field(name="🎯 By Category", value=cat_text, inline=False)
        
        # Bet types
        if type_rows:
            type_text = "\n".join([f"{bt}: {count}" for bt, count in type_rows])
            embed.add_field(name="🎲 By Type", value=type_text, inline=True)
        
        return embed
