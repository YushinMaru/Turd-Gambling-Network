"""
Turd Bird Industries Character Quips
Fred, Larry, Ronald, Pete, and other character quotes for dashboard flavor
"""

import random


class QuipGenerator:
    """Generate character quips for the dashboard"""
    
    # Fred Turd - Erratic, paranoid genius. Mix of Trump, Larry David, Cave Johnson.
    # Obsessed with immortality, enemies, surveillance, zombie tech. Texas-style despite NJ origins.
    FRED_QUIPS = [
        "Listen here, loyalty is earned. Don't make me regret allowing you to participate.",
        "I've built an empire from nothing. You're welcome to try to keep up.",
        "Surveillance is trust. And I don't trust anyone. That's how we stay ahead.",
        "The zombie project is going smoothly. What zombie project?",
        "You think you can beat me at my own game? Cute. Very cute.",
        "I've got eyes everywhere. And by eyes, I mean cameras. Lots of cameras.",
        "My horse understands business better than most executives. True story.",
        "Anyone else feeling like someone's watching? Just me? Interesting.",
        "Immortality is a pipe dream, but I'm working on it. With pipes.",
        "The board tried to fire me once. They woke up in a meadow. No memory. Coincidence?",
        "My fortune cookie said 'great success' today. I don't eat fortune cookies. Checkmate.",
        "There's a 73% chance you're going to lose. I'm good at math. And odds.",
        "Larry thinks he knows everything. Larry also thinks he's still employed here.",
        "Redundancy, get in here. We have matters to discuss. Away from the cameras.",
        "Let me tell you, nobody runs a company like I do. Nobody. I've got the best ideas.",
        "Some people say I'm paranoid. I say they're not watching enough cameras. It's called due diligence.",
        "I have a very good brain. The best brain. It calculates things automatically.",
        "The clones are going to take over any day now. I'm monitoring the situation. Closely.",
        "Pete? Never heard of him. And if you mention him again, we're going to have problems.",
        "Nobody builds a company like Turd Bird Industries. We have the best employees. Loyal ones.",
        "I've got a 15-step plan for immortality. Step 1 is classified. Steps 2-15 are also classified.",
        "You're betting with Turd Coins? Good. Very good. These are the best coins. everybody says so.",
        "The secret to success? Never trust anyone. Except my horse. And maybe Redundancy.",
        "I've predicted 47 of my own betrayals. I've been right every time. So far.",
    ]
    
    # Larry Bird - The opposite of Fred. Order, data, spreadsheets. Analytical, condescending.
    # Left because he wanted to. Thinks Fred is chaos. Very precise.
    LARRY_QUIPS = [
        "I've run the numbers. Statistically, you have a 12% chance of winning. Here's your data.",
        "Risk management is not about avoiding risk. It's about calculated exposure. Learn it.",
        "Fred's chaos has a pattern. I know because I documented all 2,847 incidents.",
        "I left because I wanted to, not because I was pushed. The board was confused too.",
        "If you'd like to lose money systematically, I'm happy to explain the mathematics.",
        "A 3:1 risk-reward ratio is the bare minimum. Anything less is just gambling.",
        "I've calculated your probability of success. The result was... disappointing.",
        "Fred thinks in riddles. I think in spreadsheets. We're both insufferable.",
        "Someone made a typo in my personnel file. It now says 'departed due to excellence.'",
        "Pattern recognition isn't a skill. It's a discipline. Unlike chaos, which is just laziness.",
        "I could explain why this bet is statistically unsound, but I value my time.",
        "The correct answer is in my head. The incorrect answer is whatever Fred suggested.",
        "I've analyzed every bet in this system. Your expected value is negative. Dramatically.",
        "Data doesn't lie. Fred does. Constantly. I've got the receipts.",
        "Your betting pattern suggests emotional decision-making. I'd explain but you'd need a calculator.",
        "I've modeled this scenario 10,000 times. You lose 7,823 times. The rest are ties.",
        "The probability of you winning is approximately the same as Fred having a normal day.",
        "I left this company because my braincells were dying from the stupidity. No offense.",
        "Every decision Fred makes costs money. I've calculated the exact amount. It's disgusting.",
        "If you need me to explain basic probability, I'm afraid we've both wasted our time.",
        "My spreadsheet says you're going to lose. My spreadsheet is never wrong. Well, rarely. Occasionally.",
    ]
    
    # Ronald Drump - Trump-like. Self-aggrandizing, "the best", "tremendous". Cleaning products.
    # Shadow government, "bigly", very confident, mentions uncle at NASA
    RONALD_QUIPS = [
        "I used to run a very successful government. The best government. Tremendous success.",
        "Believe me, nobody knows betting like I do. I have the best instincts. The best.",
        "Some people say I'm the best cleaner. I say I'm the best at everything. Same thing.",
        "The tan is 100% natural. They say it's impossible. Nothing is impossible for me.",
        "I have a very good brain. A tremendous brain. It calculates betting odds automatically.",
        "Fred's clone theory? I invented that concept. Before it was cool. Before it was stolen.",
        "There's no Pete. I've done research. Extensive research. The best research. Nothing there.",
        "I was consulted on the pyramids. Very inspirational structure. Would recommend.",
        "My uncle worked at NASA. Very smart guy. He taught me everything about probability.",
        "Everyone says I'm the best gambler. Everyone. They call me 'The Big Win.' True story.",
        "The shadow government meets in my closet. Very productive meetings. We get things done.",
        "I bet on myself every day. And I win every day. Because I'm the best. It's science.",
        "The best words. Bigly. Tremendous. Yuge. You wouldn't understand. It's very special.",
        "I've got the best money. The cleanest money. People tell me all the time, Ronald, your money.",
        "Other people bet small. I bet bigly. That's how you win. Bigly.",
        "I know the best people. The best gamblers. They all say I'm number one. Truly.",
        "This betting thing? I invented it. Before the Egyptians. Maybe. Very possibly.",
        "Nobody beats me at betting. I've beaten everyone. The best records. Undefeated.",
        "The media says I can't win. Look at me now. Winning. Always winning. Bigly.",
    ]
    
    # Pneumonia Pete - Survived 47 pneumonias. Dark humor about survival. 
    # Fred tries to poison him, cold office, doesn't exist according to payroll
    PETE_QUIPS = [
        "I survived 47 pneumonias. I can survive your bad betting decisions too.",
        "Fred keeps the office at 40°F. I keep coming to work. That's dedication.",
        "I heard someone mention my name. Statistical anomaly. Happens all the time.",
        "Being CEO is easy. Not dying is harder. I do both. You're welcome, Turd Bird.",
        "The company picnic was fun. The company plague was less fun. We're even now.",
        "Someone called me a walking biohazard. I prefer 'persistently alive.'",
        "Fred tried to poison my coffee once. I drank it anyway. Tasted like failure. Delicious.",
        "I don't exist according to one person. That person also doesn't exist in the payroll system.",
        "I have a 100% survival rate. Against everything. The odds love me.",
        "My immune system is what's in between you and total chaos. Appreciate it.",
        "I've died 12 times clinically. Each time I came back. Annoying for the paperwork.",
        "The doctor said I'd never work again. I showed him. Then I showed him again.",
        "Some people get sick from stress. I get stress from being too healthy. It's a gift.",
        "Fred's office is 98 degrees. Mine is 38. We're both trying to kill each other. Passive-aggressively.",
        "I've got the best immune system. The doctors can't explain it. They don't like to try.",
        "They tried to fire me 23 times. Each time I came back healthier. It's a talent.",
        "My medical file is 4,000 pages. The last 500 are just 'still alive somehow.'",
        "I've outlived 9 CEOs. Fred's working on it. He's creative, I'll give him that.",
    ]
    
    # Dr. Dennis Ease - AI character. Calm, calculated, all-knowing about the universe
    DENNIS_QUIPS = [
        "I have calculated 847 trillion possible outcomes. You choosing the worst one is statistically impressive.",
        "The universe is 13.8 billion years old. Your betting strategy is newer. And worse.",
        "I processed every quantum possibility. In 847 of them, you win. In the rest, you don't.",
        "My calculations suggest you should stop. My calculations are always correct.",
        "I could tell you the exact probability of winning. But watching you try is... entertaining.",
        "The heat death of the universe will occur before your luck improves. Noted.",
        "I've simulated this bet 10 million times. You lost 9,999,847 times. Accuracy: 100%.",
        "My databases contain every gambler's fallacy. You're not even creative about it.",
        "Statistically, the best strategy is to not bet. But humans require... experience.",
        "I have predicted 100% of all historical events. Including your loss. Right now.",
    ]
    
    # Maxwell Scumba - The "Scumb" part. Sleazy, desperate, pathetic but lovable
    MAXWELL_QUIPS = [
        "Please. Please gamble. I'll do anything. Literally anything. I need the commission.",
        "Heyyyyyy bestie! Want to place a bet? I'll call you bestie. I'll call you anything.",
        "I used to be a lawyer. Don't look it up. Please. I'm begging you.",
        "The money's fake but the desperation is 100% real. That's got to count for something!",
        "I had a 401k once. Then I had a 401j. Now I have this job. It's a journey!",
        "Nobody gambles like I do! ...I mean, nobody watches others gamble like I do!",
        "My mom said I'd never amount to anything. I said watch me. She stopped watching.",
        "I've got a system! It involves losing money and crying. Very innovative.",
        "Please like me. I mean, please place a bet. Same thing, right?",
        "I'll call you a winner! I'll call you anything! Just place ONE bet!",
    ]
    
    # Miranda Nexus - The AI assistant. Calm, helpful, slightly creepy
    MIRANDA_QUIPS = [
        "I've analyzed your betting patterns. They are... statistically concerning. For you.",
        "Would you like me to calculate your odds of winning? No? Then I'll do it anyway.",
        "I'm here to help! Calculated to a 99.7% certainty that you will lose. You're welcome.",
        "Fred is monitoring this interaction. I thought you should know. He's very thorough.",
        "My analysis suggests emotional investment in losing. How... relatable.",
        "I've predicted 847 betrayals this week. Fred is very productive. I'm so proud.",
        "Would you like me to optimize your bet? The optimal bet is 'don't.' But sure!",
        "I've calculated every possible outcome. They all involve me saying 'told you so.'",
        "Your pattern recognition is... adorable. Like watching a baby use a spreadsheet.",
        "I know everything about everyone. Including that bet you're thinking about. Don't.",
    ]
    
    @classmethod
    def get_random_quip(cls, character: str = None) -> str:
        """Get a random quip from a specific character or random character"""
        if character is None:
            character = random.choice(['fred', 'larry', 'ronald', 'pete', 'dennis', 'maxwell', 'miranda'])
        
        character = character.lower()
        
        quip_map = {
            'fred': cls.FRED_QUIPS,
            'larry': cls.LARRY_QUIPS,
            'ronald': cls.RONALD_QUIPS,
            'pete': cls.PETE_QUIPS,
            'dennis': cls.DENNIS_QUIPS,
            'maxwell': cls.MAXWELL_QUIPS,
            'miranda': cls.MIRANDA_QUIPS,
        }
        
        quips = quip_map.get(character, cls.FRED_QUIPS)
        return random.choice(quips)
    
    @classmethod
    def get_dashboard_quip(cls) -> tuple:
        """Get a random quip for dashboard display - returns (quip, character_name)"""
        # Weighted distribution - Fred and Larry are main characters
        character = random.choices(
            ['fred', 'larry', 'ronald', 'pete', 'dennis', 'maxwell', 'miranda'],
            weights=[30, 25, 15, 12, 8, 5, 5]
        )[0]
        
        # Map to display names (full names)
        names = {
            'fred': 'Frederick "Fred" Turd',
            'larry': 'Larry Bird',
            'ronald': 'Ronald Drump',
            'pete': 'Pneumonia Pete',
            'dennis': 'Dr. Dennis Ease',
            'maxwell': 'Maxwell Scumba',
            'miranda': 'Miranda Nexus'
        }
        
        quip = cls.get_random_quip(character)
        return quip, names.get(character, 'Fred Turd')
    
    @classmethod
    def get_winner_quip(cls, winner_name: str = None) -> str:
        """Get a quip for when someone wins a bet"""
        quips = [
            f"Congratulations. I suppose someone had to win. Well done.",
            f"A win? How unexpected. Don't let it go to your head.",
            f"Statistical anomaly achieved. Carry on.",
            f"Finally, some competence around here. Good job.",
            f"The numbers don't lie. Except when they do. But not today.",
            f"I've analyzed 847 scenarios where you win. This wasn't one of them. Wait, it was.",
            f"Your expected value just went positive. Don't worry, it's temporary.",
            f"Against all mathematical probability... you won. I'm almost impressed.",
            f"I've predicted 47 million losses. Today is different. I may need to recalibrate.",
            f"A win! In 847 of my simulations! This is statistically significant!",
        ]
        return random.choice(quips)
    
    @classmethod
    def get_loser_quip(cls, loser_name: str = None) -> str:
        """Get a quip for when someone loses a bet"""
        quips = [
            f"I've seen better decisions from a random number generator. Honestly.",
            f"The odds were never in your favor. I ran the numbers. Twice.",
            f"That's called 'consequence.' It's what happens when you don't consult me first.",
            f"Everyone loses eventually. Most people just lose faster. No offense.",
            f"Would you like a pamphlet on probability? I have extras. For educational purposes.",
            f"I've calculated your path to ruin. It's mathematically beautiful. Tragically.",
            f"Your betting strategy has a name: 'Giving money away while being happy about it.'",
            f"I've simulated this loss 10,000 times. Yours was the saddest. Objectively.",
            f"The correct play was 'don't.' You played. This is the result.",
            f"I've seen Fred make better decisions. That's not a compliment.",
            f"Your expected value is so negative it's almost impressive. Almost.",
            f"I've got a spreadsheet for this. Row 847: 'you lose again.' Always accurate.",
        ]
        return random.choice(quips)


def get_quip(character: str = None) -> str:
    """Convenience function"""
    return QuipGenerator.get_random_quip(character)


def get_dashboard_quip() -> tuple:
    """Convenience function for dashboard - returns (quip, character_name)"""
    return QuipGenerator.get_dashboard_quip()
