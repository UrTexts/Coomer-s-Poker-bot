# Coomer's Poker Bot

**Discord Poker Bot** is a powerful and fun multiplayer poker bot built using `discord.py`. Designed to provide an immersive poker experience right inside your Discord server, this bot includes all the essential features needed to host a professional game of Texas Hold'em. The bot is designed to work out of the box, provided your bot is set up correctly in the [Discord Developer Portal](https://discord.com/developers/applications).

---

## Features

### Gameplay Commands
- **`!newgame`**  
  *Starts a new game, allowing players to join.*  
  Command function: `new_game`
  
- **`!join`**  
  *Lets you join a game that is about to begin.*  
  Command function: `join_game`
  
- **`!start`**  
  *Begins a game after all players have joined.*  
  Command function: `start_game`

- **`!deal`**  
  *Deals the hole cards to all the players.*  
  Command function: `deal_hand`

- **`!call`**  
  *Matches the current bet.*  
  Command function: `call_bet`

- **`!raise`**  
  *Increases the size of the current bet.*  
  Command function: `raise_bet`

- **`!check`**  
  *Bet no money.*  
  Command function: `check`

- **`!fold`**  
  *Discard your hand and forfeit the pot.*  
  Command function: `fold_hand`

- **`!all-in`**  
  *Bets the entirety of your remaining chips.*  
  Command function: `all_in`

### Utility Commands
- **`!help`**  
  *Shows the list of commands.*  
  Command function: `show_help`

- **`!options`**  
  *Displays the list of options and their current values.*  
  Command function: `show_options`

- **`!set`**  
  *Sets the value of an option.*  
  Command function: `set_option`

- **`!count`**  
  *Shows how many chips each player has left.*  
  Command function: `chip_count`

---

## Why Choose This Bot?

- **Built with `discord.py`**  
  This is the **only poker bot** leveraging the power and flexibility of `discord.py`.  
  No complicated setup required—just follow the steps below to get started!

- **Easy to Use**  
  Once your bot is configured in the Discord Developer Portal, this bot is ready to run with minimal effort.

- **Fully Multiplayer**  
  Supports multiple players for a fun and competitive game of poker.

- **Customizable**  
  Includes commands to set game options and track player stats.

---

## Installation & Setup

1. Clone the repository to your local machine:  
   ```bash
   git clone <repository-url>
   cd poker-bot
