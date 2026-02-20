"""
Turd Bird Industries Character Quips
Fred, Larry, and Ronald quotes for dashboard flavor
"""

import random


class QuipGenerator:
    """Generate character quips for the dashboard"""
    
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
    ]
    
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
    ]
    
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
    ]
    
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
    ]
    
    @classmethod
    def get_random_quip(cls, character: str = None) -> str:
        """Get a random quip from a specific character or random character"""
        if character is None:
            character = random.choice(['fred', 'larry', 'ronald', 'pete'])
        
        character = character.lower()
        
        if character == 'fred':
            return random.choice(cls.FRED_QUIPS)
        elif character == 'larry':
            return random.choice(cls.LARRY_QUIPS)
        elif character == 'ronald':
            return random.choice(cls.RONALD_QUIPS)
        elif character == 'pete':
            return random.choice(cls.PETE_QUIPS)
        else:
            return random.choice(cls.FRED_QUIPS)
    
    @classmethod
    def get_dashboard_quip(cls) -> str:
        """Get a random quip for dashboard display"""
        # Weighted towards Fred and Larry (the main characters)
        character = random.choices(
            ['fred', 'larry', 'ronald', 'pete'],
            weights=[35, 30, 20, 15]
        )[0]
        return cls.get_random_quip(character)
    
    @classmethod
    def get_winner_quip(cls, winner_name: str = None) -> str:
        """Get a quip for when someone wins a bet"""
        quips = [
            f"Congratulations. I suppose someone had to win. Well done.",
            f"A win? How unexpected. Don't let it go to your head.",
            f"Statistical anomaly achieved. Carry on.",
            f"Finally, some competence around here. Good job.",
            f"The numbers don't lie. Except when they do. But not today.",
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
        ]
        return random.choice(quips)


def get_quip(character: str = None) -> str:
    """Convenience function"""
    return QuipGenerator.get_random_quip(character)


def get_dashboard_quip() -> str:
    """Convenience function for dashboard"""
    return QuipGenerator.get_dashboard_quip()
