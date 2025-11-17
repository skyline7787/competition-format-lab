from format_engine import build_group_stage, split_into_groups, create_teams
from metrics import matches_per_team, matches_per_round
from commercial import total_commercial_value


def run_format(
    name: str,
    num_teams: int,
    group_size: int,
    double_round: bool,
    show_sample_fixtures: bool = True,
):
    """
    Run a single competition format, print key metrics, and return a summary dict.
    """
    matches = build_group_stage(
        num_teams=num_teams,
        group_size=group_size,
        double_round=double_round,
    )

    teams = create_teams(num_teams)
    groups = split_into_groups(teams, group_size)
    num_groups = len(groups)

    print(f"\n=== {name} ===")
    print(f"Number of teams: {num_teams}")
    print(f"Group size: {group_size}")
    print(f"Number of groups: {num_groups}")
    print(f"Double round-robin: {double_round}")
    print(f"Total matches: {len(matches)}")
    print(f"Total commercial value score: {total_commercial_value(matches):.2f}")

    # Matches per team (just show a few)
    mpt = matches_per_team(matches)
    print("\nMatches per team (first 8):")
    for team, count in list(mpt.items())[:8]:
        print(f"  {team}: {count} matches")

    # Matches per round
    mpr = matches_per_round(matches)
    print("\nMatches per round:")
    for rnd, count in mpr.items():
        print(f"  Round {rnd}: {count} matches")

    # Commercial value by group
    print("\nCommercial value by group:")
    for gname, gteams in groups.items():
        group_matches = [m for m in matches if m.group_id == gname]
        group_score = total_commercial_value(group_matches)
        print(f"  {gname}: {group_score:.2f}")

    # Sample fixtures
    if show_sample_fixtures:
        print("\nSample fixtures (first 10):")
        for m in matches[:10]:
            print(f"  {m.group_id} | Round {m.round_number}: {m.home.name} vs {m.away.name}")

    # Return key metrics for comparison
    summary = {
        "name": name,
        "num_teams": num_teams,
        "group_size": group_size,
        "num_groups": num_groups,
        "double_round": double_round,
        "total_matches": len(matches),
        "total_commercial_value": total_commercial_value(matches),
    }
    return summary


def main():
    # Define two formats to compare
    format_a_params = {
        "name": "FORMAT A – 55 teams, groups of 5, double round",
        "num_teams": 55,
        "group_size": 5,
        "double_round": True,
    }

    format_b_params = {
        "name": "FORMAT B – 55 teams, groups of 5, single round",
        "num_teams": 55,
        "group_size": 5,
        "double_round": False,
    }

    # Run both formats
    summary_a = run_format(**format_a_params)
    summary_b = run_format(**format_b_params)

    # Comparison summary
    print("\n=== COMPARISON SUMMARY ===")

    print(f"Total matches: A = {summary_a['total_matches']} vs B = {summary_b['total_matches']}")
    delta_matches = summary_b["total_matches"] - summary_a["total_matches"]
    print(f"  Change in matches (B - A): {delta_matches}")

    print(
        f"Total commercial value: "
        f"A = {summary_a['total_commercial_value']:.2f} vs "
        f"B = {summary_b['total_commercial_value']:.2f}"
    )
    delta_value = summary_b["total_commercial_value"] - summary_a["total_commercial_value"]
    print(f"  Change in commercial score (B - A): {delta_value:.2f}")

    if summary_a["total_matches"] > 0:
        avg_a = summary_a["total_commercial_value"] / summary_a["total_matches"]
    else:
        avg_a = 0.0
    if summary_b["total_matches"] > 0:
        avg_b = summary_b["total_commercial_value"] / summary_b["total_matches"]
    else:
        avg_b = 0.0

    print(
        f"Average commercial value per match: "
        f"A = {avg_a:.3f} vs B = {avg_b:.3f}"
    )


if __name__ == "__main__":
    main()
