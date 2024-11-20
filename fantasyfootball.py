import itertools
from tabulate import tabulate

team_aliases = {
    "Tom Brady Fan Club": "TBFC",
    "The OG of OG's": "OG",
    "Danish Lions": "Danish",
    "Team eL": "eL",
    "Ludwig's Giants": "Ludwig",
    "Watson's Massage Parlor": "Watson",
    "Harry's Genius Team": "Harry",
    "Maine lobster rolls": "Lobster",
    "Manning's Bagels": "Manning",
    "Mr.Universe": "Mr",
    "The King in the North": "TKITN",
    "The Rat Pack": "Rat"
}

standings = {"OG": {"wins": 9, "losses": 2, "PF": 1250.43, "PA": 1152.75},
             "Danish": {"wins": 8, "losses": 3, "PF": 1193.92, "PA": 992.53},
             "eL": {"wins": 6, "losses": 5, "PF": 1205.56, "PA": 1101.67},
             "Ludwig": {"wins": 6, "losses": 5, "PF": 1136.85, "PA": 1110.54},
             "Watson": {"wins": 6, "losses": 5, "PF": 1106.96, "PA": 1160.17},
             "TBFC": {"wins": 6, "losses": 5, "PF": 1099.85, "PA": 1049.92},
             "Harry": {"wins": 6, "losses": 5, "PF": 1048.07, "PA": 1049.67},
             "Lobster": {"wins": 5, "losses": 6, "PF": 1186.41, "PA": 1205.81},
             "Manning": {"wins": 5, "losses": 6, "PF": 1088.62, "PA": 1129.19},
             "Mr": {"wins": 4, "losses": 7, "PF": 1101.67, "PA": 1189.40},
             "TKITN": {"wins": 4, "losses": 7, "PF": 1029.95, "PA": 1076.58},
             "Rat": {"wins": 1, "losses": 10, "PF": 1043.44, "PA": 1273.50},
             }

matchups = [
    {"week": 12, "home": "TBFC", "away": "Danish", "p_home_win": 0.89},
    {"week": 12, "home": "OG", "away": "Mr", "p_home_win": 0.52},
    {"week": 12, "home": "Manning", "away": "Lobster", "p_home_win": 0.33},
    {"week": 12, "home": "Ludwig", "away": "Rat", "p_home_win": 0.81},
    {"week": 12, "home": "eL", "away": "TKITN", "p_home_win": 0.37},
    {"week": 12, "home": "Watson", "away": "Harry", "p_home_win": 0.38},
    {"week": 13, "home": "TBFC", "away": "Rat", "p_home_win": 0.73},
    {"week": 13, "home": "OG", "away": "eL", "p_home_win": 0.52},
    {"week": 13, "home": "Manning", "away": "Danish", "p_home_win": 0.39},
    {"week": 13, "home": "Ludwig", "away": "Mr", "p_home_win": 0.56},
    {"week": 13, "home": "Lobster", "away": "Watson", "p_home_win": 0.31},
    {"week": 13, "home": "TKITN", "away": "Harry", "p_home_win": 0.61}
    ]

