from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Team:
    id: int
    name: str


@dataclass
class Match:
    home: Team
    away: Team
    round_number: int
    group_id: str


def create_teams(num_teams: int) -> List[Team]:
    """
    Create a list of teams: Team 1, Team 2, ...
    Later you can replace this with real country names.
    """
    return [Team(id=i + 1, name=f"Team {i + 1}") for i in range(num_teams)]


def split_into_groups(teams: List[Team], group_size: int) -> Dict[str, List[Team]]:
    """
    Split the teams into groups of roughly equal size.
    Group names: 'Group A', 'Group B', etc.
    """
    if group_size <= 0:
        raise ValueError("group_size must be positive")

    groups: Dict[str, List[Team]] = {}
    group_index = 0

    for i in range(0, len(teams), group_size):
        chunk = teams[i : i + group_size]
        group_name = f"Group {chr(ord("A") + group_index)}"
        groups[group_name] = chunk
        group_index += 1

    return groups


def generate_round_robin_matches(
    group_id: str,
    teams: List[Team],
    double_round: bool = True,
) -> List[Match]:
    """
    Generate round-robin fixtures for a single group.
    Uses a standard round-robin 'circle method'.
    If double_round=True, each pairing is played twice (home/away).
    """
    if len(teams) < 2:
        return []

    # Handle odd number of teams by adding a dummy 'BYE'
    dummy = None
    if len(teams) % 2 == 1:
        dummy = Team(id=0, name="BYE")
        teams = teams + [dummy]

    n = len(teams)
    rounds = n - 1
    half = n // 2

    schedule: List[Match] = []
    team_list = teams[:]  # copy

    for r in range(rounds):
        # Pair teams for this round
        for i in range(half):
            home = team_list[i]
            away = team_list[n - 1 - i]

            if home is dummy or away is dummy:
                continue  # skip BYE matches

            round_number = r + 1

            # First leg
            schedule.append(
                Match(
                    home=home,
                    away=away,
                    round_number=round_number,
                    group_id=group_id,
                )
            )

            # Second leg (swap home/away) in later rounds, if double round-robin
            if double_round:
                schedule.append(
                    Match(
                        home=away,
                        away=home,
                        round_number=round_number + rounds,
                        group_id=group_id,
                    )
                )

        # Rotate teams (except the first) for next round
        fixed = team_list[0]
        rest = team_list[1:]
        rest = [rest[-1]] + rest[:-1]
        team_list = [fixed] + rest

    # Sort matches by round number then home team id
    schedule.sort(key=lambda m: (m.group_id, m.round_number, m.home.id))
    return schedule


def build_group_stage(
    num_teams: int,
    group_size: int,
    double_round: bool = True,
) -> List[Match]:
    """
    High-level helper:
    - Create teams
    - Split into groups
    - Generate all matches for each group
    """
    teams = create_teams(num_teams)
    groups = split_into_groups(teams, group_size)

    all_matches: List[Match] = []
    for group_name, group_teams in groups.items():
        matches = generate_round_robin_matches(
            group_id=group_name,
            teams=group_teams,
            double_round=double_round,
        )
        all_matches.extend(matches)

    # Global sort: by group, then round, then home team id
    all_matches.sort(key=lambda m: (m.group_id, m.round_number, m.home.id))
    return all_matches

