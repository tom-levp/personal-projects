from collections import Counter
import random, json, pathlib
import pandas as pd

from ..data.input.game_params import players, games, logo

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]

# For team making
def pop_random(list):
    """ Delete a random element from a list and return its name """
    idx = random.randrange(0, len(list))
    return list.pop(idx)


def make_teams(players):
    """ Return a list of teams from a list of players """
    teams = []
    init_len = len(players)

    while len(players) > 0:
        if (init_len % 2) != 0 and len(players) == init_len:
            rand1 = pop_random(players)
            rand2 = pop_random(players)
            rand3 = pop_random(players)
            pair = rand1, rand2, rand3
            teams.append(pair)

        else:
            rand1 = pop_random(players)
            rand2 = pop_random(players)
            pair = rand1, rand2
            teams.append(pair)

    return teams


def make_tournament(players, games):
    teams = make_teams(players)
    pairs = [(i, j) for i in teams for j in teams if i != j]
    random.shuffle(pairs)
    match_ups = list(set(map(tuple, map(sorted, pairs))))

    mu_list = []
    final_list = []

    for match_up in match_ups:
        while True:
            game = random.choice(games)
            
            if Counter(mu_list)[(match_up[0], game)] == 0 and Counter(mu_list)[(match_up[1], game)] == 0:
                mu_list.append((match_up[0], game))
                mu_list.append((match_up[1], game))

                turn = {

                    "team_1": match_up[0],
                    "team_2": match_up[1],
                    "game": game

                }

                final_list.append(turn)

                break
            else:
                continue

    program = []
    for team in teams:
        dict = {"team": team, "games": []}
        for element in mu_list:
            if team in element:
                dict["games"].append(element[1])
        dict["nb_games"] = len(set(dict["games"]))
        program.append(dict)
    
    return final_list, program


def save_data(retrieved_data, fileName):
    json_path = pathlib.Path(f"{ROOT_DIR}\\data\\output", f"{fileName}.json")
    csv_path = pathlib.Path(f"{ROOT_DIR}\\data\\output", f"{fileName}.csv")

    # write JSON files:
    with json_path.open("w", encoding="UTF-8") as target: 
        json.dump(retrieved_data, target, indent=4, ensure_ascii=False)

    # write CSV files:
    df = pd.read_json(json_path, encoding='utf-8-sig')
    df.to_csv(csv_path, index = None, encoding='utf-8-sig')


if __name__ == '__main__':
    print(logo)
    tournament, program = make_tournament(players, games)
    save_data(tournament, "tournament")
    save_data(program, "program")