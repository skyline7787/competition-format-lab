from collections import Counter
from typing import List, Dict

from format_engine import Match


def matches_per_team(matches: List[Match]) -> Dict[str, int]:
    """
    Count how many matches each team plays across the competition.
    """
    counter = Counter()
    for m in matches:
        counter[m.home.name] += 1
        counter[m.away.name] += 1
    return dict(counter)


def matches_per_round(matches: List[Match]) -> Dict[int, int]:
    """
    Count how many matches are played in each round.
    """
    counter = Counter()
    for m in matches:
        counter[m.round_number] += 1
    return dict(sorted(counter.items()))
