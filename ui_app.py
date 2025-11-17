import streamlit as st

from format_engine import (
    build_group_stage,
    build_group_stage_seeded,
    create_teams,
    split_into_groups,
)
from commercial import total_commercial_value
from metrics import matches_per_team, matches_per_round


st.title("Competition Format Lab")

st.sidebar.header("Format Parameters")

num_teams = st.sidebar.number_input(
    "Number of teams", min_value=4, max_value=60, value=55, step=1
)
group_size = st.sidebar.number_input(
    "Group size", min_value=2, max_value=10, value=5, step=1
)
double_round = st.sidebar.checkbox(
    "Double round-robin (home & away)", value=True
)
use_seeding = st.sidebar.checkbox("Use seeding (pots)", value=False)

if st.sidebar.button("Generate format"):
    # Build matches using chosen parameters
    if use_seeding:
        matches = build_group_stage_seeded(
            num_teams=num_teams,
            group_size=group_size,
            double_round=double_round,
        )
    else:
        matches = build_group_stage(
            num_teams=num_teams,
            group_size=group_size,
            double_round=double_round,
        )

    teams = create_teams(num_teams)
    groups = split_into_groups(teams, group_size)

    # --- Summary section ---
    st.subheader("Summary")

    mpt = matches_per_team(matches)
    mpr = matches_per_round(matches)
    total_value = total_commercial_value(matches)

    st.write(f"**Number of teams:** {num_teams}")
    st.write(f"**Group size:** {group_size}")
    st.write(f"**Number of groups:** {len(groups)}")
    st.write(f"**Double round-robin:** {double_round}")
    st.write(f"**Total matches:** {len(matches)}")
    st.write(f"**Total commercial value score:** {total_value:.2f}")

    avg_value = total_value / len(matches) if matches else 0.0
    st.write(f"**Average commercial value per match:** {avg_value:.3f}")

    # --- Groups section ---
    st.subheader("Groups")

    for gname, gteams in groups.items():
        team_names = ", ".join([t.name for t in gteams])
        st.write(f"**{gname}:** {team_names}")

    # --- Matches per round ---
    st.subheader("Matches per round")
    for rnd, count in mpr.items():
        st.write(f"Round {rnd}: {count} matches")

    # --- Sample fixtures ---
    st.subheader("Sample fixtures")
    for m in matches[:50]:
        st.write(
            f"{m.group_id} | Round {m.round_number}: "
            f"{m.home.name} vs {m.away.name}"
        )
else:
    st.info("Set parameters in the sidebar and click **Generate format**.")
