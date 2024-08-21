# PL Bets

## Description

### Summary

This repository contains the source code and documentation for the PL Bets project, a machine learning full-stack docker application written with in Python, and a frontend written in ReactJS.

The project uses neural network modeled with Tensorflow and Keras to predict the outcomes of a future match based on individual player statistics for each player in the squads.

Additionally, the frontend showcases outcome prediction for each of the matches in the upcoming gameweek, using logistic regression, based on the historic team results.

### Structure

- Frontend container - Hosts web server
- Postgres container - Holds all player and team data
- Prediction container - Contains model and scripts to create and recreate model, and API to handle and serve predictions
- API container - Connecting frontend to database, serving player and team data

## Table of Contents

- [Data Sources](#sources)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Contributing](#contributing)  

## Sources

Data used in these models starts in the 2017-2018 season, bar the squad data, which is being fetched from the 2016-2017 season, onwards:

[Player stats](https://fbref.com/)  
[Match facts](https://www.football-data.co.uk)  
[Fixtures](https://fixturedownload.com/)  
[Squads](https://www.footballsquads.co.uk/)  

## Installation

### Dependencies

Ensure you have docker installed on your machine. If not, Docker can be downloaded [here](https://www.docker.com/), selecting the correct download based on your operating system.

## Usage

Makefile contains commands to setup and run the docker compose for this project

Enter app folder

```bash
cd app
```

### Start project

```bash
make devstackbuild
make devstackup
```

### Rebuild project

```bash
make devstackrebuild
```

### Restart project

```bash
make devstackreboot
```

### Stop

```bash
make devstackdown
```

See [Makefile](./app/Makefile) to see all commands available

After the containers have started, navigate to the [frontend](http://localhost:3000) at ```localhost:3000```

## Contributing

[Dominic Lawson](https://github.com/DomLaw82)

## Notes

- Compatibility issues between PyPi, Tensorflow and h5py mean that h5py==3.9.0 & tensorflow==2.12.0 must be the versions used with these packages
- In VSCode add :

```json
"python.analysis.extraPaths": [
    "./app/utils"
]
```

to your settings.json to suppress errors about the utility modules

## TODO

- Neural net fix - predict_match_outcome.py

- Player data - match logs from fbref - CREATE A NEW TABLE TO SHOW INDIVIDUAL GAME PERFORMANCES FOR EACH PLAYER
- API-FOOTBALL.COM  to get more data

- Manager page
- Scrape manager data - [Wikipedia](https://en.wikipedia.org/wiki/List_of_Premier_League_managers) [x]
- - Typical stats per position for each manager
- - Typical overall team stats for each manager
- - Per 90 stats per manager
- - Sum team stats during managers career to identify key characteristics of each managers personal philosophy/tactics
- - Perform PCA to identify manager/tactic types
- - Identify key metrics for each tactic
- - Display in Tactics/Coaches page
- - Find some way to include this in outcome prediction
- - - Use model to determine effectiveness of each tactic against each other

- FPL page
- - Solver - Generate the best team based on fpl rules
- - Ratings for each player for each upcoming game
- - - expected points tally for each game
- - Compare players/positions/teams

- Provide choice stats for each game, comparing the two teams and tactics

- Set up CI/CD pipeline for deployment to AWS
- Deploy to AWS with CDK/Terraform  

- Caching
- General code cleanup and re-factoring
- Review "Separation of concerns"

- prediction model edits
