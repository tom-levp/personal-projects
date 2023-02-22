# ROUND ROBIN GAME TOURNAMENT

## Presentation
My friends and I love board and video games... especially when we can pit ourselves against each other.
When building this project, the objective was precisely to help in setting up flexible tournaments with a variable number of players.

Following the Round Robin format, any team will play against all the other teams. Combination rules gives then ${n \choose k} = \frac{n!}{k!(n-k)!}$ where ${n \choose k}$ possible matchups, with $n$ being the number of distinct teams, and $k$ the size of combinations.

## Parameters preparation
Before running the main apps, head first into `/data/input/game_params.py`. Here, you must fill three lists:
* _team_size_, integer which must be equal to 1 or 2 (*_need to work on that to increase this limit_*);
* _players_, a bunch of strings, you can put whatever you want here,
* and _games_, likewise.

## Core apps
There are two core apps:
* _match_maker.py_, which must be run first in order to create random teams of players and their matchups with the following constraints:
    * Every team should not play the same game twice
    * Every team must play against all the other teams
<br>Running this script will create files in the `/data/output/` directory. With these you can keep track of the teams, their corresponding individual program (which games and how many), as well as the tournament matchups.
* _score_computer.py_, which must be run after, to properly follow the tournament, see the list of unresolved matchups and input team scores once the matchups are settled

## Demo
![Demo](test)
