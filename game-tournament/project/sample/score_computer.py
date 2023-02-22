import json, pathlib, os, time

from .match_maker import save_data
from ..data.input.game_params import logo

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
MATCHUPS_PATH = pathlib.Path(ROOT_DIR, "data", "output", "tournament.json")
TEAMS_PATH = pathlib.Path(ROOT_DIR, "data", "output", "teams.json")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_score_input(team):
    while True:
        user_input = int(input(f"What score did {team} get? [0-1]\n"))
        if user_input == 0 or user_input == 1:
            return user_input
        else:
            print("Invalid input. Please try again.")


def get_matchup_input(matchups):
    while True:
        user_input = int(input(f"\nSelect a matchup to input results: [1-{len(matchups)}]\n"))
        if user_input > 0 and user_input <= len(matchups):
            return user_input
        else:
            print("Invalid input. Please try again.")


def retrieve_json(path):
    ''' Opens the JSON file, reads its contents, and parse it. '''
    with open(path, 'r', encoding='utf8') as f:
        json_content = f.read()

    return json.loads(json_content)


def display_results(results):
    ''' Displays the results with an integer identifier. '''
    if len(results) > 0:
        print('\n\nLIST OF RESULTS:\n\n')
        for i, result in enumerate(results):
            if result["team_a_score"] == 1:
                print(f"{i+1}. {result['team_a']} vs. {result['team_b']} on {result['game']} | WINNER: {result['team_a']}")
            else:
                print(f"{i+1}. {result['team_a']} vs. {result['team_b']} on {result['game']} | WINNER: {result['team_b']}")


def display_matchups(matchups):
    ''' Displays the matchups with an integer identifier. '''
    print('LIST OF UNRESOLVED MATCHUPS:\n\n')
    for i, matchup in enumerate(matchups):
        print(f"{i+1}. {matchup['team_a']} vs. {matchup['team_b']} on {matchup['game']}")


def update_matchup(matchup, final):
    ''' Update a matchup with scores. '''
    while True:
        clear_console()

        matchup["team_a_score"] = get_score_input(matchup["team_a"])
        matchup["team_b_score"] = get_score_input(matchup["team_b"])

        if matchup["team_a_score"] == matchup["team_b_score"]:
            print("Scores can't be equal.")
            time.sleep(1)
        else:
            [d for d in final if d.get('team') == matchup["team_a"]][0]["score"] += matchup["team_a_score"]
            [d for d in final if d.get('team') == matchup["team_b"]][0]["score"] += matchup["team_b_score"]
            break


def main():
    clear_console()

    matchups = retrieve_json(MATCHUPS_PATH)
    teams = retrieve_json(TEAMS_PATH)

    scores = []
    for team in teams:
        scores.append({"team": team, "score": 0})

    results = []

    while len(matchups) > 0:

        print(logo)
        # Displays unresolved matchups
        display_matchups(matchups)
        display_results(results)

        # Ask the user to select a matchup to update
        selection = get_matchup_input(matchups)

        # Update the selected matchup with results
        selected_matchup = matchups[selection - 1]
        update_matchup(selected_matchup, scores)
        
        results.append(matchups.pop(selection - 1))

        time.sleep(1)
        clear_console()

    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    save_data(sorted_scores, "scores")


if __name__ == '__main__':
    main()