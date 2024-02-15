# PL Bets

## Description

### Summary
This repository contains the source code and documentation for the PL Bets project, a machine learning full stack docker application written with Python, CSS, HTML.

The project uses Neural Network modeled with Tensorflow and Keras to predict the outcomes of future match based on team form, head-to-head form and individual player statistics for each of the squads.

### Structure
- Frontend container - Hosts web server
- Postgres container - Holds all player data
- Prediction container - Contains model and scripts to create and recreate model, and API to handle and serve predictions
- API container - Connecting frontend to database

## Table of Contents
- [Data Sources](#sources)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Sources

[Player stats](https://fbref.com/)  
[Match facts](https://www.football-data.co.uk)  
[Fixtures](https://fixturedownload.com/)  
[Squads](https://www.footballsquads.co.uk/)  

## Installation

### Dependencies
Ensure you have docker installed on your machine.


## Usage
Makefile contains commands to setup and run the docker compose for this project

### Start project
```
make devstackbuild
make devstackup
```

### Rebuild project
```
make devstackrebuild
```

### Restart project
```
make devstackreboot
```
After the containers have started, navigate to the [frontend](http://localhost:3000) at localhost:3000

## Contributing

[Dominic Lawson](https://github.com/DomLaw82)
