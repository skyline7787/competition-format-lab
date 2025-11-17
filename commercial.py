from typing import List
from format_engine import Match

# Tier 1 teams (top commercial markets)
# Later you can replace these with actual nation IDs
TIER_1_TEAMS = [1, 2, 3, 4, 5, 6, 7, 8]


def commercial_score(match: Match) -> float:
    """
    Assigns a commercial value score to a match.
    
    Logic:
    - Regular match = 1.0
    - One Tier 1 team = 1.5
    - Tier 1 vs Tier 1 = 2.0
    """
    home_t1 = match.home.id in TIER_1_TEAMS
    away_t1 = match.away.id in TIER_1_TEAMS

    if home_t1 and away_t1:
        return 2.0
    elif home_t1 or away_t1:
        return 1.5
    else:
        return 1.0


def total_commercial_value(matches: List[Match]) -> float:
    """
    Sum of commercial scores across all matches in a format.
    """
    return sum(commercial_score(m) for m in matches)