# Simplified check without looking at the win probabilities for each game
def check_playoff_qualification(team_name):
    """
    Check what needs to happen for a given team to make the playoffs.
    Outputs the scenarios in a game-results-focused format with full team names
    and prints the league standings for each scenario.
    """
    # Use alias if provided
    alias_to_full = {v: k for k, v in team_aliases.items()}
    full_name = alias_to_full.get(team_name, team_name)

    # Simulate all scenarios
    scenarios = simulate_games_with_outcomes(matchups, standings)

    qualifying_scenarios = []
    for scenario in scenarios:
        # Sort teams by wins, points scored for tiebreakers
        ranked_teams = sorted(
            scenario["standings"].items(),
            key=lambda x: (-x[1]["wins"], -x[1]["PF"])
        )
        top_teams = [team[0] for team in ranked_teams[:6]]  # Top 6 teams qualify

        if full_name in [alias_to_full.get(team, team) for team in top_teams]:
            qualifying_scenarios.append(scenario)

    if qualifying_scenarios:
        print(f"{full_name} can qualify under the following scenarios:")
        for idx, scenario in enumerate(qualifying_scenarios, 1):
            print(f"\nScenario {idx}:")
            week = 12
            for i, result in enumerate(scenario["results"], 1):
                # Replace aliases with full names
                for alias, complete_name in alias_to_full.items():
                    result = result.replace(alias, complete_name)
                print(f"week {week}: {result}")
                if i % 6 == 0:  # Assuming 6 games per week
                    week += 1

            # Print standings for the current scenario
            print("\nLeague Standings for this scenario:")
            ranked_teams = sorted(
                scenario["standings"].items(),
                key=lambda x: (-x[1]["wins"], -x[1]["PF"])
            )
            for rank, (team, data) in enumerate(ranked_teams, 1):
                full_team_name = alias_to_full.get(team, team)
                print(f"  {rank}. {full_team_name} - Wins: {data['wins']}, Points Scored: {data['PF']}")
    else:
        print(f"{full_name} cannot qualify under any scenario.")


    # Statistics
    total_scenarios = len(scenarios)
    qualifying_count = len(qualifying_scenarios)
    qualifying_percentage = (qualifying_count / total_scenarios) * 100

    # Print results
    print(f"\n{team_name} Playoff Qualification Statistics:")
    print(f"  Total scenarios: {total_scenarios}")
    print(f"  Qualifying scenarios: {qualifying_count}")
    print(f"  Qualification percentage: {qualifying_percentage:.2f}%\n")

# Simulations where the win probability in each game is 50/50
def simulate_games_with_outcomes(matchups, standings):
    """
    Simulate all possible outcomes of the remaining matchups.
    Returns: List of scenarios with corresponding game results.
    """
    outcomes = list(itertools.product(["home_win", "away_win"], repeat=len(matchups)))
    scenarios = []

    for outcome in outcomes:
        # Create a copy of standings to simulate changes
        updated_standings = {team: data.copy() for team, data in standings.items()}
        game_results = []  # To store outcomes for this scenario

        # Apply each game's result in this outcome
        for i, result in enumerate(outcome):
            game = matchups[i]
            if result == "home_win":
                updated_standings[game["home"]]["wins"] += 1
                updated_standings[game["away"]]["losses"] += 1
                game_results.append(f"{game['home']} wins against {game['away']}")
            else:
                updated_standings[game["away"]]["wins"] += 1
                updated_standings[game["home"]]["losses"] += 1
                game_results.append(f"{game['away']} wins against {game['home']}")

        # Save this scenario
        scenarios.append({"standings": updated_standings, "results": game_results})

    return scenarios


def simulate_games_with_probabilities(matchups, standings):
    """
    Simulate all possible outcomes of the remaining matchups with probabilities.
    Updates the standings (wins, losses and points scored) for the teams in each scenario.

    Returns: List of scenarios with their probabilities and game results.
    """
    outcomes = list(itertools.product(["home_win", "away_win"], repeat=len(matchups)))
    scenarios = []

    for outcome in outcomes:
        updated_standings = {team: data.copy() for team, data in standings.items()}
        game_results = []
        scenario_probability = 1  # Initialize probability for this scenario

        for i, result in enumerate(outcome):
            game = matchups[i]
            if result == "home_win":
                updated_standings[game["home"]]["wins"] += 1
                updated_standings[game["away"]]["losses"] += 1
                scenario_probability *= game["p_home_win"]
                game_results.append(f"{game['home']} wins against {game['away']}")
            else:
                updated_standings[game["away"]]["wins"] += 1
                updated_standings[game["home"]]["losses"] += 1
                scenario_probability *= (1 - game["p_home_win"])
                game_results.append(f"{game['away']} wins against {game['home']}")

        scenarios.append({
            "standings": updated_standings,
            "results": game_results,
            "probability": scenario_probability
        })

    return scenarios


