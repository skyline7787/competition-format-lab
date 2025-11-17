from format_engine import build_group_stage
from metrics import matches_per_team, matches_per_round


def run_example():
    """
    Example scenario:
    - 24 teams
    - Groups of 4
    - Double round-robin
    You can change these numbers to simulate other formats.
    """
    num_teams = 55
    group_size = 5
    double_round = True

    matches = build_group_stage(
        num_teams=num_teams,
        group_size=group_size,
        double_round=double_round,
    )

    print("=== COMPETITION FORMAT SUMMARY ===")
    print(f"Number of teams: {num_teams}")
    print(f"Group size: {group_size}")
    print(f"Double round-robin: {double_round}")
    print(f"Total matches: {len(matches)}")

    # Matches per team
    mpt = matches_per_team(matches)
    print("\nMatches per team (first 10):")
    for team, count in list(mpt.items())[:10]:
        print(f"  {team}: {count} matches")

    # Matches per round
    mpr = matches_per_round(matches)
    print("\nMatches per round:")
    for rnd, count in mpr.items():
        print(f"  Round {rnd}: {count} matches")

    # Sample fixtures
    print("\nSample fixtures (first 12):")
    for m in matches[:12]:
        print(f"  {m.group_id} | Round {m.round_number}: {m.home.name} vs {m.away.name}")


if __name__ == "__main__":
    run_example()
