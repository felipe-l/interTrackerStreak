# League of Legends Discord Win Streak Tracker

![Project Logo](images/interLogo.png)

## Overview

This project consists of a Discord bot that interacts with the League of Legends API to provide information about players' win streaks and game stats. It includes two main components:

1. **Bot Functionality (`main.py`):** A Discord bot written in Python using the `discord.py` library. The bot connects to your Discord server, listens to events, and responds to user commands with information from the League of Legends API.

2. **Win Streak Tracker (`detectStreak.py`):** A backend script responsible for monitoring players' win streaks. It interfaces with the `riotApi.py` module to fetch player data, calculates win streaks, and updates a SQLite database (`my_database.db`) located in the `modules` directory with the streak information.

## Project Structure
    interTrackerConda/
    │
    ├── modules/
    │ ├── init.py
    │ ├── databaseFunctions.py
    │ ├── riotApi.py
    │ └── my_database.db
    │
    ├── main.py
    ├── config.py
    ├── detectStreak.py
    ├── environment.yml
    └── .gitignore<br>

- The `modules` directory contains modules for interfacing with the League of Legends API (`riotApi.py`) and managing the database (`databaseFunctions.py`). The SQLite database (`my_database.db`) for win streak information is also located in this directory.
- The root directory holds files related to the Discord bot, including the main bot script (`main.py`), configuration settings (`config.py`), a script to track win streaks (`detectStreak.py`), the environment file (`environment.yml`), and the `.gitignore` file.

## Getting Started

1. Clone this repository to your local machine.
2. Set up a Python virtual environment and activate it.
3. Install project dependencies from the `environment.yml` file:

   ```sh
   conda env create -f environment.yml
   conda activate your_environment_name
   
4. Set up your Discord bot on the Discord Developer Portal.
5. Copy config.example.py to config.py and fill in your Discord bot token.
6. Run the Discord bot and the win streak tracker in separate terminal sessions from the root directory:

    ```sh
    python main.py
    python detectStreak.py

## Usage
- The Discord bot responds to user commands with information about win streaks and game stats. Use !help to see available commands.
- The win streak tracker (detectStreak.py) automatically updates the database with win streak information for tracked players.

## Contributing
Contributions are welcome! Feel free to open issues, submit pull requests, or suggest improvements.

## Licesnse
This project is licensed under the MIT License.