def check_playoff_qualification_with_sorted_probabilities(team_name):
    """
    Check what needs to happen for a given team to make the playoffs, along with probabilities.

    This function simulates all possible outcomes of remaining games in the league and calculates
    the probability of a given team qualifying for the playoffs (finishing in the top 6). The output
    includes:
      - Scenarios under which the team qualifies (sorted by probability).
      - League standings for each qualifying scenario.
      - The overall probability of the team qualifying.

    Parameters:
    team_name (str): The name (or alias) of the team to analyze.
                     This could be the alias ("TBFC") or the full name ("Tom Brady Fan Club").

    Returns:
    None: The results are printed directly, including the scenarios and statistics.
    """

    # Map aliases (short names) back to full names for clarity
    alias_to_full = {v: k for k, v in team_aliases.items()}
    full_name = alias_to_full.get(team_name, team_name)  # Convert alias to full name if needed

    # Step 1: Simulate all possible outcomes with associated probabilities
    # The `simulate_games_with_probabilities` function generates all matchups, probabilities,
    # and hypothetical standings for the remaining games.
    scenarios = simulate_games_with_probabilities(matchups, standings)

    # Step 2: Filter scenarios where the target team qualifies for the playoffs
    qualifying_scenarios = []
    for scenario in scenarios:
        adjusted_standings = scenario["standings"]

        # Step 2.1: Adjust total points scored (PF) for each winning team in the scenario
        for result in scenario["results"]:
            winner, loser = result.split(" wins against ")
            if winner in adjusted_standings:
                adjusted_standings[winner]["PF"] += 110  # Assume winning teams gain 110 points

        # Step 2.2: Rank teams based on wins and adjusted points scored (PF)
        ranked_teams = sorted(
            adjusted_standings.items(),
            key=lambda x: (-x[1]["wins"], -x[1]["PF"])  # Sort by wins first, then points scored
        )

        # Step 2.3: Check if the target team is in the top 6
        top_teams = [team[0] for team in ranked_teams[:6]]  # Top 6 teams qualify
        if full_name in [alias_to_full.get(team, team) for team in top_teams]:
            qualifying_scenarios.append({
                "results": scenario["results"],  # List of game results for this scenario
                "probability": scenario["probability"],  # Probability of this scenario
                "standings": adjusted_standings,  # Adjusted standings under this scenario
            })

    # Step 3: Display the qualifying scenarios
    if qualifying_scenarios:
        # Sort scenarios by probability in ascending order for better visualization
        qualifying_scenarios.sort(key=lambda s: s["probability"])

        print(f"{full_name} can qualify under the following scenarios:")
        for idx, scenario in enumerate(qualifying_scenarios, 1):
            print(f"\nScenario {idx} (Probability: {scenario['probability']:.2%}):")
            week = 12  # Start from week 12
            for i, result in enumerate(scenario["results"], 1):
                # Replace aliases in results with full team names for readability
                for alias, complete_name in alias_to_full.items():
                    result = result.replace(alias, complete_name)
                print(f"week {week}: {result}")
                if i % 6 == 0:  # Assuming 6 games per week
                    week += 1

            # Display standings for this scenario
            print("\nLeague Standings for this scenario:")
            ranked_teams = sorted(
                scenario["standings"].items(),
                key=lambda x: (-x[1]["wins"], -x[1]["PF"])  # Sort by wins and points scored
            )
            for rank, (team, data) in enumerate(ranked_teams, 1):
                full_team_name = alias_to_full.get(team, team)
                print(f"  {rank}. {full_team_name} {data['wins']}-{data['losses']}")

    else:
        print(f"{full_name} cannot qualify under any scenario.")

    # Step 4: Calculate and display the total qualification probability
    total_qualification_probability = sum(s["probability"] for s in qualifying_scenarios)
    print(f"\n{full_name} Playoff Qualification Statistics:")
    print(f"  Total qualification probability: {total_qualification_probability:.2%}\n")


# Example usage 4096
check_playoff_qualification_with_sorted_probabilities("Rat")
#check_playoff_qualification("Mr")

