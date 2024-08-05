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

- Set up CI/CD pipeline for deployment to AWS
- Deploy to AWS with CDK/Terraform  

--- THEN ---

- Caching
- General code cleanup and re-factoring
- Review "Separation of concerns"
